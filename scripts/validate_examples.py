#!/usr/bin/env python3
"""Validate schema.osm.dev profile examples without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def is_type(value: Any, expected: str) -> bool:
    actual = json_type(value)
    if expected == "number":
        return actual in {"integer", "number"}
    return actual == expected


def pointer_get(document: Any, pointer: str) -> Any:
    if not pointer:
        return document
    if not pointer.startswith("/"):
        raise ValidationError(f"Unsupported JSON pointer #{pointer}")
    current = document
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        raise ValidationError(f"Unresolved JSON pointer component {part!r}")
    return current


class SchemaValidator:
    def __init__(self, schemas: Dict[Path, Any]) -> None:
        self.schemas = schemas

    def resolve_ref(self, ref: str, base_file: Path) -> Tuple[Any, Path]:
        if "#" in ref:
            file_part, pointer = ref.split("#", 1)
        else:
            file_part, pointer = ref, ""

        if file_part:
            target = (base_file.parent / file_part).resolve()
        else:
            target = base_file.resolve()

        if target not in self.schemas:
            raise ValidationError(f"Schema reference {ref!r} resolved to unknown file {target}")

        return pointer_get(self.schemas[target], pointer), target

    def validate(self, instance: Any, schema: Any, path: str, base_file: Path) -> None:
        if not isinstance(schema, dict):
            if schema is True:
                return
            if schema is False:
                raise ValidationError(f"{path}: false schema rejects value")
            raise ValidationError(f"{path}: schema must be an object or boolean")

        if "$ref" in schema:
            ref_schema, ref_file = self.resolve_ref(schema["$ref"], base_file)
            self.validate(instance, ref_schema, path, ref_file)
            sibling_schema = {key: value for key, value in schema.items() if key != "$ref"}
            if not sibling_schema:
                return
            schema = sibling_schema

        for subschema in schema.get("allOf", []):
            self.validate(instance, subschema, path, base_file)

        if "anyOf" in schema:
            errors = []
            for subschema in schema["anyOf"]:
                try:
                    self.validate(instance, subschema, path, base_file)
                    break
                except ValidationError as exc:
                    errors.append(str(exc))
            else:
                raise ValidationError(f"{path}: did not match anyOf: {'; '.join(errors)}")

        if "oneOf" in schema:
            matches = 0
            errors = []
            for subschema in schema["oneOf"]:
                try:
                    self.validate(instance, subschema, path, base_file)
                    matches += 1
                except ValidationError as exc:
                    errors.append(str(exc))
            if matches != 1:
                raise ValidationError(f"{path}: matched {matches} oneOf branches, expected 1; {'; '.join(errors)}")

        if "const" in schema and instance != schema["const"]:
            raise ValidationError(f"{path}: expected const {schema['const']!r}, got {instance!r}")

        if "enum" in schema and instance not in schema["enum"]:
            raise ValidationError(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")

        if "type" in schema:
            expected_types = schema["type"]
            if isinstance(expected_types, str):
                expected_types = [expected_types]
            if not any(is_type(instance, expected) for expected in expected_types):
                raise ValidationError(f"{path}: expected type {expected_types!r}, got {json_type(instance)!r}")

        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                raise ValidationError(f"{path}: string shorter than minLength {schema['minLength']}")
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                raise ValidationError(f"{path}: string longer than maxLength {schema['maxLength']}")
            if "pattern" in schema and re.search(schema["pattern"], instance) is None:
                raise ValidationError(f"{path}: string {instance!r} does not match pattern {schema['pattern']!r}")

        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                raise ValidationError(f"{path}: number below minimum {schema['minimum']}")
            if "maximum" in schema and instance > schema["maximum"]:
                raise ValidationError(f"{path}: number above maximum {schema['maximum']}")

        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                raise ValidationError(f"{path}: array shorter than minItems {schema['minItems']}")
            if schema.get("uniqueItems"):
                seen = set()
                for item in instance:
                    fingerprint = json.dumps(item, sort_keys=True, separators=(",", ":"))
                    if fingerprint in seen:
                        raise ValidationError(f"{path}: array items are not unique")
                    seen.add(fingerprint)
            if "items" in schema:
                for index, item in enumerate(instance):
                    self.validate(item, schema["items"], f"{path}[{index}]", base_file)

        if isinstance(instance, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in instance:
                    raise ValidationError(f"{path}: missing required property {key!r}")

            properties = schema.get("properties", {})
            for key, subschema in properties.items():
                if key in instance:
                    self.validate(instance[key], subschema, f"{path}.{key}", base_file)

            additional = schema.get("additionalProperties", True)
            if additional is False:
                allowed = set(properties)
                extra = sorted(set(instance) - allowed)
                if extra:
                    raise ValidationError(f"{path}: unexpected properties {extra!r}")
            elif isinstance(additional, dict):
                for key, value in instance.items():
                    if key not in properties:
                        self.validate(value, additional, f"{path}.{key}", base_file)


def schema_files() -> Iterable[Path]:
    return sorted((ROOT / "schemas").glob("*.schema.json"))


def load_schemas() -> Dict[Path, Any]:
    return {path.resolve(): load_json(path) for path in schema_files()}


def validate_manifest(validator: SchemaValidator) -> int:
    manifest_path = ROOT / "examples" / "manifest.json"
    manifest = load_json(manifest_path)
    count = 0
    for entry in manifest["validations"]:
        instance_path = (ROOT / entry["instance"]).resolve()
        schema_path = (ROOT / entry["schema"]).resolve()
        instance = load_json(instance_path)
        schema = validator.schemas[schema_path]
        validator.validate(instance, schema, str(instance_path.relative_to(ROOT)), schema_path)
        count += 1
    return count


def embedded_values(node: Any, wanted_type: str) -> Iterable[Dict[str, Any]]:
    if isinstance(node, dict):
        if node.get("type") == wanted_type:
            yield node
        for value in node.values():
            yield from embedded_values(value, wanted_type)
    elif isinstance(node, list):
        for item in node:
            yield from embedded_values(item, wanted_type)


def assert_subset(name: str, values: Iterable[str], allowed: Iterable[str]) -> None:
    missing = sorted(set(values) - set(allowed))
    if missing:
        raise ValidationError(f"{name}: values not present in profile catalog: {missing}")


def run_semantic_checks() -> None:
    profile = load_json(ROOT / "profiles" / "penetration-testing-technical-vulnerability-management.profile.json")
    flow = load_json(ROOT / "examples" / "penetration-testing-tvm" / "perception-to-command-flow.json")

    assert_subset(
        "use_case.permitted_commands",
        profile["use_case"]["permitted_commands"],
        profile["command_catalog"],
    )

    smetion_outputs: List[str] = []
    for smetion in profile["smetions"]:
        smetion_outputs.extend(smetion["output_perception_types"])
    assert_subset("smetion output perception types", smetion_outputs, profile["perception_types"])

    flow_stages = [stage["stage"] for stage in flow["stages"]]
    required_order = [
        "source_ingested",
        "smetion_emitted",
        "command_proposed",
        "approval_requested",
        "approval_granted",
        "command_committed",
    ]
    positions = []
    for stage_name in required_order:
        if stage_name not in flow_stages:
            raise ValidationError(f"flow: missing stage {stage_name!r}")
        positions.append(flow_stages.index(stage_name))
    if positions != sorted(positions):
        raise ValidationError(f"flow: required stages are out of order: {flow_stages}")

    embedded_commands = [
        command for command in embedded_values(flow, "schema.command") if "command_type" in command
    ]
    embedded_perceptions = [
        perception for perception in embedded_values(flow, "perception.perception") if "perception_type" in perception
    ]

    assert_subset(
        "embedded command types",
        (command["command_type"] for command in embedded_commands),
        profile["command_catalog"],
    )
    assert_subset(
        "embedded perception types",
        (perception["perception_type"] for perception in embedded_perceptions),
        profile["perception_types"],
    )

    for command in embedded_commands:
        if command.get("status") == "committed" and command.get("approval_requirement") == "human_required":
            if "approval_ref" not in command:
                raise ValidationError(f"flow: committed human-required command {command['id']} has no approval_ref")


def main() -> int:
    try:
        schemas = load_schemas()
        validator = SchemaValidator(schemas)
        count = validate_manifest(validator)
        run_semantic_checks()
    except (OSError, json.JSONDecodeError, KeyError, ValidationError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"OK: validated {len(schemas)} schemas, {count} manifest entries, and semantic flow checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
