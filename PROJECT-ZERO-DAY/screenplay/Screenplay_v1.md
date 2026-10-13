# PROJECT ZERO-DAY: THE LAST DEPLOY

**A fictional technology thriller**<br>
**Screenplay v1.0 — complete beginning-to-end draft**<br>
**Target picture runtime: 30:00 (44 scenes; credits excluded)**<br>
**Estimated spoken dialogue:** approximately 2,450 words; the draft favors visual evidence and deliberate pauses over filler. Re-time after a table read.<br>
**Format:** 2.39:1 composition inside a 3840 × 2160 UHD frame; 24 fps<br>

> Production status: screenplay and preproduction documents only. No footage, performances, dialogue recording, music, mix, render, or playable film have been produced in this environment. Scene durations below are editorial targets, not measured media durations.

## FADE IN:

### 1. INT. MORROW COUNTY WATER — CONTROL ROOM — NIGHT (00:45)

A room built to be cleaned, not admired. Fluorescent tubes. A laminated process diagram behind a row of monitors. A pump vibrates somewhere below the floor.

LUZ ORTEGA, late forties, listens to the building before she looks at the screen. A local pressure gauge trembles just outside its green band. Her hand reaches for the radio.

On a monitor: **RELAY — EVENT ACCEPTED — 01:14:36Z**. Below it, **WORK ORDER: —**. The status tile is green.

Luz refreshes once. Nothing changes.

**LUZ**<br>
Control to night operator. South Intake, pump two. Check the local panel and call me back. Don't wait on the board.

She lifts a desk phone, dials from a number written beside it. No panic. This is a practiced second path.

A thin alert chime sounds from the monitor. It is almost polite.

**LUZ**<br>
(into phone)<br>
Relay took the event. It did not take the action.

She watches the green tile as she listens. The pump's low vibration continues, steady but newly audible.

**CUT TO BLACK.**

### 2. INT. MARA'S APARTMENT — KITCHEN — EVENING, SEVEN HOURS EARLIER (00:35)

A phone plays a voice message while MARA VELEZ, 38, packs a paper lunch bag. Her son MATEO, ten, talks over the sound of a school hallway.

**MATEO (V.O.)**<br>
The bridge held the big book. I moved the weight, though. You said you might come see it before I take it apart.

**MATEO (V.O.)**<br>
You said that last week, too.

Mara looks at the clock, then at her laptop. A deployment window is marked in a calendar invitation: **RELAY 4.18 — INVESTOR WALKTHROUGH 06:00**.

She records a reply, deletes it, records again.

**MARA**<br>
I heard you. I want to see it. I'll call when I know the morning for sure.

She doesn't say she'll be there. The lunch bag stays on the counter. She takes her keys.

### 3. INT. TERN SYSTEMS — ENGINEERING FLOOR — EVENING (00:40)

A wide, composed view: ordinary desks, a glass meeting room, jackets on chair backs. No neon. A cleaning cart rolls quietly behind the last row.

Mara enters. THEO PARK, 25, has a paper notebook open beside a laptop. SAMIRA “SAM” OKAFOR, 41, is on a headset, watching a deployment panel. RUTH CHEN, 44, pours coffee she has forgotten to drink.

The wall display shows **RELAY: 99.97% UPTIME**. The number is a rolling month, not a promise about tonight.

**THEO**<br>
Build finished. The summary says all checks passed.

**SAM**<br>
Did the external dispatch check run?

**THEO**<br>
No. The sandbox integration was skipped. The unit test used a fake receiver.

**MARA**<br>
Then the green line tells us what we checked, not what we didn't.

**MARA**<br>
That is what a summary is for.

**SAM**<br>
And the raw run?

Theo turns the laptop so they can all see the CI job graph. Every required check is green. One optional integration test is grey: **SKIPPED — EXTERNAL DISPATCH SANDBOX UNAVAILABLE**.

Nobody comments yet.

### 4. INT. TERN SYSTEMS — GLASS MEETING ROOM — EVENING (00:50)

DANIEL VALE, 39, product lead, lines up three paper cards for the morning demo: **INGEST**, **CORRELATE**, **DISPATCH**. He has crossed out a slide that said “fully autonomous.”

**DANIEL**<br>
It is a working-capital demo, not a product launch. If we miss the window, the bridge round moves. That's payroll, not a yacht.

**RUTH**<br>
I know. The date is real. The staffing plan is also real.

**DANIEL**<br>
I asked for a screen the county can recognize. One incident instead of twelve copies. An operator still decides what to do.

