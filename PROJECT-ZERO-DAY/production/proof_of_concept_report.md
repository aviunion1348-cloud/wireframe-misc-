# PROJECT ZERO-DAY — 60-Second Proof-of-Concept Report

**Date:** 2026-10-13<br>
**Current POC status:** **3D PROCEDURAL CLIP RENDERED; TECHNICALLY VERIFIED; SELECTED-FRAME REVIEWED. FULL PLAYBACK / ARTISTIC APPROVAL PENDING.**<br>
**Feature status:** **IN PROGRESS / NOT PRODUCED.**

## Current deliverable

- **Primary POC:** [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4`](../renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4)
- **Container/runtime:** MP4, exactly 60.000 seconds
- **Video:** H.264 High, 1280×720, `yuv420p`, 24/1 fps, 1,440 frames
- **Audio:** AAC-LC, stereo, 48 kHz, 60.000 seconds
- **Size:** 6,284,063 bytes
- **SHA-256:** `709661f705b401c8eb48b255243371f17a2e7e6087b6373b78de78816387b8ae`
- **Purpose:** demonstrate one continuous timeline with visible, time-varying 3D character, camera, and interface animation in the available environment. This is a **low-poly procedural 3D proof**, not the requested feature, cinematic realism, live-action footage, or a finished film.

The earlier 2D prototype remains preserved at [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4`](../renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4). It is not the current POC for the stricter 3D/recorded-performance criterion.

## What happens in the continuous sequence

This is one uninterrupted 60-second MP4. The five entries for each version in `render_manifest.csv` are review ranges inside that file—not separate shots assembled as disconnected clips.

| Time | Beat | Visible evidence and movement |
|---|---|---|
| 00:00–00:12 | Workstation and rollout | A stylized 3D engineer sits at a night-shift desk, types, and watches a fictional Relay interface. The rollout stage changes while readiness and canary status remain visible. |
| 00:12–00:24 | Canary continues | The camera reframes; the character's head, eyes, posture and hands animate. The interface continues its staged rollout. Green liveness is not presented as proof of end-to-end action completion. |
| 00:24–00:35 | Queue anomaly | Queue depth and age rise while readiness/latency remain green. The character turns toward the display as the interface changes. |
| 00:35–00:48 | Trace investigation | The fictional trace shows `source alarm-77` under delivery IDs `d-A1` and `d-B2`, a 2,000 ms timeout and a `201` receipt +1.7 seconds later. Camera/gaze/posture shift toward the evidence. |
| 00:48–01:00 | Containment and unresolved ending | The character reaches for the mouse; outbound publishing pauses, raw intake is preserved, outbound requests read zero, and operator confirmation remains required. The final card explicitly says this is a 60-second 3D procedural proof, not the finished film. |

All UI, IDs and metrics are fictional; no production system, customer information, credential, secret or physical-control system is shown. The continuity is consistent with the screenplay's existing technical premise: ingress acknowledgement is not action completion; a downstream timeout has an unknown result; retries may have a different delivery ID; containment pauses the outbound side effect while preserving intake.

## How it was made

- `scripts/render_poc_3d.py` constructs a 3D room, workstation, monitor and stylized character from custom primitive meshes. Panda3D `TinyOffscreenGraphicsPipe` renders the scene off-screen in software; transforms animate the character's articulated primitive groups, head/eyes/arms/hands, interface and camera for every frame. This is actual rendered 3D geometry and temporal animation—not a still-image pan/zoom, slideshow, or a set of joined stills.
- **Important visual limitation:** the character and set are visibly simple, low-poly/primitive computer graphics. The face, hands, proportions, lighting and environment do **not** achieve cinematic or photorealistic realism. This is not a captured human actor, motion-capture performance, finished character rig, or finished-quality film. The requested visual ambition is therefore **not met** by this proof.
- The soundscape is generated procedurally using the existing `scripts/render_poc.py` audio routines and NumPy: non-dialogue room/pad ambience plus timed keyboard, alert and button cues. No sampled music, spoken dialogue, TTS, voice actor, recorded performance or lip-sync is present. Cue placement was checked technically, but the sound was not listened to end-to-end in this environment.
- Tools: Python 3.11.2; Panda3D 1.10.16 (Modified BSD); Pillow 12.3.0; NumPy 1.26.4; `imageio-ffmpeg` 0.6.0; FFmpeg 7.0.2-static; FFprobe `N-66595-gc2b38619c0-static`. Python packages/binaries were installed in temporary user-space directories, not system-wide or committed. The FFmpeg build is GPL-enabled (`--enable-gpl`, `--enable-libx264`) and is not included in the repository.
- Geometry and audio are procedural; no third-party character/scene assets, stock footage, generated stills, or model weights were used. The screen uses the installed DejaVu Sans font; no font binary is bundled. This is a technical preview, not a commercially cleared distribution master; no formal H.264 patent/commercial-distribution clearance is claimed.
- The final 60-second render used 1,440 frames and took 293,154 ms (about 4m53s) on the software-rendered environment. The separate six-second final-code smoke test completed at 144 frames before the full render. The full-render command was:

```bash
PYTHONPATH=/tmp/zero-day-py FFMPEG_BINARY=/tmp/zero-day-py/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2 \
  python3 PROJECT-ZERO-DAY/scripts/render_poc_3d.py --seconds 60 \
  --output PROJECT-ZERO-DAY/renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4
```

Those temporary runtime paths describe this session; the packages/binaries are not vendored into the repository.

## Render and validation performed

The repeatable validator is [`scripts/validate_media.py`](../scripts/validate_media.py); its machine-readable result is [`qc_poc_3d.json`](qc_poc_3d.json).

1. FFprobe inspected the final output: MP4; video and audio each start at 0.000 s and report 60.000 s duration; H.264 High 1280×720, 24/1 fps, 1,440 frames; AAC-LC stereo at 48 kHz.
2. The validator decoded the complete MP4 with FFmpeg: **passed**, 1,440 frames decoded, no errors.
3. A full-frame hash comparison found **zero consecutive identical-frame pairs**.
4. Active-picture `blackdetect` found **no black intervals** (the intended letterbox bars are excluded from the active-picture test).
5. Audio `volumedetect` measured mean −31.6 dB and peak −12.2 dBFS; no clipping was observed in that analysis. This is a signal-level check, not a listening or mix-quality approval.
6. Six extracted frames at 5, 18, 28, 42, 55 and 59 seconds were visually inspected for the workstation/rollout, queue anomaly, trace, containment and end-card beats. Temporary QC stills remain outside the production repository and are not substitutes for the MP4.
7. **A complete human real-time playback pass, listening pass, table read and artistic approval were not completed.** The environment has no local playback hardware. Selected stills and successful decoding are not approval of pacing, performance, continuity or cinematic quality.

The previous 2D file is preserved. It independently passed the same technical validator: 60.000 seconds, H.264/AAC, 1,440 frames, full decode, no consecutive identical frame pairs, no detected active-picture black intervals. Its SHA-256 is `77129504abfc087e1b794532c193a681862e4b66b0cfd5b7231cd8fdaa37a237`; size is 5,071,735 bytes. It remains a historical 2D prototype and does not replace this 3D POC.

The existing 44-scene screenplay, continuity bible, technical validation and 132-shot plan remain preserved. The screenplay's stated dialogue/runtime estimates have **not** been validated by a table read or actual performances; no timing revisions are claimed.

## Acceptance assessment

| Requirement | Result |
|---|---|
| Continuous moving-image proof | **Met technically:** one continuous 60.000-second MP4, not a slideshow or disconnected clips. |
| Actual 3D character and moving image | **Met narrowly:** primitive-based 3D figure, set, camera and interface animate over time. No actor was recorded. |
| Subtle technical anomaly and investigation | **Represented in the POC:** queue/trace values change while readiness remains green; selected frames show the beats. |
| Cinematic/photorealistic visuals | **Not met:** visibly low-poly procedural look. This is the main quality limitation, not something the technical checks can resolve. |
| Dialogue / real performance | **Not met:** no recorded actor, dialogue, TTS, voice or lip-sync. |
| Synchronized sound | **Partly met technically:** generated ambience and timed cues are present in the 60-second file; not subjectively listened to, and there is no dialogue. |
| Media integrity | **Met technically:** full FFmpeg decode and automated QC passed; SHA-256 and report recorded. |
| Human full playback and creative sign-off | **Not met:** selected-frame review only; full playback/listening and acceptance by a human reviewer remain open. |
| Existing 30-minute feature, all 132 planned shots, 4K master | **Not met / not produced:** the POC does not establish a feasible or quality-approved feature workflow. |

## Next production decision

Do **not** scale this primitive scene into a 30-minute film or describe the film as complete. The next gate is a human full playback/listening and explicit quality decision on this 3D proof. If its visual style is rejected, a different free/legal performance or animation workflow, suitable character/scene assets, and actual shot-by-shot coverage must be secured before production. A 30-minute screenplay runtime also remains an estimate until a table read, performance timings and real scene-duration review can be done. The feature still requires all planned scene/shot coverage, continuity review, dialogue/performance, audio post, sufficient compute/storage, and complete final playback/QC. See `capability_audit.md` for tested environment details and `production_state.json` for the machine-readable project status.
