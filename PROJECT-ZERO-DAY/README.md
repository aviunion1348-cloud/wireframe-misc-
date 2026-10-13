# PROJECT ZERO-DAY: THE LAST DEPLOY

## Production status: IN PROGRESS — 60-second 3D POC rendered; feature not produced

The repository contains the preserved 44-scene screenplay and preproduction package, an earlier 2D prototype, and a **single continuous 60-second low-poly procedural 3D proof of concept**. It does **not** contain the requested approximately 30-minute feature film, a 4K master, recorded human performances/dialogue, or a complete feature playback/QC pass. Neither POC is a trailer or finished film.

## Current video deliverable — procedural 3D POC

- **File:** [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4`](renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4)
- **GitHub branch file:** [view MP4](https://github.com/aviunion1348-cloud/wireframe-misc-/blob/arena/3f506b54-wireframe-misc/PROJECT-ZERO-DAY/renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4) · [direct download](https://raw.githubusercontent.com/aviunion1348-cloud/wireframe-misc-/arena/3f506b54-wireframe-misc/PROJECT-ZERO-DAY/renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4). GitHub Contents metadata and raw API download were checked; remote size and bytes match the local MP4.
- **Measured:** MP4, 60.000 seconds; H.264 High, 1280×720, 24 fps, 1,440 frames; AAC-LC stereo 48 kHz, 60.000 seconds; 6,284,063 bytes.
- **SHA-256:** `709661f705b401c8eb48b255243371f17a2e7e6087b6373b78de78816387b8ae`.
- **What it is:** one continuous software-rendered 3D sequence: a custom primitive character at a workstation types through a rollout, reacts to changing queue/trace evidence, and pauses outbound publishing. Character parts, head/eyes/hands, monitor state and camera move over time. Generated non-dialogue sound cues accompany the action. It is not a still-image pan, slideshow or collection of disconnected clips.
- **Important quality limitation:** the characters and room are conspicuously primitive/low-poly; this does **not** reach cinematic or photorealistic realism. No live actor, recorded performance, motion capture, spoken dialogue or lip-sync is present. Treat this as a narrow technical 3D animation proof, not a quality-approved film asset.
- Full FFmpeg decode, stream checks, frame-hash check and active-picture black detection passed. Six selected frames were opened and reviewed. **Full human playback/listening and artistic approval remain open.** See the [POC report](production/proof_of_concept_report.md), [quality report](production/quality_report.md), and [machine-readable QC result](production/qc_poc_3d.json).

## Preserved earlier 2D prototype

- [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4`](renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4) — a separate 60-second flat-color procedural 2D proof, technically validated and published earlier. It is retained for provenance and comparison; it does not replace the current 3D POC or meet the stricter 3D/recorded-performance preference.

## Feature production status and limits

The target remains approximately 30 minutes, with 4K/24 fps only if actual source and compute support it. No feature scene or planned shot has been produced: the original [`shot_manifest.csv`](production/shot_manifest.csv) remains **NOT PRODUCED** for all 132 planned moving shots, and the 44-scene manifest is still a plan. `production_state.json` distinguishes feature scope from POC work.

The current POC proves that a small free, software-rendered procedural 3D pipeline can encode a continuous minute. It does **not** establish that this visibly low-poly style—or the available CPU, tools and assets—can meet the requested film-quality bar or cover 44 scenes. Blender's Python wheel still cannot run because required system graphics libraries are missing; Panda3D enabled only the limited primitive-based POC. There is no camera, video-generation/performance-capture system, GPU, or local playback device; the container exposes two CPU threads and about 3.8 GiB RAM. The screenplay's runtime and dialogue estimates have not been tested by table read or actual performances. The feature remains **IN PROGRESS / BLOCKED**, not complete.

## Continuity and technical premise

Tern Systems' Relay platform ingests industrial telemetry and helps utility operators route work orders; it does not control physical equipment. Under deadline pressure, a team ships an AI-assisted event-correlation release. A retry-specific delivery ID is mistaken for a stable source-event ID; a check-then-insert path races across consumers while reading a lagging replica; a stale migration image drops a legacy field but misses the expected uniqueness index; and a readiness probe checks connectivity rather than a full business transaction. A downstream timeout after commit amplifies retries. Green infrastructure indicators coexist with duplicate and unconfirmed work orders. The team must choose containment and honest reconciliation over an unsafe rollback or a reassuring but unsupported public statement.

The AI assistant is neither a villain nor an authority. Responsibility lies in code, tests, deployment artifacts, schema compatibility, observability, and deadline decisions shared across the team. POC dashboard text and IDs are fictional and follow the project's technical-validation note; no real utility, customer, secret or production system is represented.

## Project documents and tracking