**MARA**<br>
The summary is behind a flag. The normalizer isn't.

A beat. Daniel looks at the card marked **CORRELATE**.

**DANIEL**<br>
I thought the release was one switch.

**RUTH**<br>
The demo is a window. It is not a staffing plan.

**DANIEL**<br>
I know. The pilot renewal takes months. I asked for an early proof, not a pretend one.

**RUTH**<br>
So did the demo deck.

Daniel takes the card off the table. He doesn't defend the deck.

### 5. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:45)

Over Mara's shoulder: a pull request titled **RELAY-418: stable source identity + Signal Assist summaries**. The commit graph shows a feature branch, a rebase, one resolved conflict in `event-normalizer.ts`, then Ruth's approval. A small assistant summary reads **“Implementation complete: retry-safe idempotency helper; tests added.”** Beneath it: **“Human review required.”** Mara has edited and reviewed the helper.

The diff is neat. One line forms the downstream key from `context.deliveryId`.

**RUTH**<br>
The review says stable source identity. Is `deliveryId` the canonical ID after normalization?

**MARA**<br>
That's what the adapter wrapper calls it. I read it as the provider event identity.

Theo opens the unit fixture. Both fields contain `alarm-77`.

**THEO**<br>
This test uses the same value for both.

**MARA**<br>
Then it can't tell us whether the mapper is doing what I think it is.

**RUTH**<br>
Can we verify before the release?

Mara checks the external-test status: **SKIPPED — SANDBOX UNAVAILABLE**.

**MARA**<br>
We can keep the canary narrow and compare the actual receipt trail. If it doesn't reconcile, we stop.

### 6. INT. TERN SYSTEMS — ENGINEERING FLOOR — CONTINUOUS (00:40)

Theo opens the retry test. It times out a downstream request, then redelivers the same queued message. Both attempts carry the same delivery context, so FieldDesk sees the same key and returns one work order.

**THEO**<br>
This proves the worker can replay a message without duplicating an action.

**MARA**<br>
Good. That's the retry we see most often.

**THEO**<br>
The provider can resend the webhook too. That's a different boundary.

Mara scans the test name, then the skipped sandbox check. She does not open the provider contract.

**MARA**<br>
Right. The canary receipt comparison has to cover that gap as far as production traffic allows.

**THEO**<br>
One clean sample won't prove it.

**MARA**<br>
No. It can tell us to stop. It cannot tell us everything is safe.

He adds the limitation to the review note. The release remains a decision, not a certainty.

### 7. INT. TERN SYSTEMS — ENGINEERING FLOOR — LATER (00:50)

The additional worker-retry test runs. It passes with the same event object on both attempts. CI is green. The provider-redelivery test remains skipped because its sandbox is unavailable.

Sam joins the review with a tablet showing the deployment plan.

**SAM**<br>
The app is pinned by digest. The migration job is still on the release tag.

**MARA**<br>
Is that the same migration bundle we tested?

**SAM**<br>
The dashboard says the schema job is green. I'll check the job record before the window.

She adds a note to her tablet. The call waiting on her headset flashes; a regional node is already draining for routine maintenance.

**RUTH**<br>
Can the index wait for the next window?

**SAM**<br>
If the code is relying on it, no. If the code is not relying on it, I want to know why it is in the migration.

The question hangs there. Nobody answers it from memory.

### 8. INT. TERN SYSTEMS — SMALL CONFERENCE ROOM — NIGHT (00:35)

Anika BHANDARI, 36, reliability and security specialist, joins on a wall screen from another site. She has a runbook open, not a dashboard.

**ANIKA**<br>
What does “accepted” mean on the customer screen?

**MARA**<br>
Persisted at ingress. It does not mean a work order exists.

**ANIKA**<br>
Can the operator tell those apart without opening the trace?

Mara considers the current UI. She knows the answer.

**MARA**<br>
Not on the summary card.

**ANIKA**<br>
Then the label needs to say exactly what completed. A persisted event is not a dispatched crew.

**ANIKA**<br>
Until it changes, use the trace and the receipt.

Ruth marks the note in the runbook. Daniel, passing outside the glass, sees the meeting and waits rather than entering.

### 9. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:55)

A video call connects to Luz in the Morrow County control room. We see the same fluorescent light and laminated diagram from the opening, now in a quiet pre-incident hour.

**LUZ**<br>
We don't use Relay to run pumps. Our local controls and people do that. Relay is how the overnight crew sees which calls are waiting. If it says “accepted,” my people hear “someone is on it.”

