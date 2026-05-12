# schema.osm.dev — Foundation Schema v0.1

## 1. Purpose

`schema.osm.dev` is the canonical semantic and operational definition layer for OSM.

It defines the entities, relationships, operations, constraints, lifecycle states, evidence structures, and validation rules required to manage technology operations, governance, risk, compliance, assurance, resilience, and service management in a consistent, machine-valid, agent-operable form.

The schema is designed so that humans, systems, tools, and agents can interact with OSM data without bypassing schema validity.

## 2. Initial framing

The initial schema frame leverages ISO-style management system and technology operations standards, including:

- ISO/IEC 27001 — Information Security Management System requirements
- ISO/IEC 27002 — Information security controls and implementation guidance
- ISO 22301 — Business Continuity Management System requirements
- Related operational standards and frameworks where useful, including ISO/IEC 20000, ISO 31000, ISO/IEC 27005, ASD ISM, Essential Eight, SOC 2, PCI DSS, and CIS Controls

These standards are not treated as isolated checklists. They are treated as structured source content mapped into reusable OSM schema entities.

## 3. Design principles

### 3.1 Canonical by default

Every OSM object should resolve to a canonical schema definition.

Canonical definitions include:

- entity type
- required attributes
- optional attributes
- relationship rules
- lifecycle states
- permitted operations
- validation constraints
- provenance requirements
- evidence expectations

### 3.2 No duplication

OSM does not duplicate entities, definitions, controls, risks, requirements, assets, or obligations unless there is a justified semantic difference.

Default behaviour:

1. Reuse existing canonical definition.
2. Extend through permitted attributes or relationships.
3. Fork only when semantic divergence is necessary.
4. Coalesce equivalent or reconcilable entities when safe.

### 3.3 Fork only when necessary

A fork is permitted only when an entity or definition has diverged in a way that cannot be represented safely through context, inheritance, profile, jurisdiction, version, applicability, or local configuration.

Every fork must record:

- source entity
- reason for fork
- scope of divergence
- owner
- effective date
- review trigger
- coalescence criteria

### 3.4 Coalesce when able

Where two or more entities become semantically equivalent, redundant, or safely reconcilable, OSM should coalesce them into a shared canonical representation.

Coalescence must preserve:

- historical references
- audit trail
- evidence links
- dependent relationships
- prior decisions
- external mappings

### 3.5 Agentic interaction, schema-valid output

All non-machine interaction with OSM data is mediated through agentic ALMs.

Agentic ALMs translate human intent into schema-valid operations. They may assist with drafting, reviewing, mapping, classifying, linking, testing, reporting, or decision support, but the resulting data changes must remain exact and complete against the schema.

### 3.6 Standards as source content, not rigid structure

ISO and other standards provide authoritative domain concepts, requirements, controls, control attributes, implementation guidance, and assurance expectations.

They do not dictate the entire OSM schema structure.

The OSM schema separates:

- canonical operational entities
- standards-derived requirements
- standards-derived controls
- implementation artefacts
- evidence
- assessments
- treatment decisions
- assurance results

## 4. Root schema domains

The schema begins with the following root domains.

| Domain | Purpose |
|---|---|
| `identity` | Defines organisations, people, teams, roles, accounts, agents, and authorities. |
| `operation` | Defines services, activities, processes, procedures, tasks, jobs, events, and workflows. |
| `asset` | Defines information, systems, applications, infrastructure, facilities, records, data stores, and other associated assets. |
| `governance` | Defines objectives, policies, rules, responsibilities, approvals, delegations, decisions, and oversight structures. |
| `risk` | Defines risks, threats, vulnerabilities, impacts, likelihoods, treatments, controls, and residual risk. |
| `control` | Defines controls, control objectives, implementation patterns, operating expectations, and verification methods. |
| `compliance` | Defines standards, clauses, requirements, obligations, mappings, applicability, exclusions, and conformance status. |
| `evidence` | Defines records, artefacts, observations, attestations, test results, audit evidence, and proof objects. |
| `assurance` | Defines audits, assessments, reviews, findings, nonconformities, corrective actions, and assurance outcomes. |
| `continuity` | Defines business impact analysis, prioritized activities, resources, dependencies, recovery objectives, continuity strategies, plans, exercises, and recovery. |
| `integration` | Defines external systems, connectors, synchronisation jobs, imported objects, source records, and reconciliation status. |
| `schema` | Defines schema entities, versions, profiles, extensions, forks, coalescence rules, and validation constraints. |

## 5. Primitive object model

Every persisted OSM object should inherit from `schema.object`.

### 5.1 `schema.object`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Globally unique object identifier. |
| `type` | `schema.type_ref` | yes | Canonical schema type. |
| `canonical_key` | `string` | conditional | Stable human-meaningful key where applicable. |
| `name` | `string` | yes | Primary display name. |
| `description` | `markdown` | optional | Human-readable explanation. |
| `status` | `schema.lifecycle_status` | yes | Current lifecycle state. |
| `owner_ref` | `identity.party_ref` | conditional | Accountable owner. |
| `tenant_ref` | `identity.tenant_ref` | yes | Owning tenant or organisational boundary. |
| `source_ref` | `integration.source_ref` | optional | Source system or source import reference. |
| `created_at` | `datetime` | yes | Creation timestamp. |
| `created_by` | `identity.actor_ref` | yes | Creating actor. |
| `updated_at` | `datetime` | yes | Last update timestamp. |
| `updated_by` | `identity.actor_ref` | yes | Last modifying actor. |
| `valid_from` | `date` | optional | Date from which object is valid. |
| `valid_until` | `date` | optional | Date until which object is valid. |
| `provenance` | `schema.provenance[]` | yes | Origin, derivation, and decision trail. |
| `labels` | `schema.label[]` | optional | Classification, tags, and search labels. |
| `external_refs` | `schema.external_ref[]` | optional | Links to external systems, standards, documents, or records. |

### 5.2 Common lifecycle states

Initial lifecycle states:

- `draft`
- `proposed`
- `active`
- `under_review`
- `superseded`
- `retired`
- `archived`
- `rejected`

Domain-specific states may extend these through schema profiles, but should not redefine the base state semantics.

## 6. Primitive relationship model

Relationships are first-class schema objects, not implicit links.

### 6.1 `schema.relationship`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique relationship identifier. |
| `relationship_type` | `schema.relationship_type_ref` | yes | Canonical relationship type. |
| `source_ref` | `schema.object_ref` | yes | Source object. |
| `target_ref` | `schema.object_ref` | yes | Target object. |
| `directionality` | `enum` | yes | Directed, bidirectional, or derived. |
| `strength` | `enum` | optional | Strong, weak, inferred, candidate. |
| `status` | `schema.lifecycle_status` | yes | Relationship lifecycle status. |
| `valid_from` | `date` | optional | Start of relationship validity. |
| `valid_until` | `date` | optional | End of relationship validity. |
| `evidence_refs` | `evidence.object_ref[]` | optional | Evidence supporting the relationship. |
| `provenance` | `schema.provenance[]` | yes | Source and rationale. |

### 6.2 Initial relationship types

