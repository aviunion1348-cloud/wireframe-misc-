# Technical Incident Validation — PROJECT ZERO-DAY

**Status:** internally checked story model for a fictional system; not an audit of any real product.<br>
**Scope:** enough detail to keep the screenplay legible and plausible without making dialogue a systems-design lecture.

## 1. System boundary

Tern Systems' Relay receives telemetry and maintenance events from customer systems, stores a durable observation, correlates related events, and can create a human work order in FieldDesk. It does not control a pump, valve, generator, or other physical equipment. Local instrumentation, operator procedures, and customer call trees remain authoritative. The incident therefore creates real operational risk—duplicate crews, delayed records, unconfirmed work—not a remote-control catastrophe.

```text
customer webhook
  -> relay-ingest (fast durable acknowledgement)
  -> at-least-once broker / raw-event archive
  -> correlator (read-before-write duplicate check)
  -> action publisher
  -> FieldDesk work-order API
  -> human operator verifies local condition and assignment
```

Postgres has a primary and an asynchronous read replica. The deployment's readiness check verifies that the process can reach Postgres and the broker. It does not exercise the full path or check the required unique index.

## 2. Event identity and the bug

The provider sends two identifiers:

- `source_event_id`: stable identity of the alarm across re-delivery.
- `delivery_id`: identity of one transport attempt; a retry may have a different value.

The corrected invariant is one canonical observation/action per `(tenant_id, source_event_id)` unless an explicit domain rule says otherwise. A repeated transport delivery must not be mistaken for a new alarm.

The AI-assisted helper's editor summary claims retry-safe idempotency and added tests, while also marking human review as required. The release's unit-test fixture sets the two values equal. Its timeout test replays the same queued message, not a fresh provider webhook delivery. The refactored helper derives the downstream idempotency key from the per-attempt delivery context. The test therefore passes while missing the provider's retry semantics; the assistant is a tool whose conclusion lacked the complete provider contract and production context. The 25% canary sees only a handful of single-delivery events; it matches those receipts, but none exercises the changed delivery ID. The team then promotes to all 2,140 tenants with a delayed export and no live source-to-receipt detector.

Representative **fictional, redacted** log lines:

```text
2026-10-12T21:14:03.118Z INFO ingest.accepted tenant=t-17 site=s-04 source_event_id=alarm-77 delivery_id=d-a1
2026-10-12T21:14:04.902Z WARN provider.retry tenant=t-17 site=s-04 source_event_id=alarm-77 delivery_id=d-b2
2026-10-12T21:14:05.011Z INFO dispatch.request idempotency_key=t-17:d-b2 attempt=1
2026-10-12T21:14:07.013Z WARN dispatch.timeout elapsed_ms=2000 idempotency_key=t-17:d-b2
2026-10-12T21:14:08.713Z INFO fielddesk.receipt status=201 work_order=wo-redacted source_event_id=alarm-77
```

The timeout is not proof that the downstream write failed. The receiver committed after the client's deadline. An at-least-once queue may re-deliver; using a different delivery ID as the next idempotency key lets a second work order through.

## 3. The race and missing database invariant

The consumer's check-then-insert is not atomic:

```sql
-- Illustrative pseudocode only; not a production command.
SELECT 1
FROM relay_observations
WHERE tenant_id = :tenant
  AND source_event_id = :source_id;

-- If no row is visible, the application later inserts and publishes.
```

Two workers can both observe “no row,” particularly when the check goes to a replica that is 4.8 seconds behind. They write to the primary. Without a unique index/atomic conflict-handling path, both can commit. Queue redelivery and concurrent normal/replay consumers are normal at-least-once behavior; correctness must not depend on only one delivery.

A separate pre-existing partial unique constraint allows only one open episode per tenant/site. Competing materializers can hit that constraint and return `SQLSTATE 23505`, causing consumer retries and queue pressure. That conflict is not the missing source-identity invariant: it does not prevent duplicate raw observations or make an already-issued external side effect idempotent. The two symptoms can coexist.

The intended migration 215 creates a unique index on `(tenant_id, source_event_id)` (online/concurrently for the existing table). The production migration job resolved the mutable `:release` tag to an older migration image. That bundle completed migration 214 and declared *its own* version current; it did not know about migration 215. The app was not hard-gated on the schema version or index existence.

The code must be clear that the index is defense-in-depth for a real invariant, not a substitute for using the stable ID at the downstream boundary. Both the correct key and the atomic database invariant are needed.

## 4. Stale migration and rollback limitation

Migration 214 is a contract step that drops the legacy `legacy_event_key` column after old consumers are meant to be retired. The stale runner executes that pending DDL, then exits successfully at its older migration ceiling. It does not install migration 215's unique index. The new application uses the new canonical source ID and passes its shallow readiness probe. A rollback to the previous 4.17 binary fails when that binary queries `legacy_event_key`:

```text
ERROR SQLSTATE 42703: column "legacy_event_key" does not exist
```