**DANIEL**<br>
The new view groups repeat alarms. It should cut the duplicates.

**LUZ**<br>
Good. Keep the original alarm attached. My operator needs to know whether two readings were one noisy sensor or two different things.

**MARA**<br>
They will be. The raw event remains in the audit stream.

Luz holds Mara's eye through the camera.

**LUZ**<br>
Then show me where I can find it when the summary is wrong.

**MARA**<br>
The raw record is two clicks down. I'll put its ID beside the summary before we widen.

Mara writes that down.

### 10. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:55)

The go/no-go call. Ruth reads the checklist; Sam watches the cluster; Mara keeps the pull request open. Anika is on the wall screen. Daniel stands back from the table.

**RUTH**<br>
Five percent. We don't widen until source events match created work orders.

**SAM**<br>
We can't compare that on one dashboard.

**RUTH**<br>
Then we reconcile sampled IDs to FieldDesk receipts. If the count is unclear, we stop.

**MARA**<br>
The retry test passed locally. We never hit the real FieldDesk contract.

**DANIEL**<br>
If you say hold, I cancel the demo and explain why. I won't ask you to mislabel a check.

Ruth studies the team. She can stop the release, but the new retry test is green and the migration job reported success.

**RUTH**<br>
Proceed at five. Sam owns stop; we inspect receipts before widening.

**SAM**<br>
At five percent, I want the source IDs beside the partner receipts. If they don't line up, we stop there.

**ANIKA**<br>
Uncertainty is a stop condition.

### 11. INT. TERN SYSTEMS — OPERATIONS NOOK — NIGHT (00:30)

Sam starts the canary from the approved release panel. No improvised shell command, no dramatic countdown. A signed artifact digest appears beside the new pods.

The Kubernetes view shows two new `relay-ingest` pods ready, then one old pod draining. The request rate is low and ordinary.

**SAM**<br>
Five percent. No restart loop. Broker connections stable.

**MARA**<br>
Reviewed digest matches the commit.

**SAM**<br>
Good. Now we wait for an actual event, not a pod turning green.

She waits for the first real customer transaction, not the readiness probe.

Mara keeps one hand near the notebook. Theo watches a trace, not the color of the deployment tile.

### 12. INT. TERN SYSTEMS — OPERATIONS NOOK — CONTINUOUS (00:25)

A green health check: **200 /readyz — postgres: ok — broker: ok**.

Sam expands the probe definition. It tests a database connection and a broker handshake. It does not create an event, correlate it, or verify a downstream work order.

**SAM**<br>
It is alive.

**MARA**<br>
That's all it ever promised.

**SAM**<br>
It keeps a dead pod out of service. It was never meant to certify a customer's workflow.

**MARA**<br>
Then we need a different gate for the workflow.

The dashboard fills the wall. The camera stays on their faces rather than turning the health tile into a hero shot.

### 13. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:40)

A single real maintenance alarm arrives from a low-risk test site. The raw event appears in the archive; a worker creates one FieldDesk work order. No provider retry occurs.

The screen scrolls as Theo follows the trace into the queue. He checks the event count against the one receipt.

**THEO**<br>
One source event. One action. No retry on this delivery.

**MARA**<br>
So the ordinary path is good.

**THEO**<br>
This path is good. We still haven't seen a provider redelivery here.

Mara writes **1 : 1 — SINGLE DELIVERY** in the notebook margin. She leaves space below it.

**MARA**<br>
Keep the limitation with the result. Don't let one clean line become a blanket pass.

A green check appears for the sample only.

### 14. INT. TERN SYSTEMS — OPERATIONS NOOK — NIGHT (00:20)

A close insert of a FieldDesk response: `202 Accepted`. The number of work orders created by the canary matches the small sample.

Sam moves the cursor to the promotion control, then stops.

**SAM**<br>
That's a receipt, not a reconciliation.

**RUTH**<br>
Leave the canary narrow until the partner export catches up.

She leaves the canary at five percent. The room is quiet enough to hear the ventilation.

### 15. INT. TERN SYSTEMS — ENGINEERING FLOOR — LATER (00:35)

Ruth and Sam compare the sampled `source_event_id` list with FieldDesk's receipt export. The sample matches. The new retry test still passes.

**RUTH**<br>
No mismatch in the sample. No p99 change. Queue lag is flat.

**SAM**<br>
Widen to twenty-five. Keep the hold switch armed.

