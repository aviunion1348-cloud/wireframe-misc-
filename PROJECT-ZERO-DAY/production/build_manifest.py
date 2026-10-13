#!/usr/bin/env python3
"""Generate the planned scene and moving-shot manifests for Project Zero-Day.

This creates planning metadata only. It does not create footage, performances,
audio, or a rendered film. Run from any directory with Python 3:
    python3 PROJECT-ZERO-DAY/production/build_manifest.py
"""
from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent

# One record per screenplay scene. Durations are editorial targets; their sum
# is 1,800 seconds, not an observed media runtime.
SCENES = [
    ("01", "Accepted", 45, "Morrow County Water — control room", "Luz Ortega", "Luz checks the local gauge, radios the night operator, calls the crew, and watches Relay mark an event accepted without a work order.", "RELAY / EVENT ACCEPTED / 01:14:36Z; WORK ORDER: —", "Relay took the event. It did not take the action.", "Low pump vibration, fluorescent room tone, one polite alert, phone line.", "Luz at desk; phone right; pencil shift sheet left; local panel visible; calm, not panicked."),
    ("02", "Seven Hours Earlier", 35, "Mara's apartment — kitchen", "Mara Velez; Mateo (voice)", "Mara packs a lunch bag, listens to Mateo's message, deletes a reply, records a more honest one, and leaves for work.", "Calendar: RELAY 4.18 — INVESTOR WALKTHROUGH 06:00", "I'll call when I know the morning for sure.", "Phone speaker, bag paper, keys; restrained domestic room tone.", "Evening, not morning; lunch bag stays on counter; no wardrobe reset after this scene."),
    ("03", "Engineering Floor", 40, "Tern Systems — engineering floor", "Mara; Theo; Sam; Ruth", "A cleaning cart passes while Theo turns his CI screen toward the group; Sam listens on headset; Ruth carries untouched coffee.", "CI checks green; optional external dispatch integration skipped.", "And the raw run?", "Office HVAC, chair movement, distant conversation; no constant typing.", "Establish meeting room left, ops nook north wall, table by windows."),
    ("04", "Runway", 50, "Tern Systems — glass meeting room", "Daniel; Ruth; Mara", "Daniel arranges three demo cards, crosses out an autonomy claim, then removes the correlation card after realizing the release is not one switch.", "Paper cards: INGEST / CORRELATE / DISPATCH.", "I thought the release was one switch.", "Paper card scrape, office bed, no score.", "Daniel removes 'fully autonomous' and does not restore it."),
    ("05", "Review", 45, "Tern Systems — engineering floor", "Mara; Ruth; Theo", "Mara reviews an AI-assisted helper whose editor summary claims retry-safe idempotency; she and Ruth assume the adapter maps context.deliveryId to stable source identity while the fixture uses equal IDs.", "Assistant summary: implementation complete, retry-safe idempotency, tests added; code uses context.deliveryId; fixture IDs equal; provider sandbox skipped.", "Is deliveryId the canonical ID after normalization?", "Quiet mouse scroll, room tone; dialogue clear.", "PR title RELAY-418; one rebase conflict; code assistant is a tool, not an authority; no credentials."),
    ("06", "Same Message", 40, "Tern Systems — engineering floor", "Theo; Mara", "Theo opens the retry test: one queued message is delivered twice after a timeout, with the same delivery context on both attempts.", "Same event object and same delivery ID on worker redelivery; no provider webhook retry exercised.", "This proves the worker can replay a message without duplicating an action.", "Trace selection, quiet office bed.", "The provider may re-deliver at a different boundary; characters have not verified its identifier semantics."),
    ("07", "Gate", 50, "Tern Systems — engineering floor", "Mara; Theo; Sam; Ruth", "The worker-retry test passes; provider-redelivery integration remains skipped; Sam checks the deployment plan and notes the mutable migration tag.", "CI green for tested scope; provider sandbox skipped; migration job still references mutable release tag.", "The migration job is still on the release tag.", "CI completion chime once; headset call vibration; office bed.", "The resolved migration digest has not yet been inspected; do not imply the bug was fixed."),
    ("08", "Accepted Means What?", 35, "Tern Systems — small conference room", "Anika (remote); Mara; Ruth; Daniel (passing)", "Anika reads from a runbook on the wall screen; Mara checks the customer UI and writes down a gap.", "Customer summary card says ACCEPTED, with no work-order state.", "Can the operator tell those apart?", "Laptop fan, remote-call room tone; quiet.", "Anika remote, Daniel waits outside glass; no identity/wardrobe drift."),
    ("09", "Customer in the Room", 55, "Tern Systems / Morrow County Water video call", "Luz; Mara; Daniel; Ruth", "Luz leans toward her camera, checks a local panel, and points to the exact distinction she needs preserved.", "Raw event attached beside grouped summary.", "Keep the original alarm attached.", "Call compression, faint water-room hum, office bed.", "Luz's work jacket, diagram, phone, and pencil sheet match scenes 1/19/25/43."),
    ("10", "Go / No-Go", 55, "Tern Systems — engineering floor", "Mara; Sam; Ruth; Anika (remote); Daniel", "Ruth reads the gate; Sam watches the cluster; Mara holds the PR open; Daniel stands outside the team's circle.", "Five-percent canary; receipt reconciliation required before widening.", "No one promotes on the green tile alone.", "Room tone, a chair shift, no trailer-like pulse.", "Sam owns stop; source-vs-work-order reconciliation is a stated gate."),
    ("11", "Canary", 30, "Tern Systems — operations nook", "Sam; Mara; Theo", "Sam starts the signed artifact; pods become ready; an old pod drains while Mara and Theo track a real request.", "Pinned application digest; two new pods ready.", "Five percent. No restart loop.", "Subtle control-plane chime, HVAC.", "Screen geography: deployment view at north wall; no shell command montage."),
    ("12", "Green", 25, "Tern Systems — operations nook", "Sam; Mara", "Sam expands the readiness definition; Mara reads it; both look back to the people and workflow, not the tile.", "200 /readyz: postgres ok, broker ok.", "It is alive.", "Single soft alert; ventilation.", "Health probe only checks connectivity; do not imply end-to-end validation."),
    ("13", "Single Delivery", 40, "Tern Systems — engineering floor", "Theo; Mara", "One low-risk maintenance alarm arrives once; Theo compares its raw archive row with one downstream receipt and records that no provider retry occurred.", "One source event, one delivery, one observed work order; no retry.", "One source event. One action. No retry on this delivery.", "Trace selection clicks; low room tone.", "This is a single-delivery sample only and does not prove retry correctness."),
    ("14", "Receipt", 20, "Tern Systems — operations nook", "Sam; Mara", "Sam hovers at promotion, withdraws her hand, and leaves the canary at five percent.", "FieldDesk 202; canary receipt count matches small sample.", "That's a receipt, not a reconciliation.", "Cursor click stops; room tone.", "No dramatic zoom on a green icon."),
    ("15", "Widen", 35, "Tern Systems — engineering floor", "Ruth; Sam; Mara", "Ruth and Sam compare sampled IDs; Sam promotes to twenty-five percent while Mara tracks queue lag.", "Sample matches; queue lag flat at this moment.", "Another receipt check before full.", "Control-panel confirmation, chair movement.", "Promotion only to 25%; not yet full fleet."),
    ("16", "Full Rollout and Demo", 60, "Tern Systems — glass meeting room / operations nook", "Sam; Ruth; Mara; Daniel; Anika (remote)", "After ten minutes at 25%, five sampled receipts match but none retried; Sam flags the three-minute export lag, Ruth approves full rollout with a manual gate, then Daniel rehearses the demo.", "25% sample matches; no provider redelivery observed; export is 3 minutes late; manual stop gate; deployment advances to 100% of 2,140 tenants.", "There's no live mismatch detector.", "Control-panel confirmation, paper demo cards, restrained office bed.", "Decision is bounded by incomplete retry evidence; keep dispatch hold switch armed; AI is assistive, not autonomous."),
    ("17", "Timeout", 30, "Tern Systems — operations nook", "Sam; Theo", "Sam tracks a downstream latency line rising past the client timeout; Theo reads the configured two-second limit.", "FieldDesk p99 crosses 2 s; responses are late, not wholly down.", "They are slow, not down.", "One subdued threshold alert; ventilation.", "Graph changes over time; no physically impossible fan acceleration."),
    ("18", "Queue", 40, "Tern Systems — engineering floor", "Mara; Theo; Ruth; Sam", "With 2,140/2,140 tenants on the release, Mara compares fast ingress counts with a delayed completion metric as queue depth rises.", "100% deployment; queue depth up; ingress p99 low; completion rollup delayed 180 sec.", "The queue is growing faster than the count can catch up.", "Office bed, message arrivals sparse and spatially placed.", "Show both clocks/metric windows; do not call the metric a real-time count."),
    ("19", "Local Alarm", 45, "Morrow County Water — control room", "Luz", "Luz reads the local instrument, radios the night operator, writes a value by hand, and sees accepted/no-assignee in Relay beside a changed reading.", "Accepted; no assignee; new reading visible but no source-to-delivery trace on the customer screen.", "Don't acknowledge it in Relay. Read the instrument.", "Pump vibration, radio reply, pencil on shift sheet.", "Physical local panel is primary; no physical failure or unprotected process."),
    ("20", "Incident", 45, "Tern Systems — engineering floor", "Sam; Mara; Anika (remote); Ruth; Daniel; Theo", "Sam opens an incident channel and assigns owners; Daniel closes the demo laptop; Ruth begins the paper log.", "SEV-1: data integrity / delayed dispatch.", "Don't reprocess anything.", "Incident page, subdued notification, no siren.", "Sam incident commander; ownership explicit; team geography maintained."),
    ("21", "Health", 50, "Tern Systems — incident room", "Sam; Mara; Anika; Ruth; Theo", "Sam moves from wall dashboard to the table; Theo identifies a competing active-episode write rejected by the existing partial unique constraint.", "99.97% rolling uptime; p99 94 ms; queue age 6m12s; pool 94%; SQLSTATE 23505 on active episode.", "That is API availability, not end-to-end success.", "Distant alert damped; log pen; room tone grows audible.", "Dashboard periods labeled; uptime is not tonight's transaction success."),
    ("22", "Trace", 50, "Tern Systems — incident room", "Mara; Anika; Theo", "Mara follows the trace, Anika aligns it with the vendor receipt, and both stop at the commit-after-timeout gap.", "POST /v2/workorders timeout 2000 ms; partner receipt arrives 1.7 s later.", "We timed out after they wrote it.", "One mouse movement, restrained low room tone; silence after the line.", "No secrets; receipt and trace timestamps consistent."),
    ("23", "One Source, Two Deliveries", 40, "Tern Systems — incident room", "Theo; Mara; Ruth", "Theo places two trace views side by side, writes the shared source ID once, then circles distinct delivery IDs.", "Two source-identical rows; third broker delivery pending.", "The provider didn't send three alarms.", "Marker squeak, faint keyboard only as needed.", "Do not delete rows; original payload and provider timestamp remain available."),
    ("24", "Replica", 45, "Tern Systems — incident room", "Sam; Ruth; Anika", "Sam opens the resolved migration image record, compares digest and version, then checks the primary index catalog.", "Replica lag 4.8 s; runner at 214; app expects 215; index absent.", "It ran. It did not run the bundle we reviewed.", "Keyboard, quiet room tone.", "Migration image is old; mutable tag; no credentials in frame."),
    ("25", "Luz on the Bridge", 55, "Tern Systems / Morrow County Water call", "Luz; Mara; Ruth; Anika", "Luz keeps one hand on the radio while she reports one local alarm, two work orders, one stale location, and an available crew.", "Local record, Relay accepted state, FieldDesk duplicate receipts.", "I need to know which event you trust.", "Radio, call codec, low pump room tone.", "Luz remains active; no cutaway that turns her into a passive voice."),
    ("26", "Reproduce", 45, "Tern Systems — isolated test room", "Theo; Sam; Mara", "Theo releases two paused test consumers together against sanitized data with a deliberately lagged replica; both read before either insert.", "Two SELECT misses; two primary inserts; no unique index.", "The check wasn't a lock.", "Test-room hum, keyboard taps synced to actions.", "Label environment ISOLATED; never run reproduction on production."),
    ("27", "Rollback Request", 35, "Tern Systems — incident room", "Ruth; Mara", "Ruth points to the rollback control; Mara checks the schema record before touching it.", "Rollback target 4.17; production schema at 214.", "First, check what 214 did.", "Soft control-room click, room tone.", "No one launches an unverified production rollback."),
    ("28", "Old Column", 40, "Tern Systems — incident room / staging display", "Sam; Ruth; Mara", "A staging rollback pod passes a process probe, then fails a real query; Sam stops the test and Ruth cancels rollback.", "SQLSTATE 42703: legacy_event_key does not exist.", "The old app cannot read this schema.", "One terminal error tone at most; no glitch effect.", "This is isolated schema-copy test, not a failed production rollback."),
    ("29", "Approval", 35, "Tern Systems — incident room", "Mara; Theo; Ruth", "Mara opens the review record and reads her approval; Theo holds the notebook still; Ruth listens.", "PR approval timestamp and retry fixture.", "Both facts fit.", "Room tone and breathing; no score.", "No blame close-up on Theo; shared contribution remains visible."),
    ("30", "Lower Bound", 45, "Tern Systems — incident room", "Anika; Daniel; Mara", "Anika sorts receipt records into verified, duplicate, and unresolved columns; Daniel deletes a minimizing word from the statement.", "At least 63 duplicate work orders; 19 events unconfirmed; export incomplete.", "We can say we have not finished counting.", "Paper/keyboard, office HVAC.", "Counts are provisional lower bounds; no names or customer PII."),
    ("31", "Hold Path", 45, "Tern Systems — incident room", "Sam; Mara; Ruth; Anika; Theo", "Sam draws ingress, hold, and dispatch, crosses out the outbound line, and reads flag scope aloud.", "Ingress remains durable; publisher stops; raw archive is append-only.", "The alternative is sending a second crew.", "Marker on glass, subdued room bed.", "Hold flag is separate from Signal Assist summary flag."),
    ("32", "Investor Call", 50, "Tern Systems — phone booth", "Daniel", "Daniel listens, looks through the booth glass toward the incident room, gives the incomplete count, and cancels the demo.", "Calendar invite: investor walkthrough 06:00 — canceled.", "We don't have a complete affected count yet.", "Dry phone booth acoustics, quiet office behind glass.", "No other side of call audible; Daniel's tone stays controlled."),
    ("33", "Readback", 45, "Tern Systems — incident room", "Sam; Ruth; Mara; Theo; Anika", "The team reads the containment plan line by line; Ruth approves; Anika checks the audit record; Sam waits for in-flight count.", "Global dispatch.mode=hold; append-only input; audited two-person change.", "Events stay in raw intake.", "Paper incident log, sparse clicks.", "No action is taken until in-flight calls settle and approvals are recorded."),
    ("34", "Publisher at Zero", 25, "Tern Systems — operations nook", "Sam; Mara; Theo", "The in-flight counter falls to zero; Sam and Ruth confirm hold; Sam scales the publisher to zero; Theo verifies a held raw event.", "Outbound request rate 0; new source ID present as held/not dispatched.", "Present. Held. Not dispatched.", "One control confirmation, then room tone.", "Ingress stays on; no dropped queue, no fake instant recovery."),
    ("35", "Manual Truth", 40, "Tern Systems — incident room", "Mara; Anika; Theo", "The three compare a pencil shift sheet, local alarm history, raw event payload, and FieldDesk receipt; one row remains unresolved.", "Reconciliation labels: duplicate / stale location / unresolved.", "Leave it unresolved.", "Paper movement, quiet keyboard, no score.", "Never collapse distinct alarms based on site/minute alone."),
    ("36", "Customer Calls", 30, "Tern Systems — support desk", "Ruth", "Ruth reads a precise notification to one operator, pauses to hear the answer, and writes a callback time.", "Dispatch paused; local procedures authoritative; unresolved IDs to follow.", "I will tell you before that changes.", "Phone codec and normal room tone.", "No falsely warm music; call list redacted."),
    ("37", "Not Yet a Fix", 35, "Tern Systems — engineering floor", "Theo; Mara; Sam", "Theo changes the local test key, Sam pins a migration digest in a sandbox, and Mara adds a concurrent-consumer contract test; nobody merges.", "Same source ID / different delivery IDs => one row/action in test.", "It is evidence, not a production repair.", "Keyboard only on active typing; pre-dawn HVAC.", "Local isolated environment; branch remains frozen."),
    ("38", "Status", 40, "Tern Systems — incident room", "Anika; Daniel; Luz (remote); Ruth", "Anika deletes 'service restored'; Luz speaks from the water room; Daniel publishes the narrower status.", "Ingress up; automatic dispatch paused; reconciliation in progress.", "Tell them what we stopped and what they should do.", "Call codec, subdued keyboard, no alert fanfare.", "Status color amber; no unsupported restoration claim."),
    ("39", "Daylight Handoff", 45, "Tern Systems — engineering floor", "Sam; day-shift reliability lead (remote); Mara", "Sunlight crosses the windows as Sam reads unresolved counts and checkpoints; the next lead repeats them back; Sam closes her laptop.", "Queue high and stable; outbound requests zero; recovery not declared.", "We have a known hold and a list of questions.", "Dawn office bed, remote call, laptop close.", "Only intended wardrobe/lighting transition in overnight shift; continuous handoff."),
    ("40", "Investor Note", 45, "Tern Systems — small conference room", "Mara; Ruth; Daniel", "Daniel deletes the unsupported prevention claim; Mara names the unknown; Ruth edits a short incident note and Daniel sends it.", "Four status fields: what happened, what paused, unknowns, next update.", "We didn't know what it had done.", "Paper movement, daylight room tone.", "No celebratory reaction after send; demo removed from calendar."),
    ("41", "Post-Incident Review", 35, "Tern Systems — review room, ten days later", "Mara; Theo; Sam; Ruth", "Each person adds a decision or missing safeguard to a shared timeline under contributing conditions.", "Review timeline from pull request through customer calls.", "The date was a decision, not weather.", "Open-window traffic, marker on whiteboard.", "Ten-day time jump; ordinary daylight; no blame chart."),
    ("42", "The Bridge", 45, "School hallway, ten days later", "Mara; Mateo", "Mara arrives at Mateo's display, waits for him to turn, listens while he points to the strip of tape and bowed span.", "Paper bridge and stack of books; no overlays.", "I was wrong to say it before I knew.", "School hallway ambience, distant children low in mix.", "Bridge bends under final book; emotionally restrained."),
    ("43", "Operator Confirmed", 30, "Morrow County Water — control room, three weeks later", "Luz; night operator (offscreen)", "Luz checks the local panel, reads the work order, presses operator-confirmed, then leaves a second amber row untouched.", "Separate states: RAW EVENT RECEIVED / WORK ORDER SENT / OPERATOR CONFIRMED.", "That one's still waiting.", "Pump hum, pencil, soft interface sound.", "Same desk geography; local panel remains in shot; second event unresolved."),
    ("44", "Amber", 30, "Tern Systems — engineering floor, night", "Mara", "Mara reads the operator-confirmed row, replies to Mateo, sets the phone down, and keeps watching the unresolved amber event.", "AUTOMATION: LIMITED — HUMAN CONFIRMATION REQUIRED.", "I'll tell you before you wait.", "Office room tone; no final music swell; hold on real movement.", "Amber remains amber; reflection/window composition; ending is not a declaration of full recovery."),
]

