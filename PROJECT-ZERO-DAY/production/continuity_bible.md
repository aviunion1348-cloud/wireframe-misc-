# Continuity Bible — PROJECT ZERO-DAY: THE LAST DEPLOY

**Version:** 1.0, paired with `screenplay/Screenplay_v1.md`<br>
**Status:** text-only reference. No photographic character/location references or recorded performances have been produced.

## 1. Logline and dramatic rule

During a high-pressure release at a small infrastructure-software company, an exhausted senior engineer discovers that a green deployment hid duplicated and unconfirmed work orders. A race, a retry-key mistake, a stale migration artifact, and a misleading health probe turn a routine launch into a data-integrity incident. The team must preserve the evidence and tell customers the truth before choosing how to recover.

**Story rule:** the thriller is about imperfect knowledge, not a malicious system. Every key discovery comes from evidence gathered by a character. No miracle fix, omniscient dashboard, hacker antagonist, or instant database repair.

**Operational safety rule:** Relay is a telemetry-to-work-order workflow. It does not operate pumps, valves, power equipment, or safety interlocks. Local instruments, procedures, and people remain the authority. Harm is shown as delayed, duplicate, and uncertain work coordination—not as a spectacular physical disaster.

## 2. Character continuity

All ages, appearance cues, accents, and acting notes below are casting/design targets, not depictions of real people. Keep identity stable across the full production; do not rely on generated image similarity alone if the eventual tool supports references.

### Mara Velez — senior systems engineer, 38
- **Silhouette/costume:** average height, compact build, dark wavy hair usually tied low; charcoal overshirt over a plain rust-colored T-shirt, dark trousers, practical shoes. Same clothing from evening through dawn; sleeves get pushed up after the incident starts. No sudden wardrobe change during the overnight timeline.
- **Behavior:** observant, careful with claims, traces a question to its source before proposing a fix. Fatigue appears as slower blinks and a held breath, not slurred speech. When she realizes she approved the wrong key, she reads the review record instead of looking away.
- **Voice:** low-mid register, direct, short clauses; does not raise her voice to command a room.
- **Motivation/flaw:** wants to build systems that keep their promises, but has mistaken familiarity with the code for verification and accepted a narrow test fixture.
- **Personal continuity:** her son Mateo's message arrives before the release. She does not promise attendance until she knows. She later apologizes without demanding absolution.

### Theo Park — junior engineer, 25
- **Silhouette/costume:** slim, straight black hair, muted green knit and dark jeans; carries a small paper notebook with a blue elastic band. Avoid “hoodie hacker” shorthand.
- **Behavior:** precise and initially cautious; asks which identifier is stable, writes down actual values, builds a safe reproduction from sanitized data, and refuses to guess which event is disposable. Confidence comes from evidence, not sudden genius.
- **Voice:** quiet, measured, concrete; rarely uses metaphor.
- **Motivation/flaw:** wants to be useful and has reused the fixture already trusted by the team. Owns his part without being made the scapegoat.

### Samira “Sam” Okafor — infrastructure/SRE lead, 41
- **Silhouette/costume:** tall, close-cropped hair, navy utility shirt, dark slacks; headset and a tablet with a scuffed corner. Practical rather than tactical styling.
- **Behavior:** turns plans into observable checks, reads back the scope of a change, waits for in-flight counts before pausing a publisher, and hands off incident command with explicit unknowns. Dry humor is rare and small.
- **Voice:** grounded, low, paced; names the thing a metric actually measures.
- **Motivation/flaw:** protects reliability while juggling real infrastructure work. She trusts the green migration job record longer than she should, then follows the digest evidence.