Mara watches a slow-moving line chart. The line is still ordinary.

**MARA**<br>
Twenty-five. Another receipt check before full.

**SAM**<br>
Ten minutes of stable receipts before one hundred. We keep the stop switch armed.

Sam promotes to twenty-five percent. The new pods take traffic without a visible interruption.

### 16. INT. TERN SYSTEMS — GLASS MEETING ROOM — NIGHT (01:00)

Twenty-five percent has run for ten minutes. The sampled source IDs match FieldDesk receipts; none of those events was redelivered by the provider. Queue lag is flat. Sam and Ruth read the limits of that evidence before touching the rollout.

**SAM**<br>
No mismatch in the five receipts we saw. The export is three minutes behind.

**MARA**<br>
And none was provider-retried.

**RUTH**<br>
I know. We can't run mixed versions all night. Move to full, keep the hold switch armed, and inspect each partner batch. Stop if the count or export age breaks.

**SAM**<br>
There's no live mismatch detector.

Ruth lets that land. She looks to Mara, then back to the dashboard.

**RUTH**<br>
Then no auto-green. We call the gate by hand.

Sam changes the deployment from twenty-five to one hundred percent. The `relay-ingest` pods settle without a restart.

Daniel rehearses the investor demo with a sanitized sample feed. A work order appears once. He removes a phrase from his notes: **AI DOES IT FOR YOU**.

**DANIEL**<br>
“Relay groups related events for the operator. We show the source record.”

**ANIKA**<br>
Say the summary can be wrong.

**DANIEL**<br>
And the operator decides.

**ANIKA**<br>
They shouldn't have to reconstruct a missing receipt.

**MARA**<br>
The evidence should be on the same screen.

Daniel looks at the deck, not at her.

**DANIEL**<br>
Then that's the fix we make next week.

He hears himself. He doesn't pretend the sentence is good.

### 17. INT. TERN SYSTEMS — OPERATIONS NOOK — NIGHT (00:30)

A vendor latency graph rises from a quiet baseline. FieldDesk's p99 crosses two seconds. The circuit breaker has not opened; the downstream API is still returning successful responses, only late.

Sam sees the slope and taps the alert threshold. It is set to page after five minutes above the limit.

**SAM**<br>
They are slow, not down.

**THEO**<br>
Our client timeout is two seconds. Their response can arrive after it; that tells us nothing about what they committed.

**SAM**<br>
Then we watch the receipts, not just the response code.

She does not yet know some receipts are missing from the ingest dashboard.

### 18. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:40)

The queue-depth chart ticks upward by hundreds. Ingress p99 remains low because the API acknowledges after writing to the broker. A small label shows **RELEASE TARGETS: 2,140 / 2,140 TENANTS**.

Mara compares `accepted_count` with `action_completed_count`. The second metric updates on a delayed aggregation job. The panel says **DATA DELAY: 180 SEC** in small grey type.

**MARA**<br>
This is why the chart is late.

**THEO**<br>
The queue is growing faster than the delayed count can catch up.

**MARA**<br>
The chart is three minutes behind. We don't have a current success count to justify widening.

Ruth asks Sam for the operator-side result. Sam opens the partner portal, where response logs are also delayed.

**RUTH**<br>
We're already at full. Freeze further changes; we need the receipt export before we touch the dispatch path.

### 19. INT. MORROW COUNTY WATER — CONTROL ROOM — NIGHT (00:45)

Back at the opening location. The local alarm changes from intermittent to steady. Luz uses a second monitor to check the physical system. No failure has occurred; an operator is present and following the site procedure.

Relay shows **ACCEPTED** and **NO ASSIGNEE**. Another event from the same site appears with a later timestamp. Luz notices the changed reading but has no source-to-delivery trace on this screen.

She calls the night operator again.

**LUZ**<br>
Don't acknowledge it in Relay. Read the instrument. Tell me the value from the local panel.

**LUZ**<br>
If the radio drops, call the desk phone. We stay on the county procedure until a person confirms the handoff.

The answer comes through the radio, indistinct. Luz writes it on the laminated shift sheet with a pencil.

### 20. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:45)

The incident alert lands. The queue crosses the paging threshold. Sam stands, not loudly, and opens the incident channel.

**SAM**<br>
SEV-1. Data integrity and delayed dispatch. We do not control equipment, but people use these records to route crews. I'll command. Mara owns event flow. Anika owns customer and audit scope. Theo, preserve examples; don't reprocess anything.