| Relationship | Meaning |
|---|---|
| `owns` | Accountable ownership. |
| `custodies` | Day-to-day custodianship without full accountability. |
| `implements` | Source object implements target requirement, control, or design. |
| `supports` | Source object supports the operation of target object. |
| `depends_on` | Source object depends on target object. |
| `governs` | Source object governs target object. |
| `applies_to` | Source object applies to target object or scope. |
| `satisfies` | Source object satisfies target requirement or obligation. |
| `evidences` | Source object provides evidence for target assertion. |
| `mitigates` | Source object mitigates target risk, threat, or vulnerability. |
| `causes` | Source object causes or contributes to target object. |
| `maps_to` | Source object maps to semantically related target object. |
| `derived_from` | Source object is derived from target object. |
| `forked_from` | Source object is a fork of target object. |
| `coalesced_into` | Source object has been coalesced into target canonical object. |
| `supersedes` | Source object replaces target object. |
| `conflicts_with` | Source object conflicts with target object. |
| `requires` | Source object requires target object. |

## 7. Initial standards-content model

Standards are modelled as source systems of authoritative requirements, controls, guidance, and attributes.

### 7.1 `compliance.standard`

Represents a standard, framework, regulation, contractual framework, policy framework, or control catalogue.

Examples:

- ISO/IEC 27001:2022
- ISO/IEC 27002:2022
- ISO 22301:2019
- ASD ISM
- Essential Eight
- SOC 2 Trust Services Criteria
- CIS Controls

Core attributes:

| Attribute | Type | Required |
|---|---:|---:|
| `standard_id` | `string` | yes |
| `name` | `string` | yes |
| `publisher` | `string` | yes |
| `edition` | `string` | optional |
| `publication_date` | `date` | optional |
| `jurisdiction` | `string[]` | optional |
| `standard_type` | `enum` | yes |
| `license_constraints` | `markdown` | optional |
| `source_uri` | `uri` | optional |

### 7.2 `compliance.requirement`

Represents a normative requirement, clause, criterion, obligation, or expected outcome.

Examples:

- ISO 27001 clause requirement
- ISO 22301 BCMS requirement
- contractual security requirement
- regulatory obligation

### 7.3 `control.catalogue_control`

Represents a reusable control from a catalogue or standard.

For ISO/IEC 27002, the catalogue control model should support:

- control identifier
- control title
- theme
- control text
- purpose
- guidance
- other information
- attributes
- related requirements
- implementation patterns
- evidence expectations

### 7.4 `control.implemented_control`

Represents a tenant-specific implementation of a catalogue control or locally defined control.

It must distinguish:

- what the control is supposed to do
- where it applies
- who owns it
- how it is implemented
- how it is operated
- how it is evidenced
- how its effectiveness is assessed
- which risks, requirements, and assets it relates to

## 8. ISO/IEC 27002 as first control catalogue

ISO/IEC 27002:2022 is suitable as the first detailed control catalogue because it already provides reusable concepts that map cleanly to OSM schema concepts:

- controls
- themes
- attributes
- control type
- information security properties
- cybersecurity concepts
- operational capabilities
- security domains
- control text
- purpose
- guidance
- other information

Initial ISO/IEC 27002 control themes:

| Theme | OSM representation |
|---|---|
| Organisational controls | `control.theme.organizational` |
| People controls | `control.theme.people` |
| Physical controls | `control.theme.physical` |
| Technological controls | `control.theme.technological` |

Initial ISO/IEC 27002 control attributes:

| ISO attribute | OSM attribute namespace |
|---|---|
| Control type | `control.attribute.control_type` |
| Information security properties | `control.attribute.security_property` |
| Cybersecurity concepts | `control.attribute.cybersecurity_concept` |
| Operational capabilities | `control.attribute.operational_capability` |
| Security domains | `control.attribute.security_domain` |

## 9. ISO 22301 as first continuity requirements model

ISO 22301 is suitable as the first continuity requirements source because it defines management-system requirements for business continuity, including:

- organisational context
- interested parties
- legal and regulatory requirements
- BCMS scope
- leadership and commitment
- policy
- roles and responsibilities
- risks and opportunities
- objectives
- resources
- competence
- awareness
- communication
- documented information
- operational planning and control
- business impact analysis
- risk assessment
- continuity strategies and solutions
- business continuity plans and procedures
- exercising and testing
- performance evaluation
- improvement

These should be represented primarily as `compliance.requirement` objects, with supporting `continuity.*` operational entities.

## 10. Initial OSM entity candidates

The following entity types should be defined next.

### Identity

- `identity.tenant`
- `identity.organization`
- `identity.organizational_unit`
- `identity.person`
- `identity.team`
- `identity.role`
- `identity.actor`
- `identity.authority`
- `identity.account`

### Operation

- `operation.service`
- `operation.product`
- `operation.process`
- `operation.procedure`
- `operation.activity`
- `operation.task`
- `operation.job`
- `operation.workflow`
- `operation.event`
- `operation.incident`
- `operation.change`

### Asset

- `asset.asset`
- `asset.information_asset`
- `asset.system`
- `asset.application`
- `asset.infrastructure_component`
- `asset.device`
- `asset.network`
- `asset.data_store`
- `asset.record`
- `asset.facility`
- `asset.supplier_asset`

### Governance

- `governance.objective`
- `governance.policy`
- `governance.topic_policy`
- `governance.rule`
- `governance.responsibility`
- `governance.decision`
- `governance.approval`
- `governance.exception`
- `governance.review`

### Risk

- `risk.risk`
- `risk.threat`
- `risk.vulnerability`
- `risk.impact`
- `risk.likelihood`
- `risk.control_effect`
- `risk.treatment`
- `risk.acceptance`
- `risk.scenario`

### Control

- `control.catalogue_control`
- `control.implemented_control`
- `control.control_objective`
- `control.control_activity`
- `control.control_test`
- `control.control_result`
- `control.control_exception`

### Compliance

- `compliance.standard`
- `compliance.clause`
- `compliance.requirement`
- `compliance.obligation`
- `compliance.mapping`
- `compliance.applicability_decision`
- `compliance.conformance_status`
- `compliance.statement_of_applicability`

### Evidence

- `evidence.record`
- `evidence.artefact`
- `evidence.observation`
- `evidence.attestation`
- `evidence.test_result`
- `evidence.audit_sample`
- `evidence.external_report`

### Assurance

- `assurance.assessment`
- `assurance.audit`
- `assurance.finding`
- `assurance.nonconformity`
- `assurance.observation`
- `assurance.corrective_action`
- `assurance.management_review`

### Continuity

- `continuity.business_impact_analysis`
- `continuity.prioritized_activity`
- `continuity.impact_type`
- `continuity.resource_requirement`
- `continuity.dependency`
- `continuity.rto`
- `continuity.rpo`
- `continuity.mtpd`
- `continuity.strategy`
- `continuity.solution`
- `continuity.plan`
- `continuity.exercise`
- `continuity.recovery_process`

### Integration

- `integration.system`
- `integration.connector`
- `integration.source_record`
- `integration.sync_job`
- `integration.ingestion_rule`
- `integration.reconciliation_result`
- `integration.transform`

### Schema governance

- `schema.type`
- `schema.profile`
- `schema.extension`
- `schema.constraint`
- `schema.operation`
- `schema.validation_result`
- `schema.fork`
- `schema.coalescence`
- `schema.version`

## 11. Initial next build order

The schema should be built in this order:

1. `schema.object`
2. `schema.relationship`
3. `identity.party` and actor model
4. `compliance.standard`
5. `compliance.requirement`
6. `control.catalogue_control`
7. `control.implemented_control`
8. `asset.asset`
9. `operation.service` and `operation.process`
10. `risk.risk`
11. `evidence.record`
12. `assurance.assessment`
13. ISO/IEC 27002 control catalogue import profile
14. ISO 22301 requirement import profile
15. OSM tenant implementation profile

## 12. Use-case driven extension model

OSM implementation and data-layer capabilities are extended through first-class `use_case` definitions.

A use case is not only a user story or process description. In OSM it is a schema-governed operational pattern that defines:

- intent
- actors and agents
- input perceptions
- required context
- permitted operations
- expected outputs
- validation rules
- evidence requirements
- handoff rules
- escalation rules
- success criteria
- lifecycle states

Use cases allow OSM to grow dynamically while preserving exact schema validity.

### 12.1 `operation.use_case`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique use-case identifier. |
| `canonical_key` | `string` | yes | Stable key, e.g. `vulnerability.intake.triage`. |
| `name` | `string` | yes | Human-readable name. |
| `description` | `markdown` | yes | Use-case purpose and operating context. |
| `domain_refs` | `schema.domain_ref[]` | yes | Related schema domains. |
| `trigger_types` | `operation.trigger_type[]` | yes | Events, schedules, perceptions, manual requests, or agent-initiated triggers. |
| `actor_roles` | `identity.role_ref[]` | optional | Human roles involved. |
| `agent_roles` | `agent.role_ref[]` | optional | Agent roles involved. |
| `input_types` | `schema.type_ref[]` | yes | Permitted input object types. |
| `output_types` | `schema.type_ref[]` | yes | Expected output object types. |
| `permitted_commands` | `schema.command_ref[]` | yes | Commands this use case may invoke. |
| `validation_profile_ref` | `schema.validation_profile_ref` | yes | Validation profile to apply. |
| `evidence_expectations` | `evidence.expectation_ref[]` | optional | Evidence required or produced. |
| `handoff_rules` | `operation.handoff_rule[]` | optional | Rules for agent-to-agent or agent-to-human handoff. |
| `approval_policy_ref` | `governance.policy_ref` | optional | Approval policy for committing changes. |
| `success_criteria` | `markdown` | optional | Completion and quality criteria. |
| `failure_modes` | `operation.failure_mode[]` | optional | Expected failure classes and responses. |

### 12.2 Use-case examples

Initial use-case examples:

- `control.catalogue.import.oscal`
- `control.implementation.design`
- `risk.scenario.identify`
- `risk.treatment.propose`
- `vulnerability.intake.triage`
- `incident.event.classify`
- `evidence.collect.validate`
- `policy.review.perform`
- `supplier.assessment.perform`
- `continuity.bia.perform`
- `change.impact.assess`
- `architecture.pattern.review`
- `test.case.generate`
- `operations.activity.schedule`

## 13. Perception model

OSM should distinguish between raw data, smetion-produced perceptions, agent interpretations, structured observations, assertions, and validated canonical facts.

This is essential for monitoring data, logs, alerts, vulnerability feeds, agent observations, audit findings, and operational telemetry.

### 13.1 Perception pipeline

```text
source data
  -> ingestion event
  -> smetion
  -> perception
  -> agent interpretation
  -> observation
  -> assertion
  -> validated object / relationship / decision
```

A smetion is an SME-authored automation that translates raw, external, noisy, or tool-specific data into structured OSM perceptions.

Smetions do not generally decide canonical truth. They normalise, enrich, classify, correlate, score, and frame source data so agents and validation workflows can reason over it.

### 13.2 `automation.smetion`

A smetion is an SME automation: a domain-specific translator from source data into OSM perceptions.

The name combines SME and automation. It represents expert-authored operational logic that captures how a subject matter expert would interpret raw data before passing it to agents.

Examples:

- translate a CrowdStrike detection into a security event perception
- translate an AWS GuardDuty finding into a threat/risk perception
- translate a Microsoft Entra risky sign-in into an identity-risk perception
- translate a failed backup job into a continuity/control perception
- translate a Jira ticket transition into an operational-status perception
- translate a vulnerability scan result into an asset/vulnerability perception
- translate an OSCAL control update into a compliance-change perception

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique smetion identifier. |
| `canonical_key` | `string` | yes | Stable key, e.g. `smetion.aws.guardduty.finding_to_threat_perception`. |
| `name` | `string` | yes | Human-readable name. |
| `description` | `markdown` | yes | What the smetion translates and why. |
| `sme_domain_refs` | `schema.domain_ref[]` | yes | SME domains encoded by the automation. |
| `source_type_refs` | `schema.type_ref[]` | yes | Input source object or event types. |
| `output_perception_types` | `perception.type_ref[]` | yes | Perception types produced. |
| `trigger_types` | `operation.trigger_type[]` | yes | Event, schedule, manual, webhook, polling, or batch trigger. |
| `transform_ref` | `integration.transform_ref` | yes | Transformation logic or mapping definition. |
| `normalisation_rules` | `schema.rule_ref[]` | optional | Data cleaning, field mapping, canonicalisation, and enrichment rules. |
| `classification_rules` | `schema.rule_ref[]` | optional | Rules for assigning perception types, severity, confidence, and affected domains. |
| `correlation_rules` | `schema.rule_ref[]` | optional | Rules for linking source records to existing OSM objects. |
| `confidence_model` | `automation.confidence_model_ref` | optional | Method for assigning confidence. |
| `validation_profile_ref` | `schema.validation_profile_ref` | yes | Validation required before perception emission. |
| `owner_ref` | `identity.party_ref` | yes | SME or team accountable for the smetion. |
| `status` | `schema.lifecycle_status` | yes | Draft, active, under_review, retired, etc. |

### 13.3 Smetion lifecycle

Smetions should follow a controlled lifecycle:

- `draft`
- `test`
- `active`
- `under_review`
- `superseded`
- `retired`

A smetion should be reviewed when:

- the source integration changes
- the source data schema changes
- a false positive or false negative pattern is identified
- a related standard/control requirement changes
- an agent repeatedly rejects or corrects its perceptions
- an incident, audit, or post-implementation review identifies translation error

### 13.4 Smetion output rules

A smetion may emit:

- `perception.perception`
- `perception.observation`
- `schema.command.proposal`
- `evidence.candidate_record`
- `operation.candidate_task`

But it should not directly commit canonical state except in tightly controlled low-risk cases.

Default rule:

```text
smetion output is candidate reality, not canonical truth
```

### 13.5 Smetion versus agent

| Capability | Smetion | Agent |
|---|---|---|
| Purpose | Translate source data into structured perceptions. | Interpret perceptions, reason, plan, decide, propose, validate, and operate. |
| Behaviour | Mostly deterministic or rule-bound. | Adaptive, goal-directed, context-aware. |
| Authorship | SME-authored automation. | Agent capability and policy profile. |
| Input | Raw data, logs, events, source records. | Perceptions, observations, schema objects, use cases, tasks. |
| Output | Perceptions, candidate observations, candidate commands. | Work products, staged commands, decisions, handoffs. |
| Risk | Translation error. | Reasoning/action error. |
| Governance | SME owner and validation profile. | Permission profile and supervision mode. |

