# PROJECT ZERO-DAY — 60-Second Proof-of-Concept Report

**Date:** 2026-10-13
**Status:** **POC RENDERED; TECHNICALLY VERIFIED; SELECTED-FRAME REVIEWED. FEATURE FILM IN PROGRESS / BLOCKED.**

## Deliverable

- **File:** [`renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4`](../renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4)
- **Container/runtime:** MP4, exactly 60.000 seconds
- **Video:** H.264 High, 1280×720, 24/1 fps constant, 1,440 frames, yuv420p
- **Audio:** AAC-LC, stereo, 48 kHz, 60.000 seconds
- **Size:** 5,071,735 bytes
- **SHA-256:** `77129504abfc087e1b794532c193a681862e4b66b0cfd5b7231cd8fdaa37a237`
- **Purpose:** prove one continuous, temporally animated sequence can be produced in the actual environment before considering any scale-up. This is a stylized procedural-animation test, not the feature, a trailer, or live-action footage.

## What happens in the continuous sequence

The MP4 contains one uninterrupted 60-second timeline. The five rows in `render_manifest.csv` are review ranges within the same file; they are **not five disconnected clips**.

| Time | Beat | Visible evidence and movement |
|---|---|---|
| 00:00–00:12 | Workstation and canary deployment | Mara types at a night-shift engineering desk. The fictional Relay interface shows a 5% canary, green `/readyz`, ingress p99, and changing rollout progress. |
| 00:12–00:24 | Deployment continues | Camera slowly moves toward the monitor; animated hands, eyes, breathing, head/gaze and interface continue to change. Green liveness is not presented as end-to-end proof. |
| 00:24–00:35 | Subtle anomaly becomes visible | A restrained alert accompanies an asynchronous queue that grows while the green health/latency tiles remain. The character leans in and follows the changing graph. |
| 00:35–00:48 | Engineer investigates the trace | The interface shows fictional `source_event_id=alarm-77` twice under different delivery IDs (`d-A1`, `d-B2`), a 2,000 ms downstream timeout, and a 201 receipt +1.7 seconds later. Mara's gaze and posture move toward the evidence. |
| 00:48–01:00 | Containment decision and tone-setting finish | The cursor and hand move to a hold control. Outbound publishing pauses, raw intake is preserved, outbound requests read zero, and operator confirmation remains required. The ending is deliberately unresolved, not a claim of recovery. An on-picture footer labels this a 60-second stylized 2D POC and says it is not the finished film. |

The UI and all identifiers/metrics are fictional. No real infrastructure, customer data, credential, secret, or physical-control system is shown. The story treatment follows the existing technical validation: ingress acknowledgement is not action completion; a downstream timeout is an unknown result; a retry can carry a different delivery ID; containment pauses the outbound side effect while preserving intake.

## How it was made

- `scripts/render_poc.py` generates a newly drawn 1280×536 active picture for each of 1,440 frames at 24 fps, then places it in a 1280×720 letterboxed canvas. Pillow draws the room, animated character pose/eyes/hands, monitor and changing interface; a time-varying camera transform supplies motivated reframing. This is not a still-image pan/zoom or slideshow.
- The character is a simplified, flat-color vector/2D procedural figure with head/eye movement, blinking, breathing/lean, typing and a keyboard-to-mouse/hold gesture. It is a genuine animated body/face performance in the limited procedural sense, **not a recorded human actor, photoreal performance, or 3D character**.
- NumPy creates a non-dialogue stereo soundscape from synthesized room-tone/pad signals and timed keyboard, alert and button transients. No sampled music, speech, TTS, recorded dialogue, voice actor, or lip-sync is present. Audio events are placed at the corresponding interface beats in the timeline.
- Tools and versions: Python 3.11.2, Pillow 12.3.0, NumPy 1.26.4, `imageio-ffmpeg` 0.6.0, FFmpeg 7.0.2-static (`libx264`/AAC), and FFprobe `N-66595-gc2b38619c0-static`. Python packages and binaries were installed in temporary user-space directories, not system-wide and not committed. The wrapper reports BSD-2-Clause metadata; the bundled FFmpeg build configuration is GPL-enabled (`--enable-gpl`, `--enable-libx264`).
- Visual assets are procedurally drawn. Text uses the system DejaVu Sans font; no font binary is included in the repository. No model weights, stock footage, image-generation stills, or third-party audio assets were used. The POC has no formal H.264 patent/commercial-distribution clearance; it is a technical preview, not a commercial master. See `capability_audit.md` for verified tool and font licensing notes.

## Render and validation performed

1. The renderer passed an initial six-second smoke test (144 frames). After sound-level and queue-age refinements, the final 60-second render was run from the updated script and completed at 1,440/1,440 frames.
2. FFprobe inspected the final file: MP4, 60.000 s; H.264 High 1280×720 at 24/1 with 1,440 frames; AAC-LC stereo 48 kHz at 60.000 s. Both streams start at 0.000 s and report 60.000 s duration.
3. FFmpeg decoded the entire final MP4 to a null output with no reported decode error.
4. `framemd5` decoded 1,440 video frames and found **zero consecutive identical-frame pairs**.
5. FFmpeg `volumedetect` reported mean volume −31.6 dB and maximum −12.2 dBFS; no digital clipping was observed in that analysis.
6. Six representative extracted frames (5, 18, 28, 42, 55 and 59 seconds) were opened and visually inspected for the workstation, anomaly, trace, containment and end-card beats. Their temporary QC stills were not retained as substitutes for the MP4.
7. The full file was decoder-tested and its representative moments were inspected. **A complete human real-time playback pass and a listening pass were not completed**: this container exposes no local display/audio playback device. The browser-facing MP4 remains available for playback by a reviewer.

Detailed media values and scope limits are in [`quality_report.md`](quality_report.md). The true production status is tracked in [`production_state.json`](production_state.json); the 44-scene screenplay and 132 planned feature shots remain unchanged and unproduced.

## Acceptance assessment

| POC requirement | Result |
|---|---|
| 60–120 seconds of continuous moving-image proof | **Met:** one 60.000-second H.264 MP4, not a slideshow or assembled random clips. |
| Developer/engineer at workstation and deployment beat | **Met, stylized:** animated engineer at desk; changing canary/deployment UI. |
| Subtle anomaly, engineer notices/debugs | **Met, stylized:** queue/trace behavior changes and character posture/gaze follow it. |
| Moving body/face | **Met within the disclosed 2D procedural style:** animated face/eyes/body/arms/hands. |
| Synchronized audio | **Partly met:** generated sound cues align with the key interface/gesture times; no dialogue/lip-sync and not subjectively listened to here. |
| Actual MP4 properties / decoder validation | **Met technically:** FFprobe values recorded; full FFmpeg decode and adjacent-frame check passed. |
| Human full playback and creative sign-off | **Not met:** only selected-frame inspection and complete technical decode; needs an actual playback/review pass. |
| Full 30-minute film, genuine live-action/photoreal performance, 4K | **Not met / blocked:** no such footage or master exists. |

## Next production decision

The POC proves a small local procedural-animation pipeline works; it does **not** establish that scaling this one office/character into the existing 44 scenes and 132 planned shots would meet the user's full-film requirement. This environment still has no live-action or temporal-video assets, no usable Blender runtime, no local dialogue performer/TTS path, no playback hardware, and only two CPU threads and 3.8 GiB RAM. Do not label the POC a movie or mark the feature complete. A full feature requires a legally usable, repeatable performance/animation and dialogue workflow, actual scene/shot coverage and continuity review, post/audio, sufficient resources, and a complete playback/QC pass.