**RUTH**<br>
I'm freezing new deployments and keeping the incident log and customer line current.

Daniel closes the demo laptop.

**DANIEL**<br>
I'll tell the investor we are not ready.

No one thanks him. The room is already moving.

### 21. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:50)

A restrained, slightly handheld move follows Sam from the wall monitor to the table. The dashboard still reads **99.97% AVAILABLE**. Ingress p99 is 94 milliseconds.

**SAM**<br>
That is API availability, not end-to-end success.

**ANIKA**<br>
Put the time window beside that number. The monthly uptime hides the hour we're in.

**MARA**<br>
And acceptance is upstream of the work-order write.

She opens the queue panel: oldest message 6 minutes 12 seconds. `action_completed` is stale. The database connection pool is at 94 percent. A log line shows `SQLSTATE 23505` on the separate active-episode constraint; a worker has scheduled a retry.

**THEO**<br>
Two workers tried to open the same site episode.

**SAM**<br>
That explains a database conflict. It doesn't explain the partner receipts.

**MARA**<br>
Keep those as two hypotheses.

**MARA**<br>
The process is alive. The workflow isn't caught up.

**ANIKA**<br>
Don't call it a health check in the customer statement.

Ruth puts a paper incident log beside the keyboard and begins writing actual times.

### 22. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:50)

Mara pulls up a distributed trace. The ingress span ends with `202`; a later span in the worker shows `POST /v2/workorders` waiting 2,000 milliseconds, then `ReadTimeout`.

Anika opens FieldDesk's receipt export. The vendor committed the work order 1.7 seconds after the client's timeout.

**MARA**<br>
We timed out after they wrote it.

**ANIKA**<br>
And the retry used what key?

**ANIKA**<br>
A timeout is an unknown result. We must not translate it into “failed” and blindly repeat the side effect.

Mara scans the trace. A `delivery_id` appears in the header where a source identity should be.

**MARA**<br>
A new key for a new delivery. So the receiver sees two requests.

A small quiet interval. The sound of the ventilation comes forward.

### 23. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:40)

Theo lays two redacted trace views side by side. Same `source_event_id`. Different `delivery_id`. Two rows in the event table. A third is still in the broker.

**THEO**<br>
The provider didn't send three alarms. It sent one alarm three times.

**RUTH**<br>
Can the timestamps prove the measurements were identical?

**THEO**<br>
Not all of them. One retry carried a later value. We preserve each payload until the provider confirms the relationship.

**RUTH**<br>
Can we delete the extra rows?

**THEO**<br>
Not from this screen. One of the repeats may have carried a changed measurement. We need the original payload and the provider's timestamp.

Mara looks at the append-only archive. It is intact, but slower to query than the customer summary.

**MARA**<br>
Then we don't guess at duplicates by site and minute.

### 24. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:45)

Sam checks replication metrics on the database view. The read replica is 4.8 seconds behind the primary. She opens the deployed migration job's full record for the first time.

The image label ends in `:release`; the resolved digest belongs to the older 4.17 migration bundle. The job completed migration 214 and reports “schema current.” The expected 215 index is absent.

**SAM**<br>
This tag moved. The node reused the old image.

**RUTH**<br>
The job was green.

**SAM**<br>
It ran. It did not run the bundle we reviewed.

**RUTH**<br>
The job can be green and still be too old to know about 215.

**SAM**<br>
Exactly. It checked its own migration list, not the release manifest's expected schema.

She queries the primary index catalog. `uq_source_event_identity` is not there. A row in the migration log shows 214; the release manifest expected 215.

### 25. INT. MORROW COUNTY WATER — CONTROL ROOM — NIGHT (00:55)

Luz joins the incident call but keeps one hand on the local radio. The camera does not cut away from her when the engineers speak.

**LUZ**<br>
I have one alarm on the plant panel and two open jobs in your partner portal. One crew was dispatched to a stale location. The second crew is still available. I need to know which event you trust.

**LUZ**<br>
I'm not asking you to predict the pump. I need to know which notification has a person attached to it.

**MARA**<br>
We don't know yet. The local reading is authoritative. Please use the plant procedure and your call tree. Do not use our green status as confirmation.

**LUZ**<br>
That is the first useful sentence I've heard from the screen all night.

Mara writes it into the incident log exactly as said.

### 26. INT. TERN SYSTEMS — SMALL TEST ROOM — NIGHT (00:45)

Theo builds a controlled reproduction from a sanitized copy. Two consumers pause after the same `SELECT`; a replica snapshot is deliberately held four seconds behind. They resume together.