### 13.6 `perception.perception`

A perception is an interpreted view of data by a human, system, or agent. It is not automatically canonical truth.

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique perception identifier. |
| `perceiver_ref` | `identity.actor_ref | agent.agent_ref | integration.system_ref` | yes | Actor, agent, or system that perceived the data. |
| `source_refs` | `schema.object_ref[]` | yes | Source events, records, logs, alerts, documents, or telemetry. |
| `perception_type` | `enum` | yes | Classification, anomaly, risk, relationship, evidence, requirement, control, dependency, change, incident. |
| `summary` | `markdown` | yes | Interpreted summary. |
| `confidence` | `number` | yes | Confidence score from 0 to 1. |
| `claims` | `perception.claim[]` | optional | Atomic claims made by the perception. |
| `candidate_relationships` | `schema.relationship[]` | optional | Proposed relationships. |
| `recommended_commands` | `schema.command_ref[]` | optional | Commands suggested by the perception. |
| `status` | `enum` | yes | Candidate, accepted, rejected, superseded, escalated. |
| `validation_refs` | `schema.validation_result_ref[]` | optional | Validation outcomes. |

### 13.3 `perception.observation`

An observation is a structured statement derived from perception, monitoring, review, audit, or testing.

Examples:

- A vulnerability scanner detected CVE exposure.
- A log source stopped reporting.
- A backup job failed.
- An access review is overdue.
- A policy control has no current evidence.
- A service dependency was inferred from telemetry.

### 13.4 Raw operational data types

Initial raw and semi-structured data entities:

- `telemetry.metric`
- `telemetry.log_event`
- `telemetry.alert`
- `telemetry.trace`
- `telemetry.health_check`
- `telemetry.vulnerability_finding`
- `telemetry.configuration_item`
- `telemetry.identity_event`
- `telemetry.cloud_event`
- `telemetry.ticket_event`
- `telemetry.repository_event`

These are generally source-derived and may be high volume. They should not all become canonical OSM objects unless promoted by a use case, perception, or validation rule.

## 14. Agentic IT group model

OSM agents operate as an IT group. Agents have roles, responsibilities, permissions, work queues, handoff rules, artefact expectations, and validation constraints.

Agents are not treated as generic assistants. They are typed operational actors participating in controlled organisational workflows.

### 14.1 Agent classes

Initial agent classes:

| Agent class | Primary purpose |
|---|---|
| `agent.scout` | Discover, collect, monitor, inspect, and surface candidate information. |
| `agent.concept` | Form concepts, classify information, identify patterns, and propose semantic structures. |
| `agent.architect` | Design target state, architecture patterns, controls, dependencies, and implementation approaches. |
| `agent.business_analyst` | Convert needs, obligations, risks, and objectives into requirements and use cases. |
| `agent.developer` | Produce implementation artefacts, schema definitions, integrations, automation, and code changes. |
| `agent.tester` | Validate outputs, generate test cases, verify controls, check conformance, and detect defects. |
| `agent.operator` | Execute operational workflows, monitor status, schedule recurring tasks, and maintain service state. |

### 14.2 Agent group operating pattern

```text
ScoutAgent
  -> ConceptAgent
  -> BusinessAnalystAgent
  -> ArchitectAgent
  -> DeveloperAgent
  -> TestAgent
  -> OperatorAgent
  -> ScoutAgent feedback loop
```

This is not a fixed linear workflow. It is a default collaboration pattern. Use cases define which agents participate and what handoffs are required.

### 14.3 `agent.agent`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique agent identifier. |
| `agent_class` | `agent.class_ref` | yes | Scout, concept, architect, BA, developer, tester, operator, or specialised subclass. |
| `name` | `string` | yes | Agent display name. |
| `tenant_ref` | `identity.tenant_ref` | yes | Tenant boundary. |
| `capability_refs` | `agent.capability_ref[]` | yes | Capabilities available to the agent. |
| `tool_refs` | `integration.tool_ref[]` | optional | Tools/connectors the agent can use. |
| `permission_profile_ref` | `governance.permission_profile_ref` | yes | Authorised operations. |
| `use_case_refs` | `operation.use_case_ref[]` | optional | Use cases the agent can participate in. |
| `supervision_mode` | `enum` | yes | Suggest, stage, commit_low_risk, commit_with_policy, requires_approval. |
| `handoff_policy_ref` | `operation.handoff_policy_ref` | optional | Handoff and escalation policy. |
| `status` | `schema.lifecycle_status` | yes | Agent lifecycle state. |

### 14.4 Agent work products

Agents produce work products, not unstructured responses.

Initial work product types:

- `agent.work_product.discovery_report`
- `agent.work_product.concept_model`
- `agent.work_product.requirement_brief`
- `agent.work_product.architecture_decision_record`
- `agent.work_product.schema_change_proposal`
- `agent.work_product.implementation_plan`
- `agent.work_product.code_change`
- `agent.work_product.test_plan`
- `agent.work_product.test_result`
- `agent.work_product.operational_runbook`
- `agent.work_product.handoff_note`
- `agent.work_product.validation_report`

Every work product should link to:

- source perceptions
- use case
- agent
- validation result
- impacted objects
- next recommended command or handoff

## 15. Command-mediated agent operations

Agents do not directly mutate canonical OSM objects. Agents propose or invoke schema commands.

### 15.1 Command flow

```text
perception / intent
  -> proposed command
  -> precondition validation
  -> schema validation
  -> policy validation
  -> impact analysis
  -> staged diff
  -> approval if required
  -> commit
  -> event emission
  -> projection updates
```

### 15.2 Initial agent-safe command classes

- `schema.command.propose_object`
- `schema.command.update_object`
- `schema.command.propose_relationship`
- `schema.command.attach_evidence`
- `schema.command.classify_event`
- `schema.command.create_finding`
- `schema.command.propose_requirement`
- `schema.command.propose_control_mapping`
- `schema.command.propose_risk`
- `schema.command.propose_treatment`
- `schema.command.create_task`
- `schema.command.request_human_approval`
- `schema.command.fork_object`
- `schema.command.coalesce_objects`

## 16. Modelling an IT group in OSM

The agentic IT group should be modelled similarly to a human IT function:

| IT function concept | OSM schema object |
|---|---|
| Team | `identity.team` |
| Role | `identity.role` or `agent.role` |
| Responsibility | `governance.responsibility` |
| Work queue | `operation.queue` |
| Ticket/task | `operation.task` |
| Change | `operation.change` |
| Incident | `operation.incident` |
| Problem | `operation.problem` |
| Runbook | `operation.procedure` |
| Handoff | `operation.handoff` |
| Decision | `governance.decision` |
| Artefact | `evidence.artefact` or `agent.work_product.*` |
| Review | `assurance.review` |

This permits mixed human-agent teams where responsibility, authority, approval, evidence, and accountability remain explicit.

## 17. Use Case 1: end-to-end penetration testing and technical vulnerability management

### 17.1 Purpose

This use case provides an end-to-end model for penetration testing, external/internal technical exposure analysis, asset discovery perception, technical vulnerability management, risk-group selection, mitigation planning, remediation execution, validation, and ongoing monitoring.