This is a deliberately unsafe expand/contract sequence: contract DDL ran before rollback compatibility was retired, and the migrator artifact was mutable/stale. The rollback limitation must be shown as a concrete schema incompatibility, not as a magical prohibition on reverting software. A tested forward containment path is safer than repeatedly deploying an old binary that cannot read the current schema.

A correct deployment would pin the migration runner by immutable digest, require the expected schema revision and index catalog state, separate expand from contract, and retain backward-compatible readers until the recovery window is closed.

## 5. Why green indicators coexist with failure

The `/readyz` probe answers: “Can this process connect to Postgres and the broker?” It does **not** answer: “Can a source event become exactly one, correctly attributed, visible work order?”

`relay-ingest` acknowledges after durable broker acceptance. The API's p99 can remain low while the asynchronous worker queue grows. The `action_completed` rollup is delayed by three minutes. A reasonable dashboard can therefore show:

```text
GET /readyz                         200
relay-ingest p99                   94 ms
queue oldest message              6m 12s
Postgres primary connections      94% of pool
read replica replay lag            4.8 s
FieldDesk client timeout           2.0 s
FieldDesk receipt after timeout    +1.7 s
```

There is no contradiction. Each measurement describes a different boundary and clock. The UI is misleading only if it promotes a liveness result or an ingress acknowledgement as proof of end-to-end business completion.

## 6. Evidence-driven debugging sequence

1. Classify the event as data-integrity / dispatch uncertainty. Do not restart consumers or replay a queue blindly.
2. Preserve raw webhook records, delivery IDs, source IDs, queue offsets, traces, DB state, and FieldDesk receipts. Avoid a destructive cleanup based on site/time buckets.
3. Compare ingress accepted count with downstream receipts, accounting for delayed aggregation and API commits after client timeouts.
4. Inspect the full distributed trace. It changes the working hypothesis from “FieldDesk is down” to “FieldDesk may have committed before our timeout.”
5. Join source IDs to per-attempt delivery IDs. Duplicate source IDs with different delivery IDs expose the idempotency-key error.
6. Check the primary's catalog and migration runner's resolved image digest. A completed old migration job is not proof that the current migration bundle ran.
7. Reproduce with two consumers and a delayed replica in an isolated sanitized environment. Do not induce the race against production.
8. Test the standard rollback in an isolated copy of the production schema. The missing legacy column invalidates the rollback target.
9. Publish a lower-bound impact count and explicitly retain unresolved events; do not infer “no event” from “no materialized work order.”

## 7. Containment and recovery semantics

The story's decision is to stop the outbound side effect, not to discard input:

- Let already in-flight FieldDesk requests settle; verify their receipt status.
- Set the audited global dispatch mode to `hold` and stop the action publisher.
- Keep raw ingress and append-only source records available; mark new records `held / not dispatched`.
- Do not delete duplicates solely by site, alarm category, or time bucket.
- Reconcile the provider's stable source ID, raw payload/timestamp, Relay rows, FieldDesk receipts, and the customer's local/operator record.
- Call affected operators with the exact unknowns and direct them to local procedures; no automatic summary can replace their instrumentation.
- Build the repair in isolation: immutable migration digest, schema gate, correct stable idempotency key, unique constraint, transactional outbox/atomic state transition, consumer idempotency, and concurrent retry + timeout-after-commit tests.
- Re-enable only by a verified canary that compares source events, persisted rows, downstream receipts, and operator-visible state. Recovery remains partial until each boundary is reconciled.

The dashboard's final states are separate: `RAW EVENT RECEIVED`, `WORK ORDER SENT`, and `OPERATOR CONFIRMED`. Uncertainty remains amber and queryable.

## 8. Engineering realism checks for script/footage review

- CI's skipped external integration test is visible; do not imply a skipped test passed.
- A CI fixture that makes `delivery_id == source_event_id` can mask the bug, but the retry test later makes them different.
- Feature flag scope is explicit: `Signal Assist` summary can be off while the shared normalization/action path remains active. The incident hold flag is a distinct, audited kill switch for downstream actions.
- A queue is at-least-once. It can redeliver; code must be idempotent. The story does not call queue semantics a broker defect.
- A downstream timeout is an unknown result, not a failed transaction. The receipt appearing after timeout is central evidence.
- Replica lag is measured and useful to the hypothesis; do not portray the replica as a mysterious data-loss engine.
- Migration “success” means that process exited successfully. A stale bundle can truthfully report itself current without being the bundle required by the deployed app.
- Rollback does not fail because `kubectl rollout undo` is forbidden; it fails because the previous binary queries a dropped column.
- Health probes, feature flags, canaries, and rollback each have limits. None is presented as inherently useless.
- Do not show real credentials, customer PII, actual utility topology, or real secrets. All IDs, metrics, company names, and interface data are fictional.

## 9. Items to validate with a domain reviewer in a future production

Before locking picture, ask an experienced database/reliability engineer to verify the exact DDL ordering, deployed image resolution, replica-read path, and partner idempotency contract. Ask an operations practitioner to review the customer workflow and the distinction between telemetry, work orders, and physical controls. The present chain is constructed to be plausible; it has not been independently certified by a production SRE, DBA, utility operator, or counsel.