SHOT_TYPES = (
    ("continuous master", "human-scale wide or medium-wide; establish geography and preserve uninterrupted actor movement"),
    ("tracked evidence", "over-shoulder or moving insert; performer manipulates a real prop/interface while the evidence changes"),
    ("reaction/decision", "close or two-shot; preserve breath, eye movement, gesture, and a visible choice or exit"),
)


def tc(total_seconds: int) -> str:
    h, rem = divmod(total_seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}:00"


def shot_lengths(scene_seconds: int) -> list[int]:
    q, r = divmod(scene_seconds, 3)
    return [q + (1 if i < r else 0) for i in range(3)]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if len(SCENES) != 44:
        raise SystemExit(f"Expected 44 scenes, found {len(SCENES)}")
    runtime = sum(s[2] for s in SCENES)
    if runtime != 1800:
        raise SystemExit(f"Scene target durations must sum to 1800, got {runtime}")

    scene_fields = [
        "scene_id", "scene_title", "target_duration_sec", "target_start_tc",
        "target_end_tc", "location", "characters", "story_action",
        "screen_or_physical_evidence", "key_dialogue", "production_sound",
        "continuity_lock", "production_status",
    ]
    scene_rows: list[dict] = []
    shot_rows: list[dict] = []
    scene_start = 0
    for record in SCENES:
        sid, title, duration, location, cast, action, evidence, line, sound, continuity = record
        scene_end = scene_start + duration
        scene_rows.append({
            "scene_id": sid,
            "scene_title": title,
            "target_duration_sec": duration,
            "target_start_tc": tc(scene_start),
            "target_end_tc": tc(scene_end),
            "location": location,
            "characters": cast,
            "story_action": action,
            "screen_or_physical_evidence": evidence,
            "key_dialogue": line,
            "production_sound": sound,
            "continuity_lock": continuity,
            "production_status": "PLANNED — NOT PRODUCED",
        })
        lengths = shot_lengths(duration)
        shot_start = scene_start
        for index, ((function, framing), shot_duration) in enumerate(zip(SHOT_TYPES, lengths), start=1):
            shot_end = shot_start + shot_duration
            if index == 1:
                movement = f"Continuous master: {action} Camera: {framing}; motivated, controlled movement; keep at least one performer physically moving."
            elif index == 2:
                movement = f"{function}: follow the performer interacting with the evidence/prop: {evidence} Camera: {framing}; screen content changes in time with the action."
            else:
                movement = f"{function}: track the performer's live decision/reaction around: {line} Camera: {framing}; hold on visible breathing, gaze shift, hand movement, or purposeful exit—never a frozen portrait."
            shot_rows.append({
                "scene_id": sid,
                "shot_id": f"S{sid}-{index:02d}",
                "scene_title": title,
                "target_duration_sec": shot_duration,
                "target_start_tc": tc(shot_start),
                "target_end_tc": tc(shot_end),
                "location": location,
                "characters": cast,
                "shot_function": function,
                "camera_and_performance_plan": movement,
                "screen_or_physical_evidence": evidence,
                "dialogue_reference": line,
                "sound_requirements": sound,
                "continuity_requirements": continuity,
                "production_status": "NOT PRODUCED — planned shot only",
            })
            shot_start = shot_end
        if shot_start != scene_end:
            raise SystemExit(f"Shot timing mismatch in scene {sid}")
        scene_start = scene_end

    shot_fields = [
        "scene_id", "shot_id", "scene_title", "target_duration_sec",
        "target_start_tc", "target_end_tc", "location", "characters",
        "shot_function", "camera_and_performance_plan",
        "screen_or_physical_evidence", "dialogue_reference",
        "sound_requirements", "continuity_requirements", "production_status",
    ]
    write_csv(OUT / "scene_manifest.csv", scene_rows, scene_fields)
    write_csv(OUT / "shot_manifest.csv", shot_rows, shot_fields)
    if len(shot_rows) != 132 or scene_start != 1800:
        raise SystemExit("Manifest totals failed validation")
    print(f"Wrote {len(scene_rows)} planned scenes and {len(shot_rows)} planned shots; target {scene_start}s (30:00). No media generated.")


if __name__ == "__main__":
    main()