It perceives the output of asset discovery tooling that discovers and watches an organisation's deployed assets, initially across:

- AWS services and data stores
- Microsoft 365 people, services, identities, access paths, and exposure surfaces
- external attack/exposure views generated by an `assetsInteractor` tool using white-box, grey-box, and black-box scanning modes

It then uses `assetsInteractor` to scan, probe, examine, test, jiggle, fuzz, and otherwise interact with assets in controlled ways to generate perceptions, refine understanding/context, identify relative risk groups, propose mitigation activity sets, generate testable plans, and establish ongoing watching/monitoring.

### 17.2 Core principle

```text
asset discovery output, scanner output, and probe output are not canonical truth
```

Discovery tooling, cloud APIs, M365 APIs, scanners, logs, fuzzing output, probes, and external interactions produce source data. Smetions translate that data into perceptions. Agents interpret those perceptions and propose schema-valid changes.

Canonical asset, risk, control, and mitigation state is updated only through validated OSM commands.

### 17.3 End-to-end pipeline

```text
AWS / M365 / external scan source data
  -> ingestion event
  -> asset-discovery smetion
  -> asset / service / data / identity / exposure perceptions
  -> ScoutAgent correlation
  -> ConceptAgent semantic classification
  -> assetsInteractor scan/probe/examine/test/jiggle/fuzz cycle
  -> smetion-generated interaction perceptions
  -> context and understanding refinement
  -> relative risk group determination
  -> decider review / selection / approval
  -> standards-guided mitigation activity optimisation
  -> mitigation plan generation
  -> success criteria and test design
  -> implementation by agents and/or people
  -> validation and evidence capture
  -> established monitoring / watching
  -> feedback loop into discovery, perception, risk, and activity prioritisation
```

### 17.4 Use-case parameters

| Parameter | Type | Required | Purpose |
|---|---:|---:|---|
| `organisation_ref` | `identity.organization_ref` | yes | Organisation being assessed. |
| `scope_ref` | `operation.scope_ref` | yes | Authorised assessment scope. |
| `deciders` | `identity.person_ref[]` | yes | People authorised to review, select, and approve the relevant risk group and mitigation direction. |
| `asset_sources` | `integration.system_ref[]` | yes | Asset discovery sources, e.g. AWS, M365, scanners. |
| `assetsInteractor_ref` | `integration.tool_ref` | yes | External interaction/scanning/probing tool. |
| `interaction_modes` | `enum[]` | yes | White-box, grey-box, black-box. |
| `standards_profile_refs` | `compliance.profile_ref[]` | yes | Standards/publications used to guide activities. |
| `risk_method_ref` | `risk.method_ref` | yes | Method for grouping, scoring, and comparing risks. |
| `approval_policy_ref` | `governance.policy_ref` | yes | Review and approval rules. |
| `monitoring_profile_ref` | `operation.monitoring_profile_ref` | conditional | Watch/monitoring rules once plans are established. |

### 17.5 External tools

#### Asset discovery tooling

The asset discovery tooling is implemented as an external integration. It discovers and watches deployed organisation assets.

Initial discovery domains:

| Source | Discovery focus |
|---|---|
| AWS | Accounts, organisations, regions, services, workloads, identities, policies, networks, storage, data services, logs, security services, public exposure, encryption, backup posture. |
| Microsoft 365 | People, users, groups, roles, tenants, domains, applications, mail, SharePoint, Teams, OneDrive, Entra ID, conditional access, privileged access, external sharing, guest exposure. |

#### `assetsInteractor`

`assetsInteractor` is an external scanner/interactor that examines assets from multiple trust perspectives:

| Mode | Meaning |
|---|---|
| White-box | Uses authorised internal context, credentials, APIs, configuration, and known architecture. |
| Grey-box | Uses partial knowledge or limited credentials to simulate partner, user, supplier, or partially trusted access. |
| Black-box | Uses externally observable information and unauthenticated or internet-facing interaction. |

The tool may scan, probe, examine, test, jiggle, fuzz, fingerprint, enumerate, validate, and safely exercise asset behaviours within an authorised scope.

`assetsInteractor` does not directly mutate canonical OSM state. It emits source records and scan results that are translated by smetions into perceptions.

### 17.6 Interaction activities

`assetsInteractor` may perform controlled interaction activities including:

- passive discovery
- active probing
- service fingerprinting
- endpoint enumeration
- configuration examination
- identity/access path testing
- permission boundary testing
- authenticated configuration inspection
- unauthenticated exposure testing
- grey-box role/path testing
- fuzzing within defined safety constraints
- vulnerability validation
- exploitability confirmation where authorised
- control effectiveness probing
- data exposure checks
- externally visible attack-surface mapping

Every interaction activity must be linked to:

- authorised scope
- interaction mode
- source asset candidate
- safety constraints
- timestamp
- tool identity
- resulting source records
- resulting perceptions

### 17.7 Understanding/context refinement

The use case maintains a progressively refined model of understanding/context.

Understanding/context is built from:

- evidence
- source data
- perceptions
- observations
- prior canonical objects
- asset relationships
- business service context
- identity/access context
- standards mappings
- control coverage
- risk history
- external exposure data

#### `operation.understanding_context`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique context identifier. |
| `scope_ref` | `operation.scope_ref` | yes | Scope to which the context applies. |
| `subject_refs` | `schema.object_ref[]` | yes | Assets, services, identities, data stores, or exposure surfaces being understood. |
| `evidence_refs` | `evidence.record_ref[]` | optional | Evidence used to form context. |
| `data_refs` | `integration.source_record_ref[]` | optional | Raw/source data used. |
| `perception_refs` | `perception.perception_ref[]` | optional | Perceptions used. |
| `observation_refs` | `perception.observation_ref[]` | optional | Structured observations used. |
| `relationship_refs` | `schema.relationship_ref[]` | optional | Relevant existing or candidate relationships. |
| `confidence` | `number` | yes | Context confidence score from 0 to 1. |
| `unknowns` | `markdown[]` | optional | Known unknowns and unresolved assumptions. |
| `assumptions` | `markdown[]` | optional | Assumptions currently influencing context. |
| `last_refined_at` | `datetime` | yes | Last refinement timestamp. |
| `refined_by_refs` | `identity.actor_ref[]` | yes | Agents/people/tools involved in refinement. |

### 17.8 Relative risk group determination

A relative risk group is a selected grouping of related risks derived from the discovered and understood technical context.

Risk groups may be formed by:

- shared asset or service
- shared exposure path
- shared threat actor path
- shared vulnerability class
- shared control weakness
- shared data sensitivity
- shared business impact
- shared identity/access failure mode
- shared remediation dependency
- shared standards obligation

#### `risk.relative_group`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique risk group identifier. |
| `name` | `string` | yes | Human-readable group name. |
| `scope_ref` | `operation.scope_ref` | yes | Assessment or organisational scope. |
| `risk_refs` | `risk.risk_ref[]` | yes | Risks included in the group. |
| `subject_refs` | `schema.object_ref[]` | yes | Assets, services, identities, or data objects related to the group. |
| `basis` | `markdown` | yes | Rationale for grouping. |
| `relative_priority` | `number` | yes | Priority compared with other groups. |
| `confidence` | `number` | yes | Confidence in grouping and prioritisation. |
| `standards_refs` | `compliance.requirement_ref[]` | optional | Standards/publications informing risk relevance. |
| `evidence_refs` | `evidence.record_ref[]` | optional | Evidence supporting group. |
| `status` | `enum` | yes | Candidate, under_review, selected, approved, rejected, superseded. |
| `decider_refs` | `identity.person_ref[]` | yes | People authorised to select/approve the group. |
| `approval_ref` | `governance.approval_ref` | conditional | Approval record once selected. |