### Ruth Chen — engineering manager, 44
- **Silhouette/costume:** neat white shirt with rolled cuffs, dark trousers, simple watch; hair in a short, stable bob. Coffee cup appears in scenes 3–10 and is forgotten, never inexplicably refilled.
- **Behavior:** translates competing needs into explicit decisions, keeps the incident log, owns the calendar pressure she approved, and stops rollback when the schema check fails.
- **Voice:** clear, restrained; asks for a decision and a named owner rather than issuing theatrical ultimatums.
- **Motivation/flaw:** tries to protect the team and the company, but allowed an unrealistic date to become an engineering input.

### Anika Bhandari — reliability and security specialist, 36
- **Silhouette/costume:** medium height, dark curls pinned back, light-grey cardigan over a black top; joins remotely in scenes 8–10, then remains on the secure incident bridge. No visual “cyber” costume.
- **Behavior:** challenges semantic ambiguity, protects audit evidence, distinguishes a persisted ingress record from a completed business action, and rejects a falsely reassuring status statement.
- **Voice:** calm, exact, often asks one short question that changes the group's focus.
- **Motivation/flaw:** values proof and can sound severe when other people are afraid; she is not an antagonist to product or engineering.

### Daniel Vale — product lead, 39
- **Silhouette/costume:** dark denim shirt, no tie, sleeves rolled once; carries three paper demo cards. He removes the “fully autonomous” phrase in scene 4 and never restores it.
- **Behavior:** understands the investor window and payroll pressure, but changes the demo claim when the human consequence becomes clear. He discloses the incident rather than bargaining for a quiet fix.
- **Voice:** conversational and persuasive, with pauses when he recognizes his own euphemism.
- **Motivation/flaw:** wants the company to survive and initially thinks of the demo as a single, coherent product switch.

### Luz Ortega — Morrow County Water operations supervisor, late 40s
- **Silhouette/costume:** work jacket over a pale-blue uniform shirt, reading glasses on a cord, pencil tucked behind one ear. Same room, light, jacket, and shift sheet in scenes 1, 9, 19, 25, 43.
- **Behavior:** checks local instruments, radios the on-site operator, keeps a pencil record, and asks for the status she can act on. She never panics or waits passively for the platform.
- **Voice:** clear, slightly dry, comfortable with silence; uses operational language rather than software terminology.
- **Motivation:** protect the crew's time and the integrity of the handoff. She is a customer with agency, not a plot device or a technical novice.

### Mateo — Mara's son, 10
- **On-screen time:** voice message, school hallway in scene 42, and text only. His bridge is a small paper-and-tape project, not an allegory highlighted by music.
- **Behavior/voice:** matter-of-fact, observant; he can say he was disappointed without resolving Mara's work conflict for her.
- **Continuity:** the bridge remains on the display in scene 42 with a strip of tape and a small bend; no extra sentimental insert is required.

## 3. Locations and geography

### Tern Systems engineering floor
One open office with a glass meeting room on the left side of the main aisle, operations nook at the north wall, and incident table near the windows. Establish this geography in a stable wide shot before using close-ups. For office conversations, keep Mara generally screen-left facing screen-right toward the shared display; Sam's operational station remains screen-right. Do not reverse the axis without a motivated establishing move.

Practical sources: ceiling fixtures, laptop/monitor spill, dawn through windows. Monitor light may lift eyes and hands, but never replace all room illumination. The floor is active but not packed with anonymous typing extras.

### Morrow County Water control room
A working municipal control space: fluorescent fixtures, laminated process diagram, local panel visible beyond the operations desk, pencil shift sheet, telephone, radio. The Relay screen is secondary to physical readouts. Keep the pump vibration low and physically motivated; do not add alarms absent from the script.

Luz occupies the desk nearest the local panel. The phone is to her right; the pencil sheet lies left of the keyboard. Maintain this layout in every return visit.

### Apartment and school hallway
The apartment is only a threshold glimpse: counter, lunch bag, clock, laptop. Do not add a long domestic subplot. The school hallway in scene 42 is warm, ordinary, and quiet, with real ambient children offscreen but no sentimental montage.

### Phone booth / test room
The phone booth is small and acoustically dry. The test room contains a sanitized local environment, not a production database or a magical live mirror. Make clear through labels and dialogue that the reproduction is isolated.