- [`screenplay/Screenplay_v1.md`](screenplay/Screenplay_v1.md) — full draft with 44 timed scenes; timing remains unmeasured.
- [`production/continuity_bible.md`](production/continuity_bible.md) — character, visual, sound, location, interface and performance continuity.
- [`production/technical_validation.md`](production/technical_validation.md) — incident causality, failure/recovery semantics and engineering realism checks.
- [`production/scene_manifest.csv`](production/scene_manifest.csv) — 44 planned scenes, still unproduced.
- [`production/shot_manifest.csv`](production/shot_manifest.csv) — 132 planned feature shots, still unproduced.
- [`production/proof_of_concept_report.md`](production/proof_of_concept_report.md) — contents, pipeline, acceptance assessment and limits of both POCs.
- [`production/quality_report.md`](production/quality_report.md) — measured media properties, decode/frame checks, selected-frame review and open QC.
- [`production/render_manifest.csv`](production/render_manifest.csv) — timeline review ranges for both POC versions inside their continuous files; not separate clips.
- [`production/qc_poc_3d.json`](production/qc_poc_3d.json) — machine-readable FFprobe/FFmpeg validation of the current 3D MP4.
- [`production/production_log.md`](production/production_log.md) — environment audit, render actions and production boundaries.
- [`production/capability_audit.md`](production/capability_audit.md) — initial and fresh checks, temporary tools, Panda3D/Blender findings and feasibility limits.
- [`production/production_state.json`](production/production_state.json) — resumable machine-readable status; feature-master fields remain null.
- [`production/build_manifest.py`](production/build_manifest.py) — generator for the planned 44-scene/132-shot manifests; planning metadata only.
- [`production/check_preproduction.py`](production/check_preproduction.py) and [`production/preproduction_qc.md`](production/preproduction_qc.md) — screenplay/manifest checks; the original no-media statements are a historical pre-POC snapshot, with the POC status documented in later reports.
- [`scripts/render_poc.py`](scripts/render_poc.py) — 2D prototype renderer and generated soundscape routines.
- [`scripts/render_poc_3d.py`](scripts/render_poc_3d.py) — Panda3D procedural 3D POC renderer.
- [`scripts/validate_media.py`](scripts/validate_media.py) — repeatable FFprobe/FFmpeg media validation. Temporary packages/binaries remain outside the repository.

## Delivery record

| Deliverable | Status |
|---|---|
| 60-second procedural 3D POC | **Rendered; automated technical checks passed; six selected frames reviewed.** Visibly low-poly, not cinematic realism. Human full playback/listening and approval remain open. |
| Historical 60-second 2D POC | **Preserved; technical checks passed; not the current 3D POC.** |
| Continuous approximately 30-minute feature | **Not produced.** |
| 4K / 24 fps feature master | **Not produced.** The current POC is 720p. |
| Human live-action/performance-capture or lip-synced ensemble performances | **Not produced.** |
| Feature dialogue, original score, final mix, 5.1 master, viewing copy, trailer, poster, screenplay PDF | **Not produced.** The POC contains only generated non-dialogue sound. |
| POC checksum / branch artifact | **Checksum and technical QC recorded.** A branch POC is not a feature master or release. |
| GitHub Release | **Not created.** No feature-film download/streaming link is claimed. |

## Provenance and licensing notes

The story, characters, company, product, utility, interfaces and incident data are fictional. The screenplay draft, continuity/technical notes, manifest generator and POC code were created from the user's brief; no independent engineering/operations or creative approval is recorded. No human performers, recording assets, outside video, character model, model weights, generated stills or third-party audio are claimed. The 3D scene is assembled from procedural geometry; the sound is synthesized. Text uses the system-installed DejaVu Sans font; no font binary is copied into the repository. Panda3D 1.10.16's wheel metadata identifies the Modified BSD license. Temporary FFmpeg 7.0.2 is GPL-enabled and was not redistributed. No formal H.264 patent/commercial-distribution review was performed; these POCs are not commercial masters. Future production must document asset/model provenance, performer/voice rights, music rights, tool terms and any required distribution disclosures before release.

## Resume requirements

1. Preserve this screenplay, continuity bible, technical validation and 132-shot plan unless the user explicitly requests a story revision.
2. Have a human play the 3D POC start-to-finish, listen to its sound, and record explicit acceptance/rejection notes for the low-poly style before any feature-scale decision. This report is not that sign-off.
3. If realism is rejected, establish an authorized zero-cost (or explicitly funded) quality-level animation/performance, dialogue, asset-provenance and post workflow. Do not treat one stylized POC as coverage for the 44-scene feature.
4. Table-read the existing screenplay and measure actual performance/scene timings before changing runtime targets. Current duration estimates are not verified.
5. Produce and continuity-review every actual feature scene/shot against the script; track paths, rights, versions and review status in the manifests. Never mark planned shots produced without media.
6. Render an actual full-length master, validate runtime/codec/resolution/frame rate/audio, complete human playback and QC, compute its checksum, and download-verify it from an authorized host before reporting delivery.
