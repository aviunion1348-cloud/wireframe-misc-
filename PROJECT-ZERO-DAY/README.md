# PROJECT ZERO-DAY: THE LAST DEPLOY

## Production status: preproduction packet only — no film rendered

This repository contains a complete 44-scene screenplay draft and a production plan for a target 30-minute fictional technology thriller. **It does not contain a movie, trailer, recorded performances, generated video, rendered scene, poster, screenplay PDF, or downloadable film master.** No release or film download link exists. The screenplay's 30:00 duration is a timed editorial plan, not a measured runtime.

The production request was checked against the capabilities actually exposed in this session before work began. This environment has no video-generation or performance-capture tool, no video editor or render farm, no GPU, and no FFmpeg/FFprobe. Image-generation capability, where available, is not genuine moving performance footage and was not passed off as a film. Speech synthesis can create spoken audio, but it cannot supply a consistent ensemble performing and lip-syncing in moving scenes; it was not used as a substitute.

### Verified environment and destination

- Authorized repository remote: [`aviunion1348-cloud/wireframe-misc-`](https://github.com/aviunion1348-cloud/wireframe-misc-), public repository; the current session has repository-admin permission.
- Current work branch: `arena/3f506b54-wireframe-misc`.
- GitHub CLI authentication was present. Git LFS is not installed. No external video/object-storage connector or video-generation connector is available.
- Filesystem had approximately 20 GB free when checked. That is adequate for many intermediates but does not create footage or a rendering capability.
- `ffmpeg`, `ffprobe`, Blender, Manim, SoX, OpenCV, MoviePy, Pillow, NumPy, PyTorch, and Diffusers were not installed. No NVIDIA GPU was detected. ImageMagick `convert` was present.

These checks are observations from the production environment, not claims about the entire GitHub account or services outside this session.

## Contents

- [`screenplay/Screenplay_v1.md`](screenplay/Screenplay_v1.md) — complete story draft; 44 timed scenes with a beginning, escalation, containment decision, and ending.
- [`production/continuity_bible.md`](production/continuity_bible.md) — character, visual, sound, location, interface, and performance continuity.
- [`production/technical_validation.md`](production/technical_validation.md) — causal chain, representative fictional logs, failure/recovery behavior, and engineering review checks.
- [`production/scene_manifest.csv`](production/scene_manifest.csv) — 44 timed scene records.
- [`production/shot_manifest.csv`](production/shot_manifest.csv) — 132 planned moving shots across 44 scenes; each row is marked **NOT PRODUCED**.
- [`production/production_state.json`](production/production_state.json) — resumable phase/state record, including missing capabilities and unproduced deliverables.
- [`production/build_manifest.py`](production/build_manifest.py) — deterministic generator for the scene and shot manifests.
- [`production/check_preproduction.py`](production/check_preproduction.py) and [`production/preproduction_qc.md`](production/preproduction_qc.md) — checks for the screenplay/manifest timing and records their preproduction-only result. They explicitly do not validate a movie.

## Story and engineering premise

Tern Systems' Relay platform ingests industrial telemetry and helps utility operators route work orders; it does not control physical equipment. Under a deadline for an investor demonstration, the team ships an AI-assisted event-correlation release. A retry-specific delivery ID is mistaken for a stable source-event ID; a check-then-insert path races across consumers while reading a lagging replica; a stale migration image drops a legacy field but misses the expected uniqueness index; and a readiness probe tests connectivity rather than a complete business transaction. A downstream timeout after commit amplifies retries. Green infrastructure indicators coexist with duplicate and unconfirmed work orders. The team must choose containment and honest reconciliation over an unsafe rollback or a reassuring but unsupported public statement.

The AI assistant is neither a villain nor an authority. The screenplay locates responsibility in code, tests, deployment artifacts, schema compatibility, observability, and deadline decisions shared across the team.

## Delivery record

| Requested item | Status |
|---|---|
| Full 30-minute 4K MP4 / 24 fps master | **Not produced** |
| Continuous moving performances / complete playback review | **Not produced / not reviewable** |
| Synchronized dialogue, original score, sound mix | **Not produced** |
| 5.1 master, viewing copy, trailer, poster | **Not produced** |
| Screenplay and preproduction package | **Produced in this repository** |
| PDF screenplay | **Not produced**; the screenplay is Markdown |
| SHA-256 for film master / verified download link | **Not applicable**; no master file exists |

No placeholder has been created under a movie filename. Do not cite the planned runtime or this packet as a completed film. A future production needs genuine continuous moving performances, an audio and post pipeline, an actual render, and independent playback/QC before any master can be described or published as complete.

## Production, AI, and licensing notes

The story, characters, company, product, utility, interfaces, and incident data are fictional. The screenplay draft, continuity/technical notes, manifest generator, and planned shot descriptions were generated by the Arena AI agent from the user's production brief; no human rewrite or independent engineering/operations approval is recorded. The user supplied the creative brief and requirements. No human performers, crew, or production credits are claimed.

No recorded or generated audiovisual assets, dialogue, music, or poster were produced. Image and speech tools were not used as substitutes for a movie. No music or other third-party creative asset has been selected or licensed. A future production must document asset provenance, model/tool terms, performer/voice rights, music rights, and any required disclosures before distribution. Screen content uses invented, non-secret identifiers; it contains no real credentials or customer personal information.