## 4. System and interface canon

### Fictional product and components
- **Company:** Tern Systems.
- **Product:** Relay.
- **External work-order API:** FieldDesk (fictional).
- **Input fields:** `tenant_id`, `site_id`, stable `source_event_id`, and per-attempt `delivery_id`.
- **Services:** `relay-ingest`, an at-least-once queue, `correlator`, an append-only raw-event archive, Postgres primary plus asynchronous read replica, and a downstream action publisher.
- **No physical control plane:** Relay does not send actuator commands. It helps a human route and verify work orders.

### The bug, precisely
1. A refactor uses the per-attempt `delivery_id` to form the downstream idempotency key. Provider retries may have a new delivery ID for the same stable source event, so the downstream system sees a new action.
2. The consumer does a read-before-write duplicate check through an asynchronous replica, then inserts on the primary. Two consumers can see “no row” at once. The code has no atomic upsert/lock for the invariant.
3. The intended unique index on `(tenant_id, source_event_id)` is migration 215. The migration workload resolves a mutable `:release` tag to an older bundle; that job completes migration 214 and reports its own bundle current, but never creates migration 215's index.
4. The same stale bundle executes the pending contract step 214 and drops `legacy_event_key`. The deployed code has moved forward; the normal 4.17 rollback target still queries the removed field and fails with `SQLSTATE 42703`.
5. FieldDesk sometimes commits a request after Relay's two-second client timeout. At-least-once queue redelivery retries it; a fresh per-delivery key defeats downstream deduplication.
6. `/readyz` checks process/database/broker connectivity, not a full event-to-work-order transaction. The ingress API returns quickly after durable broker acceptance, so ingress latency can be green while the action queue grows.

No single item explains the outage. The coupling of assumptions, deployment artifacts, retry semantics, schema compatibility, and lagging observations does.

### Interface grammar and screen text
- Ingress **ACCEPTED** means the raw event was persisted/enqueued. It must never be shown as proof that a work order exists.
- A complete customer-facing flow has separately visible states: **RAW EVENT RECEIVED**, **WORK ORDER SENT**, **OPERATOR CONFIRMED**.
- `source_event_id` remains stable across provider retries. `delivery_id` changes per attempt. Show both together in investigation shots; do not substitute one label for the other.
- Use invented tenant/site IDs, redacted payloads, and no credentials. Avoid green-on-black terminal wallpaper and unreadable walls of fake code.
- Useful, legible evidence: queue age/depth, ingress p99, downstream timeout, replica replay lag, migration version, resolved container digest, unique-index catalog, and FieldDesk receipt time.
- Dashboard design must distinguish service liveness from business completion. A `200 /readyz` can coexist with unconfirmed work orders without the film treating that as a contradiction.

### Incident recovery canon
The team does not “fix” the issue by restarting pods or deleting rows. It drains in-flight side effects, moves the global action mode to `hold`, keeps durable raw intake, preserves the append-only event stream, reconciles against local/customer records and FieldDesk receipts, and leaves uncertain items explicitly unresolved. Any later repair is tested in isolation with a pinned migration image, stable source identity, unique constraint, safe transactional outbox, and concurrent retry tests before promotion. The completed feature remains limited until a full end-to-end validation exists.

## 5. Timeline and continuity locks

- Scene 1 is approximately 01:14 UTC, the incident already visible at a customer site.
- Scene 2 cuts back to approximately seven hours earlier; the release occurs that evening, and the investor walkthrough is scheduled for 06:00.
- The 25% canary has only a handful of receipt-matched events and no observed provider redelivery. The migration job appears green, but there is no live source-to-receipt detector. Ruth approves a full rollout to 2,140 tenants while requiring manual batch checks; the later queue backlog is therefore broad, not limited to the canary.
- The overnight sequence proceeds toward dawn. Do not change the order of scene 1's customer evidence, the later release setup, the incident response, and the final three-weeks-later customer confirmation.
- The night is one continuous shift for Mara, Theo, Sam, Ruth, Anika, and Daniel. Fatigue grows gradually; faces, hair, clothing, eyewear, and props do not reset between scenes.
- The 44 target scene durations total exactly 1,800 seconds. This is a timing plan only; actual performed timing must be reviewed and re-edited.
- The post-incident review occurs ten days later. Luz's scene 43 takes place three weeks later. These time jumps require restrained inserts and clear scene headings, not an unexplained color or wardrobe shift.

