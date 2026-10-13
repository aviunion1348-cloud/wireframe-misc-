# POC Media Quality-Control Report

**Date:** 2026-10-13
**Asset:** `renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4`
**Status:** **TECHNICAL FILE CHECK PASS; LIMITED VISUAL REVIEW; FULL PLAYBACK / LISTENING REVIEW NOT COMPLETED.**
**This report is for the 60-second POC only, not the 30-minute feature.**

## Measured media properties

| Property | Measured result |
|---|---|
| Container | MP4 / ISO Base Media (`mov,mp4,m4a,3gp,3g2,mj2`) |
| Format duration | 60.000000 seconds |
| File size | 5,071,735 bytes |
| Video codec/profile | H.264 High, `yuv420p` |
| Video raster | 1280×720 pixels (16:9 container with 2.388:1 active picture and intentional letterbox bars) |
| Frame rate / count | 24/1 fps average and nominal; 1,440 frames; stream start 0.000000; duration 60.000000 s |
| Audio codec/profile | AAC-LC, 2-channel stereo, 48,000 Hz |
| Audio start / duration | 0.000000 / 60.000000 s |
| SHA-256 | `77129504abfc087e1b794532c193a681862e4b66b0cfd5b7231cd8fdaa37a237` |

**Tools used:** FFprobe `N-66595-gc2b38619c0-static` for the stream/container report; FFmpeg `7.0.2-static` for full decode, audio analysis and frame hashing. Both binaries were temporary user-space tools.

## Checks run

- **Full demux/decode:** FFmpeg read the entire MP4, decoded audio/video, and wrote to a null output; command completed successfully with no reported decode error.
- **Frame sequence:** FFmpeg `framemd5` returned 1,440 decoded video frames. An adjacent digest comparison found **0 consecutive identical pairs**. This supports that the file is not a sequence of repeated still frames; it does not by itself certify artistic performance quality.
- **Audio signal:** FFmpeg `volumedetect` reported mean `−31.6 dB` and maximum `−12.2 dBFS`. No clipping was seen in this analysis. These are signal measurements, not a listening judgment or broadcast loudness certification.
- **Representative visual inspection:** one decoded still each at 5, 18, 28, 42, 55 and 59 seconds was opened and reviewed. The sampled moments show the workstation/canary, changing queue, duplicate/late-receipt trace, publisher hold, and explicit POC end card. The character's posture/gaze/body/hands, interface state and camera composition differ across the reviewed moments. Temporary extracted stills were removed after inspection.
- **Synchronization claim:** no dialogue or lip-sync exists. Synthesized sound cues were placed in code at the typing/anomaly/trace/hold beats. Stream start times and durations match exactly at 60 seconds, but a real-time human audio/video listening-and-watch pass was not completed.

## Limitations and open QC

- There is no playback/display or `/dev/snd` audio device in this environment. The MP4 was decoder-tested, not watched and listened to start-to-finish in a media player. A reviewer should play it and sign off on motion, legibility, sound level, emotional tone, and cue timing.
- The visual is deliberately disclosed as **flat, stylized procedural 2D**, not live action, 3D/Blender, photoreal, or captured human performance. The character has simple facial/body/hand animation, not actor-grade expression or lip sync.
- There is no spoken dialogue or performer recording. The sound is a quiet, synthesized non-dialogue bed with generated effects, not a final film mix or original orchestral score.
- Only the listed representative frames were visually opened; no frame-by-frame art/continuity review, legal review, color-grade pass, complete performance assessment, or feature-level QC was performed.
- This 1280×720, 60-second clip does not meet the full-film target of approximately 30 minutes and native 4K. The existing 44 scenes and 132-shot feature plan remain unproduced.
- The selected H.264 encoder build is GPL-enabled and was not redistributed. No formal patent/commercial-distribution review was performed; the POC is not a commercial master.
- No GitHub Release or film-master upload is claimed. The POC is a small preview asset; repository-branch write/read verification is tracked in the production log after publication.