Both read “no matching source event.” Both attempt an insert. The missing unique index lets both commits through.

**THEO**<br>
The queue is at least once. That's allowed. Our handler made that unsafe.

**MARA**<br>
At-least-once delivery is the contract. Our job is to make a repeat boring. We made it a second action.

**SAM**<br>
The index was the last line of defense. The check wasn't a lock.

**MARA**<br>
And the retry key turned an identical event into a new action before the index ever got a chance.

Theo closes the reproduction. He does not try it against production.

### 27. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:35)

Ruth points at the rollback button in the release console. Mara doesn't touch it.

**RUTH**<br>
If rollback is safe, we take it.

**MARA**<br>
“Last good code” doesn't mean “last compatible schema.” We need to test the actual pair.

**MARA**<br>
The database isn't at the schema the old binary expects. First, check what 214 did.

**RUTH**<br>
And if it is what we think?

**MARA**<br>
Then rollback would replace one visible failure with a silent one.

Ruth removes her hand from the mouse.

### 28. INT. TERN SYSTEMS — INCIDENT ROOM — CONTINUOUS (00:40)

A controlled rollback begins in the staging namespace using the exact production schema snapshot. The old 4.17 pod starts, passes its process probe, then fails its first event query.

On screen: `SQLSTATE 42703: column legacy_event_key does not exist`.

**SAM**<br>
Migration 214 was the contract step. It dropped the field the old app reads.

**ANIKA**<br>
The probe checked a socket. It never executed the old query.

**RUTH**<br>
Then a green rollback check would have lied to us the same way.

**ANIKA**<br>
And the health probe stayed green until a real query.

**RUTH**<br>
Stop the test. No production rollback.

The old pod is taken down. Its brief green status remains in a log, meaningless now.

### 29. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:35)

Mara opens her pull-request review. Her approval is still there, beneath the code. She reads it without scrolling away.

**MARA**<br>
I said “stable” in the review. I didn't verify the provider contract. Then I let one fixture stand in for a retry.

**THEO**<br>
I wrote the fixture.

**MARA**<br>
And I approved it. Both facts fit.

**THEO**<br>
I should have separated the IDs in the fixture.

**MARA**<br>
Yes. And I should have asked what the provider meant by each one.

Ruth sits opposite her.

**RUTH**<br>
We'll put the decisions in the timeline. No one gets made into the whole cause.

Mara closes the PR, not the evidence.

### 30. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:45)

Anika reconciles three sources: immutable raw events, Relay's materialized rows, and FieldDesk's receipt ledger. A spreadsheet fills with statuses, not names.

**ANIKA**<br>
At least sixty-three duplicate work orders. Nineteen source events have no confirmed work order. Those are lower bounds; the delayed vendor export is incomplete.

**DANIEL**<br>
Can we say “intermittent delay” until we know the full count?

**ANIKA**<br>
We can say we have not finished counting. We cannot imply the count is small.

**DANIEL**<br>
Then say “at least,” and name what is still unknown.

**ANIKA**<br>
That is accurate. Keep the next update time on it.

Daniel reads the proposed sentence again. He removes “intermittent.”

### 31. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:45)

Sam sketches three boxes: **INGRESS**, **HOLD**, **DISPATCH**. A pencil line connects them. She crosses out the arrow from HOLD to DISPATCH.

**SAM**<br>
We can keep durable raw intake. We stop the action publisher. Events stay in the broker and archive; nothing leaves for a work order until reconciled.

**RUTH**<br>
The backlog will be visible to customers.

**MARA**<br>
A visible backlog is safer than a completed-looking record that went to the wrong crew.

**RUTH**<br>
The queue will grow. We will miss our morning capacity target.

**MARA**<br>
The alternative is sending a second crew because we can't prove the first one wasn't sent.

Anika asks for the exact flag scope and audit trail. Sam reads them aloud before changing anything.

### 32. INT. TERN SYSTEMS — PHONE BOOTH — NIGHT (00:50)

Daniel steps into the phone booth. We hear only his side of the call, low and controlled.

**DANIEL**<br>
The release is live and the downstream actions are not trustworthy. We've paused them. The old version cannot safely read the migrated schema. No, we don't have a complete affected count yet.

A pause. Daniel listens.

**DANIEL**<br>
The demo is canceled. I'll send the incident note before you send another calendar invite.

A pause. The person on the other end asks whether the release can simply be reverted.

**DANIEL**<br>
Not safely. We tested the rollback against the schema and it failed.