## 6. Camera, aspect, light, and color progression

### Capture/frame policy
Compose for a 2.39:1 image safely inside UHD 16:9, with important eyes, hands, and critical interface evidence inside the delivery-safe area. Delivery resolution is not permission to crop unreadable text. Any monitor replacement must preserve screen perspective, moiré behavior, reflections, and exposure.

### Visual progression
- **Opening and pre-release:** stable wide masters, measured dolly/tracking only when following a person with purpose; neutral white office light and natural skin tones.
- **Canary:** medium over-shoulder frames and patient inserts. Let one real event complete; do not montage unrelated typing.
- **Incident:** frame progressively tighter; introduce selective handheld movement when the room reorganizes, not on every line. Keep geography and eyelines clear. Use focus pulls only to transfer attention between an actor and relevant evidence.
- **Containment:** camera movement becomes stable again as the team makes a decision; stillness is a choice, not a frozen image.
- **Ending:** balanced daylight / practical lighting and an honest amber interface. No sudden triumphant grade, artificial blue-purple neon, heavy grain, or glitch transitions.

Skin tone, contrast, monitor brightness, and fluorescent color must remain coherent from shot to shot. Never use a color shift to imply an invented technical state.

## 7. Sound and music continuity

- Office bed: restrained HVAC, distant chair movement, occasional ordinary conversation. Use keyboard/mouse sounds only when the action calls for them.
- Water-room bed: low pump vibration, fluorescent room tone, radio/phone texture, local alarm only when shown.
- Computer audio: minimal, distinctive, spatially placed alerts. No constant beeps. A “green” status has no victory sting.
- Incident: let the FieldDesk timeout, page, and delayed queue become legible through rhythm and selective silence; do not make fan noise physically “speed up” because a graph rose.
- Dialogue: natural overlap only in planned group beats; preserve pauses, breath, and room acoustics. All production dialogue and lip sync remain unproduced.
- Score target: original, restrained, and sparse. No commercial/copyrighted music chosen. Primary tension comes from room tone, pace, and withheld certainty. Silence around the duplicate-key discovery and the final amber state should remain audible.
- Mix target for future production: dialogue intelligible, stable center image, controlled alert peaks, no crushed dynamics; stereo minimum and separate 5.1 only if a real multichannel mix is produced and checked.

## 8. Performance and editorial safeguards

- The actors are doing a job, not “acting like programmers.” Hands, gestures, and gaze should correspond to the investigation and interface.
- No repeated typing montage, random terminal commands, arbitrary face inserts, fake system-code overlays, or “genius reveal” shot.
- Every technical conclusion must be preceded by evidence in frame or audible dialogue. The audience should understand the human stakes even if it does not read every identifier.
- Keep the strongest moral beats quiet: Luz's distinction between accepted and acted upon; Mara reading her own approval; the unresolved row; the honest public status; Mateo's disappointment; the amber close.
- Never cut from duplicate work orders to a fabricated physical catastrophe. The scale is communicated through human coordination, uncertainty, and the work still waiting.

## 9. Asset/continuity status

No reference portraits, location photographs, video, motion tests, recorded voices, screen composites, music, or licensed third-party assets are included. The textual specifications above are the continuity reference until actual approved performers, locations, and audiovisual assets exist. A future production should attach performer-approved reference frames and identify source/version/license for each production asset before shooting or rendering.
