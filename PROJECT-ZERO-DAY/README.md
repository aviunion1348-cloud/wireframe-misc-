# PROJECT ZERO-DAY: THE LAST DEPLOY

## Production status: IN PROGRESS — POC rendered; feature not produced

This repository contains the existing 44-scene screenplay and preproduction package, plus a **single 60-second stylized 2D proof of concept**. It does **not** contain the requested approximately 30-minute feature film, any 4K master, recorded human performances, or a complete feature playback/QC pass. The POC is not a trailer or finished film.

## Actual video deliverable

- **File:** [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4`](renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4)
- **Measured:** MP4, 60.000 seconds; H.264 High, 1280×720, 24 fps, 1,440 frames; AAC-LC stereo 48 kHz; 5,071,735 bytes.
- **SHA-256:** `77129504abfc087e1b794532c193a681862e4b66b0cfd5b7231cd8fdaa37a237`.
- This is one continuous procedural 2D animation sequence: a stylized engineer types at a workstation during a canary deployment, notices an asynchronous queue anomaly, traces duplicate delivery/late receipt evidence, and pauses outbound dispatch while preserving intake. The figure's face, body, eyes, hands and posture move; interface values and camera framing change over time. It is not a still-image pan or slideshow.
- The visual is flat-color procedural animation—not live action, photoreal footage, Blender 3D, or a captured actor. Audio is an original synthesized non-dialogue soundscape with timed effects. There is no recorded speech, voice actor, or lip sync. The last seconds display an explicit “not the finished film” label.
- FFprobe measured both streams at 60.000 seconds; a full FFmpeg decode passed and no adjacent video frames were identical. Six representative moments were opened for visual review. A human real-time full-length playback/listening pass was **not** completed because the container has no local display/audio device. See the separate POC and quality reports for the exact checks and limitations.

The five entries in [`production/render_manifest.csv`](production/render_manifest.csv) are review ranges within that one MP4; they are not separate clips. No release or feature-film download link exists.

## Feature production status and limits

The requested target remains approximately 30 minutes, with native 4K/24 fps only if source and compute support it. No feature scene or planned shot has been produced: the original [`shot_manifest.csv`](production/shot_manifest.csv) remains marked **NOT PRODUCED** for all 132 planned moving shots, and the scene manifest remains a plan. `production_state.json` distinguishes this feature plan from the 60-second POC.

The POC establishes that a small local Pillow/NumPy/FFmpeg animation can render. It does not provide 44-scene art/character/location coverage, a human performance or dialogue workflow, a full audio/post pipeline, or the quality bar of a finished thriller. Blender's Python wheel cannot run here because seven system graphics libraries are missing. The environment has no camera, video-generation/performance-capture system, GPU, or audio playback device, and exposes two CPU threads and about 3.8 GiB RAM. The full film is therefore still **IN PROGRESS / BLOCKED**, not complete.

## Continuity and technical premise

Tern Systems' Relay platform ingests industrial telemetry and helps utility operators route work orders; it does not control physical equipment. Under deadline pressure, a team ships an AI-assisted event-correlation release. A retry-specific delivery ID is mistaken for a stable source-event ID; a check-then-insert path races across consumers while reading a lagging replica; a stale migration image drops a legacy field but misses the expected uniqueness index; and a readiness probe checks connectivity rather than a full business transaction. A downstream timeout after commit amplifies retries. Green infrastructure indicators coexist with duplicate and unconfirmed work orders. The team must choose containment and honest reconciliation over an unsafe rollback or a reassuring but unsupported public statement.

The AI assistant is neither a villain nor an authority. Responsibility lies in code, tests, deployment artifacts, schema compatibility, observability, and deadline decisions shared across the team. The POC's fictional dashboard and IDs follow the project technical-validation note; it does not represent a real utility, customer, secret, or production system.

## Project documents and tracking

- [`screenplay/Screenplay_v1.md`](screenplay/Screenplay_v1.md) — full draft with 44 timed scenes.
- [`production/continuity_bible.md`](production/continuity_bible.md) — character, visual, sound, location, interface and performance continuity.
- [`production/technical_validation.md`](production/technical_validation.md) — incident causality, failure/recovery semantics and engineering realism checks.
- [`production/scene_manifest.csv`](production/scene_manifest.csv) — 44 planned scenes, still unproduced.
- [`production/shot_manifest.csv`](production/shot_manifest.csv) — 132 planned feature shots, still unproduced.
- [`production/proof_of_concept_report.md`](production/proof_of_concept_report.md) — what the POC contains, how it was made, requirements met/unmet, and review limits.
- [`production/quality_report.md`](production/quality_report.md) — measured MP4 properties, full-decoder/frame checks, selected-frame review, and open QC.
- [`production/render_manifest.csv`](production/render_manifest.csv) — POC timeline ranges and frame-level review records; not separate clips.
- [`production/production_log.md`](production/production_log.md) — actions, environment, render and production boundary.
- [`production/capability_audit.md`](production/capability_audit.md) — actual operating environment, installed temporary tools, Blender blocker, and current feasibility assessment.
- [`production/production_state.json`](production/production_state.json) — resumable machine-readable status. The feature-master fields remain null.
- [`production/build_manifest.py`](production/build_manifest.py) — generator for the planned 44-scene/132-shot manifests; it creates planning metadata only.
- [`production/check_preproduction.py`](production/check_preproduction.py) and [`production/preproduction_qc.md`](production/preproduction_qc.md) — screenplay/manifest timing checks. The QA report's original no-media statements are a historical pre-POC snapshot; its addendum points to current POC QC.
- [`scripts/render_poc.py`](scripts/render_poc.py) — procedural POC animation/soundscape renderer. Temporary Python packages and FFmpeg/FFprobe binaries are not stored in this repository.

## Delivery record

| Deliverable | Status |
|---|---|
| 60-second moving-image POC | **Rendered; technical file checks passed; representative stills reviewed.** Full human playback/listening review remains open. |
| Continuous approximately 30-minute feature | **Not produced.** |
| 4K / 24 fps feature master | **Not produced.** The POC is 720p. |
| Human live-action/photoreal or lip-synced ensemble performances | **Not produced.** POC is procedural 2D and has no dialogue. |
| Full final dialogue, original score, mix, 5.1 master, viewing copy, trailer, poster, screenplay PDF | **Not produced.** POC contains only synthesized non-dialogue sound. |
| POC SHA-256 / verified repo artifact | Checksum is recorded above; remote branch verification is logged after actual publication. No feature-master checksum/link exists. |
| GitHub Release | **Not created.** A proof of concept is not being presented as the completed film. |

## Provenance and licensing notes

The story, characters, company, product, utility, interfaces and incident data are fictional. The screenplay draft, continuity/technical notes, manifest generator, planned shot descriptions and POC renderer were created by the Arena AI agent from the user's brief; no human rewrite or independent engineering/operations approval is recorded. No human performers, production crew, recording assets, outside video, model weights, generated stills, or third-party audio are claimed. The POC uses programmatically drawn shapes, system-installed DejaVu Sans text (no font binary copied into the repository), and synthesized audio. The capability audit records the observed font license and temporary tooling. The bundled FFmpeg build used for H.264 encoding is GPL-enabled and was not redistributed; no formal H.264 patent/commercial-distribution review was performed, so this POC is not a commercial master. Future production must document asset/model provenance, performer/voice rights, music rights, tool terms and any required distribution disclosures before release.

## Resume requirements

1. Preserve this screenplay, continuity bible, technical validation and 132-shot plan unless the user explicitly requests a story revision.
2. Before scaling, have a human play the POC from start to finish, listen to the mix, and record creative/technical notes. The current report is not that sign-off.
3. Establish an authorized zero-cost (or explicitly funded) workflow for consistent moving performances/animation, dialogue, asset provenance, and post-production. Do not treat one stylized POC scene as coverage for the 44-scene feature.
4. Produce and review every feature scene/shot against the script and continuity bible; track source paths, licenses, versions and actual review status in the manifests.
5. Render an actual full-length master, verify runtime/codec/resolution/frame rate/audio, complete a full playback pass, compute its checksum, and download it back from an authorized host before reporting delivery.