He returns to the floor. There is no triumphant music, only a door latch and distant typing.

### 33. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:45)

The team reads the containment plan line by line. Two-person approval is required for the global `dispatch.mode=hold` flag. Ingress remains on; the raw archive is append-only; the action publisher will drain in-flight requests before stopping.

**SAM**<br>
We wait for the in-flight count to reach zero. Then hold. No restart loop.

**MARA**<br>
What about events that arrive during the drain?

**THEO**<br>
They remain in raw intake. We don't claim they have an action.

**ANIKA**<br>
Record the flag change, approvers, drain count, and the last outbound receipt. We need to know where the boundary was.

Ruth enters her approval. Anika verifies the audit record. Sam waits for the counter.

### 34. INT. TERN SYSTEMS — OPERATIONS NOOK — NIGHT (00:25)

The in-flight count reaches zero. Sam and Ruth confirm the flag. The publisher scales to zero through the approved control plane. The queue depth continues to rise, but the outbound request counter falls to zero.

**SAM**<br>
No new actions leaving.

**MARA**<br>
Raw intake still writing?

Theo checks a fresh event in the archive and reads back its stable source ID.

**THEO**<br>
Present. Held. Not dispatched.

**SAM**<br>
Keep the queue. Do not purge it to make the graph look better.

The room exhales without celebrating.

### 35. INT. TERN SYSTEMS — INCIDENT ROOM — NIGHT (00:40)

Luz's site appears in the reconciliation sheet. One operator's paper shift note, the local alarm history, and FieldDesk's receipt are laid beside the event IDs.

Mara and Anika compare timestamps. Theo reads each identifier aloud. They mark one duplicate, one stale location, and one event that still needs a human call.

**ANIKA**<br>
This row is known. This one is not.

**MARA**<br>
Leave it unresolved.

**ANIKA**<br>
We'll call the site and compare its shift sheet. A blank is still information; a guessed match is not.

**THEO**<br>
It makes the total look worse.

**MARA**<br>
It is worse than a made-up answer.

### 36. INT. TERN SYSTEMS — CUSTOMER SUPPORT DESK — NIGHT (00:30)

Ruth calls a list of affected operators. No mass message pretending to be personal. She reads from a short, specific script and pauses for each answer.

**RUTH**<br>
We have paused automatic work-order dispatch. Your local alarms and call procedures remain the source of truth. We will give you the event IDs we cannot yet reconcile.

A caller asks when it will be fixed. Ruth doesn't fill the silence.

**RUTH**<br>
I don't know yet. I will tell you before that changes.

She listens to the caller's answer instead of filling the gap with another promise.

### 37. INT. TERN SYSTEMS — ENGINEERING FLOOR — PRE-DAWN (00:35)

The release branch remains frozen. In a local test environment, Theo changes the idempotency key to use `source_event_id`; Mara adds a contract test where delivery IDs differ. Sam pins the migration runner to the exact digest and tests a new index migration on a copy.

No one merges the hotfix. It is evidence, not a production repair.

**THEO**<br>
One source ID, two delivery IDs: one row, one action.

**SAM**<br>
Then repeat it concurrently, time out after the test receiver commits, and prove the second request is harmless.

**MARA**<br>
And prove rollback from the exact schema we deploy.

**SAM**<br>
After the index exists.

**MARA**<br>
And after the outbox is atomic. Not before.

She adds the test for two concurrent consumers.

### 38. INT. TERN SYSTEMS — INCIDENT ROOM — PRE-DAWN (00:40)

A new status page is prepared. The first draft says **SERVICE RESTORED**. Anika deletes it.

**ANIKA**<br>
Ingress is up. Automatic dispatch is paused. Reconciliation is in progress. “Restored” is a bigger claim than we can support.

**DANIEL**<br>
Can we give them a time for the next update, even if we don't know the answer yet?

**ANIKA**<br>
Yes. A time we can keep.

**DANIEL**<br>
Will customers read that as failure?

**LUZ (V.O., ON CALL)**<br>
They already know something failed. Tell them what we stopped and what they should do.

Daniel nods and publishes the revised status. The status is amber, not green.

### 39. INT. TERN SYSTEMS — ENGINEERING FLOOR — DAWN (00:45)

Daylight reaches the windows without making the office feel new. A fresh incident log is taped beside the monitor. Queue depth is high and stable; outbound work orders remain at zero.

Sam hands command to the day-shift reliability lead over a call. She reads the unresolved count and the next checkpoint aloud.