### 17.9 Mandatory decider review and approval gate

Before mitigation plans are defined and iterated, the relevant `risk.relative_group` must be reviewed, selected, and approved by the `deciders` supplied as a use-case parameter.

Required approval states:

```text
candidate
  -> under_review
  -> selected
  -> approved
  -> mitigation_planning_allowed
```

Rules:

1. Mitigation planning cannot proceed against a risk group unless its status is `approved`.
2. Approval must identify the deciders, approval timestamp, selected risk group, scope, and rationale.
3. Rejected risk groups must preserve rationale and may be superseded by later groups.
4. Risk group approval does not approve every mitigation plan; it approves the group as the mitigation-planning target.
5. If material new perceptions change the risk group basis, the group returns to `under_review` or requires re-approval.

### 17.10 Standards-guided activity optimisation

Activities are abstract units of mitigation intent. They are guided by standards, authoritative publications, control catalogues, threat guidance, vendor hardening guides, and organisational policy.

Examples of authoritative guidance sources:

- ISO/IEC 27001 requirements
- ISO/IEC 27002 controls and implementation guidance
- ISO/IEC 27005 risk treatment guidance
- ISO 22301 where continuity impact is relevant
- ASD ISM controls
- Essential Eight maturity guidance
- CIS Controls and Benchmarks
- NIST publications where applicable
- vendor hardening guides for AWS, Microsoft 365, identity, endpoint, network, and application platforms
- internal policy and architecture standards

#### `operation.activity`

An activity is abstract. It defines mitigation intent and expected risk effect, not the full implementation detail.

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique activity identifier. |
| `name` | `string` | yes | Activity name. |
| `activity_type` | `enum` | yes | Mitigate, validate, monitor, remove, harden, isolate, patch, configure, restrict, detect, recover, document. |
| `target_risk_group_ref` | `risk.relative_group_ref` | yes | Approved risk group targeted. |
| `target_risk_refs` | `risk.risk_ref[]` | optional | Specific risks targeted. |
| `objective_refs` | `governance.objective_ref[]` | optional | Objectives supported. |
| `standards_refs` | `compliance.requirement_ref[]` | optional | Standards/publications guiding the activity. |
| `expected_risk_effect` | `risk.effect_ref` | yes | Expected mitigation effect. |
| `priority` | `number` | yes | Relative priority. |
| `efficiency_score` | `number` | optional | Expected mitigation efficiency compared with alternatives. |
| `dependencies` | `operation.activity_ref[]` | optional | Other activities required first. |
| `success_criteria_refs` | `assurance.success_criteria_ref[]` | yes | Testable success criteria. |
| `status` | `schema.lifecycle_status` | yes | Draft, proposed, approved, active, completed, retired. |

### 17.11 Activity optimisation objective

The optimisation objective is:

```text
select the smallest, safest, most feasible and most effective set of activities
that produces the greatest validated mitigation of the approved relative risk group,
subject to business constraints, standards obligations, operational risk, dependencies,
available capability, and evidence/testability requirements.
```

Optimisation inputs:

- relative risk priority
- expected risk reduction
- implementation cost
- operational disruption
- dependency order
- exploitability/exposure confidence
- data sensitivity
- business criticality
- standards obligations
- control coverage gaps
- agent/person capacity
- testability
- monitoring feasibility

### 17.12 Plans implement activities

Plans are groups of concrete actions by agents and/or people. A single abstract activity may be implemented by one or many plans.

#### `operation.plan`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique plan identifier. |
| `name` | `string` | yes | Plan name. |
| `activity_refs` | `operation.activity_ref[]` | yes | Activities implemented by this plan. |
| `action_refs` | `operation.action_ref[]` | yes | Concrete actions in the plan. |
| `actor_refs` | `identity.actor_ref[]` | yes | Agents and/or people executing the plan. |
| `owner_ref` | `identity.party_ref` | yes | Accountable plan owner. |
| `success_criteria_refs` | `assurance.success_criteria_ref[]` | yes | Criteria that must be tested. |
| `test_plan_ref` | `assurance.test_plan_ref` | yes | How success criteria will be tested. |
| `evidence_expectation_refs` | `evidence.expectation_ref[]` | yes | Evidence to collect. |
| `rollback_or_recovery` | `markdown` | conditional | Rollback/recovery approach where applicable. |
| `monitoring_profile_ref` | `operation.monitoring_profile_ref` | yes | Watching/monitoring once established. |
| `status` | `enum` | yes | Draft, proposed, approved, active, established, monitoring, completed, failed, superseded, retired. |

### 17.13 Actions

Actions are concrete units of work performed by agents or people.

Examples:

- change AWS S3 bucket public-access block configuration
- restrict Entra app consent policy
- remove stale privileged role assignment
- patch vulnerable package
- rotate exposed credential
- update conditional access policy
- deploy detection rule
- add backup monitoring
- create evidence collection automation
- update system architecture documentation
- schedule retest using `assetsInteractor`

#### `operation.action`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique action identifier. |
| `name` | `string` | yes | Action name. |
| `plan_ref` | `operation.plan_ref` | yes | Parent plan. |
| `action_type` | `enum` | yes | Configure, patch, remove, restrict, deploy, test, verify, document, monitor, approve, notify. |
| `assignee_ref` | `identity.actor_ref` | yes | Agent or person responsible. |
| `target_refs` | `schema.object_ref[]` | yes | Assets, controls, services, identities, or records targeted. |
| `preconditions` | `markdown[]` | optional | Conditions required before execution. |
| `execution_method` | `enum` | yes | Manual, agentic, automated, external-tool, hybrid. |
| `expected_output_refs` | `schema.type_ref[]` | optional | Expected outputs. |
| `evidence_refs` | `evidence.record_ref[]` | optional | Evidence produced. |
| `status` | `enum` | yes | Proposed, ready, blocked, in_progress, completed, failed, cancelled. |

### 17.14 Success criteria and testability

All plans must have success criteria that can be tested.

#### `assurance.success_criteria`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique success criterion identifier. |
| `statement` | `markdown` | yes | Testable success statement. |
| `target_refs` | `schema.object_ref[]` | yes | Objects the criterion applies to. |
| `test_method` | `enum` | yes | Inspect, query, scan, probe, fuzz, simulate, sample, attest, monitor, retest. |
| `expected_result` | `markdown` | yes | Result required to pass. |
| `evidence_expectation_ref` | `evidence.expectation_ref` | yes | Evidence proving the result. |
| `pass_fail_rule` | `schema.rule_ref` | yes | Deterministic or reviewable pass/fail rule. |
| `validity_period` | `duration` | optional | How long the success result remains valid before retest. |

Examples:

- Black-box scan no longer identifies exposed administrative endpoint.
- Grey-box user cannot access restricted SharePoint site.
- White-box AWS IAM analysis shows no cross-account trust path outside approved principals.
- Vulnerability scanner confirms CVE no longer present.
- M365 external sharing setting matches approved policy.
- GuardDuty/Security Hub finding is resolved and no recurrence observed within monitoring period.

### 17.15 Established plans must be monitored/watched

Once a plan reaches `established`, it must have an active monitoring profile.

#### `operation.monitoring_profile`

| Attribute | Type | Required | Purpose |
|---|---:|---:|---|
| `id` | `uuid` | yes | Unique monitoring profile identifier. |
| `watched_refs` | `schema.object_ref[]` | yes | Assets, controls, risks, plans, or criteria watched. |
| `signal_refs` | `telemetry.signal_ref[]` | yes | Telemetry, smetions, scans, or checks used. |
| `frequency` | `duration | schedule` | yes | Watch frequency. |
| `thresholds` | `schema.rule_ref[]` | optional | Trigger conditions. |
| `responsible_actor_refs` | `identity.actor_ref[]` | yes | Operators/agents responsible. |
| `response_use_case_ref` | `operation.use_case_ref` | optional | Use case to invoke on threshold breach. |
| `status` | `schema.lifecycle_status` | yes | Active, paused, retired, failed. |

Monitoring outputs may create:

- new perceptions
- control degradation observations
- recurring vulnerability findings
- risk reactivation
- plan failure findings
- retest tasks
- escalation tasks

### 17.16 Primary OSM objects involved

#### Source and telemetry objects

- `integration.system`
- `integration.connector`
- `integration.tool`
- `integration.source_record`
- `integration.sync_job`
- `integration.reconciliation_result`
- `telemetry.cloud_event`
- `telemetry.identity_event`
- `telemetry.configuration_item`
- `telemetry.vulnerability_finding`
- `telemetry.alert`
- `telemetry.health_check`
- `telemetry.exposure_finding`
- `telemetry.interaction_result`
- `telemetry.fuzz_result`
- `telemetry.probe_result`

#### Perception objects

- `perception.perception`
- `perception.observation`
- `perception.claim`

#### Asset objects

- `asset.asset`
- `asset.information_asset`
- `asset.system`
- `asset.application`
- `asset.infrastructure_component`
- `asset.network`
- `asset.data_store`
- `asset.identity_store`
- `asset.service_account`
- `asset.external_endpoint`
- `asset.public_exposure`

#### Identity/access objects

- `identity.person`
- `identity.account`
- `identity.group`
- `identity.role`
- `identity.permission`
- `identity.access_grant`
- `identity.privileged_access`
- `identity.external_party`

#### Risk/control/compliance objects

- `risk.vulnerability`
- `risk.threat`
- `risk.risk`
- `risk.relative_group`
- `risk.treatment`
- `risk.effect`
- `control.implemented_control`
- `compliance.requirement`
- `evidence.record`
- `assurance.finding`
- `assurance.success_criteria`
- `assurance.test_plan`
- `operation.activity`
- `operation.plan`
- `operation.action`
- `operation.task`
- `operation.change`
- `operation.monitoring_profile`

### 17.17 Smetions for this use case

Initial smetions:

| Smetion | Input | Output perception |
|---|---|---|
| `smetion.aws.asset_inventory` | AWS API inventory/source records | AWS asset, service, data store, network, identity, and region perceptions. |
| `smetion.aws.iam_exposure` | IAM users, roles, policies, trust relationships, access analyzer results | Privilege, trust, access path, and excessive-permission perceptions. |
| `smetion.aws.data_exposure` | S3, RDS, DynamoDB, KMS, backups, snapshots, public policies | Data asset, confidentiality, encryption, backup, public exposure, and retention perceptions. |
| `smetion.aws.security_signal` | GuardDuty, Security Hub, Inspector, CloudTrail, Config | Threat, vulnerability, misconfiguration, incident, and control-status perceptions. |
| `smetion.m365.identity_inventory` | Entra ID users, groups, roles, applications, devices | Person, account, role, group, guest, and privileged access perceptions. |
| `smetion.m365.service_inventory` | Exchange, SharePoint, Teams, OneDrive, Defender, Purview, Intune | M365 service, data store, endpoint, and governance perceptions. |
| `smetion.m365.access_exposure` | Conditional access, external sharing, guest users, app grants, role assignments | Access/exposure, external sharing, and excessive privilege perceptions. |
| `smetion.assetsInteractor.whitebox` | Authenticated scanner/interactor results | Validated internal exposure, reachable service, configuration, vulnerability, and control-effectiveness perceptions. |
| `smetion.assetsInteractor.greybox` | Partially trusted scan/interactor results | Partner/user/supplier-perspective exposure, access path, and privilege-boundary perceptions. |
| `smetion.assetsInteractor.blackbox` | External scan/interactor results | Internet-facing exposure, attack surface, service fingerprint, and vulnerability perceptions. |
| `smetion.assetsInteractor.fuzzing` | Controlled fuzz/probe results | Behavioural weakness, input-handling, service instability, and exploitability perceptions. |
| `smetion.risk.relative_grouping` | Perceptions, observations, asset context, control context | Candidate relative risk groups. |
| `smetion.mitigation.activity_options` | Approved risk group, standards profile, constraints | Candidate mitigation activities and priority options. |

### 17.18 Perception types emitted

Initial perception types:

- `perception.asset_detected`
- `perception.asset_changed`
- `perception.asset_removed_candidate`
- `perception.service_detected`
- `perception.data_store_detected`
- `perception.identity_detected`
- `perception.access_grant_detected`
- `perception.privileged_access_detected`
- `perception.external_sharing_detected`
- `perception.public_endpoint_detected`
- `perception.public_exposure_detected`
- `perception.attack_surface_detected`
- `perception.reachable_service_detected`
- `perception.vulnerability_detected`
- `perception.exploitability_candidate_detected`
- `perception.misconfiguration_detected`
- `perception.control_gap_detected`
- `perception.control_effectiveness_candidate_detected`
- `perception.dependency_detected`
- `perception.ownership_candidate_detected`
- `perception.business_service_candidate_detected`
- `perception.evidence_candidate_detected`
- `perception.relative_risk_group_candidate_detected`
- `perception.mitigation_activity_candidate_detected`

### 17.19 Canonical update commands

This use case may propose the following commands:

- `schema.command.propose_object`
- `schema.command.update_object`
- `schema.command.propose_relationship`
- `schema.command.attach_evidence`
- `schema.command.classify_event`
- `schema.command.create_finding`
- `schema.command.propose_risk`
- `schema.command.propose_relative_risk_group`
- `schema.command.submit_risk_group_for_review`
- `schema.command.approve_risk_group`
- `schema.command.reject_risk_group`
- `schema.command.propose_activity_set`
- `schema.command.optimise_activity_set`
- `schema.command.propose_plan`
- `schema.command.approve_plan`
- `schema.command.establish_monitoring_profile`
- `schema.command.propose_treatment`
- `schema.command.propose_control_mapping`
- `schema.command.create_task`
- `schema.command.request_human_approval`
- `schema.command.coalesce_objects`
- `schema.command.mark_object_absent_candidate`

### 17.20 Example relationship outputs

Potential relationships produced or proposed:

