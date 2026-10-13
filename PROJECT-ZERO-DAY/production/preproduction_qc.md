# Preproduction QC Record

**Check date:** 2026-10-13 UTC<br>
**Scope:** documents and planned timing only. This is not a movie QC pass.

## Automated checks run

Command:

```text
python3 PROJECT-ZERO-DAY/production/build_manifest.py
python3 PROJECT-ZERO-DAY/production/check_preproduction.py
```

Result:

```text
Wrote 44 planned scenes and 132 planned shots; target 1800s (30:00). No media generated.
PREPRODUCTION QA PASS
44 screenplay scenes; screenplay and scene manifest targets match at 1,800 seconds.
132 planned shots; three per scene; timecodes span 00:00:00:00–00:30:00:00.
Every scene/shot is marked not produced; production state lists no master or link.
This does not validate a movie: no footage, audio, rendered file, or playback exists.
```

The check verifies scene IDs and order, the 1,800-second target, screenplay-to-scene-manifest duration parity, shot counts and timecodes, unproduced status labels, and absence of a claimed master/download location. It does not render media, review acting, test continuity in footage, validate lip sync, inspect audio, or measure runtime from a movie.

## Manual review performed

- Read the story for a beginning, escalating technical investigation, containment decision, partial recovery, and ending.
- Reconciled the identity bug, retry semantics, asynchronous read-before-write race, missing unique index, separate active-episode conflict, stale migration behavior, readiness-probe gap, and rollback incompatibility across the screenplay and technical note.
- Confirmed that all technical interface data is fictional and contains no credentials or real customer data.
- Confirmed that the manifests describe planned moving performances and mark all rows not produced; they are not footage assets.

## Not checked / not passed

At the time this preproduction-only check was recorded, there was no MP4/MOV, continuous moving footage, recorded dialogue, music/sound mix, or screenplay PDF, and FFmpeg/FFprobe had not yet been installed. Those statements are a historical snapshot, not the current production state. The 30-minute feature remains unproduced.

## Later production addendum — 2026-10-13

After this preproduction-only record, a 60-second stylized 2D prototype was rendered and preserved. A later continuation also produced a separate 60-second low-poly procedural 3D POC using Panda3D's software offscreen renderer; the current 3D file passed automated FFprobe/FFmpeg checks and six selected frames were reviewed. Current measurements, technical report, limitations and human-review status are in [`proof_of_concept_report.md`](proof_of_concept_report.md), [`quality_report.md`](quality_report.md), and [`production_state.json`](production_state.json). Neither proof changes any of the 132 planned feature-shot statuses or constitutes the approximately 30-minute film, a full human playback/listening review, artistic approval or feature QC.