**SAM**<br>
We have not declared recovery. We have a known hold, a preserved source stream, and a list of questions.

**DAY-SHIFT RELIABILITY LEAD (V.O.)**<br>
Understood. I have the unresolved count and the next customer checkpoint.

**SAM**<br>
Read it back to me once more.

The day-shift lead repeats the count back. Only then does Sam close her laptop.

### 40. INT. TERN SYSTEMS — SMALL CONFERENCE ROOM — DAWN (00:45)

Mara, Ruth, and Daniel revise the investor note. Daniel removes a sentence claiming the platform “automatically prevents duplicate work.”

**DANIEL**<br>
If I say we paused because we couldn't prove the dispatches, does that sound like we don't know the product?

**RUTH**<br>
It sounds like we know what we do not know. That's a better starting point than a promise.

**MARA**<br>
We didn't know what it had done. That's the product tonight.

Ruth keeps the note short: what happened, what was paused, what remains unknown, when the next update will arrive.

Daniel presses send. The investor meeting is gone from the calendar.

### 41. INT. TERN SYSTEMS — POST-INCIDENT REVIEW ROOM — TEN DAYS LATER (00:35)

A plain room, windows open to traffic. No raised voices. A timeline covers the whiteboard: review, migration, canary, timeout, hold, customer calls.

**RUTH**<br>
The staffing gap and the date were decisions, not weather.

**SAM**<br>
Why didn't the alert catch the duplicate actions?

**ANIKA**<br>
It watched request latency and process availability. We never gave it a source-to-receipt invariant.

**THEO**<br>
And the migration job reported success for its own version, not ours.

**MARA**<br>
I approved a key I had not traced to the provider's stable identity.

**THEO**<br>
I copied the fixture everyone already trusted.

**SAM**<br>
The migration tag was mutable. The job checked itself, not the schema the app needed.

They write each statement under **CONTRIBUTING CONDITIONS**, not under a person's name.

### 42. INT. SCHOOL HALLWAY — AFTERNOON, TEN DAYS LATER (00:45)

Mara stands by a display of student projects. Mateo's bridge is still there, a strip of tape on one side and a stack of books beside it. Mateo watches Mara arrive before he looks back at the bridge.

**MARA**<br>
I missed it.

**MATEO**<br>
You said you would come.

**MARA**<br>
I did.

**MATEO**<br>
The last book made it bend. I had to take it down before it fell.

**MARA**<br>
I did. I was wrong to say it before I knew.

He nods, not quite forgiving and not trying to punish her. He shows her where the bridge bent under the last book.

**MATEO**<br>
This is the part I changed.

Mara looks closely. She gives him her full attention.

### 43. INT. MORROW COUNTY WATER — CONTROL ROOM — NIGHT, THREE WEEKS LATER (00:30)

A new Relay screen has separate labels: **RAW EVENT RECEIVED**, **WORK ORDER SENT**, **OPERATOR CONFIRMED**. No single green tile can stand in for all three.

Luz reads a work order, checks the local panel, and presses **CONFIRM**. The audit trail records her name and time. A second event remains amber pending a call.

**LUZ**<br>
That one's still waiting.

**NIGHT OPERATOR (O.S.)**<br>
I have the local reading. I'll call the crew and leave the row open until they confirm.

**NIGHT OPERATOR (O.S.)**<br>
I see it.

Luz does not clear the amber row.

### 44. INT. TERN SYSTEMS — ENGINEERING FLOOR — NIGHT (00:30)

Mara watches the operator-confirmed row appear in the audit stream. Her phone lights with a message from Mateo: **THURSDAY?**

She types: **Yes. I'll be there. If that changes, I'll tell you before you wait.

She rereads the message once, then sends it. No smile to camera.** She sends it, then puts the phone face down and looks once more at the unresolved amber event.

Across the room, the dashboard reads **AUTOMATION: LIMITED — HUMAN CONFIRMATION REQUIRED**. No music tells us that this is victory.

The monitor reflection shows Mara, still at work, and the dark window behind her. The amber light does not turn green.

**CUT TO BLACK.**

## END

---

### Screenplay continuity note

The system never controls pumps or other physical equipment. Relay ingests telemetry and helps people route work orders. Local alarms, procedures, and operators remain the safety authority. The outage causes delayed and duplicate work-order records, not a magical loss of all safeguards. The final automation remains deliberately limited; exact recovery scope is left for the film's verified production pass to establish from actual performances and timing.
