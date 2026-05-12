# schema.osm.dev

This repository contains the first executable schema artifacts extracted from `PLAN.md`.

## Artifact layout

- `schemas/` contains JSON Schema 2020-12 artifacts for `operation.use_case`, `automation.smetion`, `perception.perception`, command state, approval state, and use-case profile bundles.
- `profiles/penetration-testing-technical-vulnerability-management.profile.json` is the first concrete profile. It models the end-to-end penetration-testing and technical vulnerability-management use case.
- `examples/penetration-testing-tvm/` contains examples that exercise source-to-smetion, perception, command proposal, approval, and commit flow.
- `scripts/validate_examples.py` validates the profile and examples without external dependencies.

## Validate

```bash
python3 scripts/validate_examples.py
```

The validator checks the local JSON artifacts, then runs semantic checks that the profile command catalogue covers the use case, smetion output perception types are declared by the profile, and the example flow preserves the perception-to-command-to-approval order.

## Current scope

The first schema pass is intentionally focused on the model introduced in sections 12, 13, 15, and 17 of `PLAN.md`. Downstream domain payloads such as `asset.asset`, `risk.relative_group`, `operation.plan`, and `assurance.finding` are represented inside command payloads but not yet defined as full standalone schemas.