| Relationship | Example |
|---|---|
| `contains` | AWS account contains S3 bucket. |
| `hosts` | EC2 instance hosts application component. |
| `stores` | RDS database stores customer data. |
| `processes` | Lambda function processes regulated data. |
| `exposes` | Load balancer exposes application endpoint. |
| `grants_access_to` | IAM role grants access to S3 bucket. |
| `depends_on` | Service depends on KMS key or Entra application. |
| `owned_by` | Cloud resource is owned by service owner. |
| `implements` | AWS Backup plan implements backup control. |
| `evidences` | Security Hub finding evidences control weakness. |
| `mitigates` | Conditional access policy mitigates identity risk. |
| `violates` | Public bucket policy violates data protection rule. |
| `maps_to` | AWS control maps to ISO/ISM control. |
| `targets` | Mitigation activity targets approved risk group. |
| `implemented_by` | Activity is implemented by one or more plans. |
| `tested_by` | Plan is tested by test plan or success criteria. |
| `monitored_by` | Established plan is watched by monitoring profile. |

### 17.21 Validation rules

Initial validation expectations:

1. A discovered asset must have a source reference.
2. A discovered cloud asset must have provider, account or tenant, region where applicable, and source-native identifier.
3. A public exposure perception must identify the exposure path or observable endpoint.
4. A data exposure perception must identify the affected data store or information asset candidate.
5. A privileged access perception must identify subject, permission, target, and source of authority where available.
6. A vulnerability perception must include scanner/source, affected asset candidate, finding identifier, severity, and detection timestamp.
7. A proposed canonical asset update must pass duplicate/coalescence checks.
8. A missing asset is marked as absent candidate before retirement or archival.
9. A black-box scan result cannot overwrite white-box canonical metadata without review.
10. A smetion confidence score below the threshold must route to agent/human review.
11. All active interaction testing must be linked to an authorised scope.
12. Fuzzing/probing must declare safety constraints and stopping conditions.
13. A relative risk group must be reviewed, selected, and approved by deciders before mitigation plans are defined or iterated.
14. Activities must reference an approved risk group.
15. Activities must reference at least one guiding standard, publication, internal policy, or explicit expert rationale.
16. Plans must implement one or more activities.
17. Plans must include testable success criteria.
18. Established plans must include an active monitoring profile.
19. Material new evidence that changes the risk group basis must trigger re-review.
20. Mitigation completion must be supported by evidence and test results.

### 17.22 Agent responsibilities

| Agent | Responsibilities |
|---|---|
| ScoutAgent | Monitor source feeds, detect new/changed/missing assets, correlate scanner outputs, identify candidate duplicates, collect initial exposure signals. |
| ConceptAgent | Classify perceived assets, services, identities, exposure types, data classes, vulnerability classes, risk themes, and semantic relationships. |
| BusinessAnalystAgent | Link assets, exposures, risks, and treatments to business services, obligations, owners, deciders, priorities, and use-case relevance. |
| ArchitectAgent | Model dependencies, trust boundaries, control coverage, design weaknesses, target-state implications, and mitigation patterns. |
| DeveloperAgent | Implement or modify smetions, connectors, transforms, schema extensions, automations, remediation scripts, and technical changes. |
| TestAgent | Validate mappings, duplicate handling, scanner interpretation, exploitability evidence, success criteria, retest design, and proposed canonical updates. |
| OperatorAgent | Schedule discovery jobs, scan cycles, review queues, tasks, changes, monitoring profiles, and ongoing operational state. |

### 17.23 Outputs

Expected outputs:

- current asset inventory perceptions
- current identity and access perceptions
- data store and data exposure perceptions
- public attack surface perceptions
- vulnerability and misconfiguration perceptions
- exploitability and control-effectiveness perceptions
- refined understanding/context objects
- dependency relationship candidates
- ownership candidates
- evidence candidates for controls
- candidate relative risk groups
- decider-approved selected risk groups
- standards-guided mitigation activities
- prioritised activity sets
- mitigation plans implementing activities
- success criteria and test plans
- operational actions for agents and people
- evidence records and validation results
- established monitoring profiles
- risk and treatment updates
- control gap candidates
- schema-valid object and relationship update proposals

### 17.24 Example sub-flow: vulnerability intake and treatment

```text
Telemetry source emits vulnerability finding
  -> ScoutAgent collects and normalises finding
  -> ConceptAgent classifies affected asset, vulnerability, threat, and control context
  -> assetsInteractor validates exposure/exploitability within authorised scope
  -> understanding/context is refined from evidence/data/perceptions
  -> relative risk group candidate is formed
  -> deciders review/select/approve risk group
  -> BAAgent identifies obligation, SLA, risk, and business impact
  -> ArchitectAgent proposes standards-guided mitigation activities
  -> activity set is optimised and prioritised
  -> plans are generated to implement selected activities
  -> TestAgent defines success criteria and retest method
  -> DeveloperAgent and/or people implement actions
  -> OperatorAgent schedules, executes, monitors, and closes work
  -> assetsInteractor retests
  -> evidence is attached
  -> established monitoring profile watches for recurrence or degradation
  -> risk/control status is updated through validated commands
```

Canonical objects potentially created or updated:

- `telemetry.vulnerability_finding`
- `telemetry.interaction_result`
- `telemetry.fuzz_result`
- `perception.perception`
- `perception.observation`
- `operation.understanding_context`
- `asset.system`
- `asset.infrastructure_component`
- `risk.vulnerability`
- `risk.risk`
- `risk.relative_group`
- `risk.treatment`
- `risk.effect`
- `control.implemented_control`
- `operation.activity`
- `operation.plan`
- `operation.action`
- `operation.task`
- `operation.change`
- `operation.monitoring_profile`
- `assurance.success_criteria`
- `assurance.test_plan`
- `assurance.validation_result`
- `evidence.record`

## 18. Example use case: control implementation design

```text
Requirement or control selected
  -> ConceptAgent interprets semantic intent
  -> BusinessAnalystAgent identifies operating requirement and affected stakeholders
  -> ArchitectAgent designs target implementation pattern
  -> DeveloperAgent implements configuration, automation, integration, or workflow
  -> TestAgent verifies control design and operating effectiveness evidence
  -> OperatorAgent schedules recurring operation and monitoring
```

Canonical objects potentially created or updated:

- `compliance.requirement`
- `control.catalogue_control`
- `control.implemented_control`
- `operation.procedure`
- `operation.job`
- `evidence.expectation`
- `assurance.control_test`
- `operation.recurring_activity`

## 19. Immediate open design decisions

The next schema iteration should decide:

1. Whether schema IDs are UUID-only, slug-plus-version, or both.
2. Whether every object must have an accountable owner.
3. Whether standards-derived content is represented as immutable source objects plus tenant overlays.
4. Whether implemented controls must always map to at least one risk, requirement, asset, or objective.
5. Whether evidence objects are immutable after collection.
6. Whether fork and coalescence operations require approval.
7. How agentic ALMs are authorised to propose, stage, validate, and commit schema operations.
8. Whether perceptions expire unless promoted to observations, assertions, findings, or canonical objects.
9. Which telemetry classes are stored canonically and which remain in external observability platforms with only references in OSM.
10. Whether agent work products are immutable once handed off.
11. How agent-to-agent handoff quality is validated.
12. Whether each use case requires a formal validation profile before activation.

