# POC Media Quality-Control Report

**Date:** 2026-10-13<br>
**Primary asset:** `renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4`<br>
**Status:** **AUTOMATED TECHNICAL CHECKS PASS; SIX SELECTED FRAMES REVIEWED; FULL PLAYBACK, LISTENING AND ARTISTIC APPROVAL NOT COMPLETED.**<br>
**Scope:** 60-second proof only. This report is not a quality sign-off for the 30-minute feature.

## Measured properties — current 3D POC

| Property | Measured result |
|---|---|
| Container | MP4 / ISO Base Media (`mov,mp4,m4a,3gp,3g2,mj2`) |
| Format duration | 60.000000 seconds |
| File size | 6,284,063 bytes |
| Video codec/profile | H.264 High, `yuv420p` |
| Raster | 1280×720 (16:9 container; 1280×536 active picture with intentional letterbox bars) |
| Frame rate / count | 24/1 fps nominal and average; 1,440 frames; stream starts at 0.000000; duration 60.000000 s |
| Audio codec/profile | AAC-LC, 2-channel stereo, 48,000 Hz |
| Audio start / duration | 0.000000 / 60.000000 s |
| SHA-256 | `709661f705b401c8eb48b255243371f17a2e7e6087b6373b78de78816387b8ae` |

The complete machine-readable report is [`qc_poc_3d.json`](qc_poc_3d.json), produced by [`scripts/validate_media.py`](../scripts/validate_media.py). The checks used FFprobe `N-66595-gc2b38619c0-static` and FFmpeg `7.0.2-static`, installed temporarily in user space. The executed validation command was:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 PROJECT-ZERO-DAY/scripts/validate_media.py \
  PROJECT-ZERO-DAY/renders/previews/Project_Zero_Day_Proof_of_Concept_60s_3D.mp4 \
  --ffprobe /tmp/zero-day-npm/node_modules/@ffprobe-installer/linux-x64/ffprobe \
  --ffmpeg /tmp/zero-day-py/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2 \
  --report PROJECT-ZERO-DAY/production/qc_poc_3d.json
```

## Checks run

- **Full decode:** the validator decoded the entire MP4 with FFmpeg. Result: passed; 1,440 video frames decoded; no reported errors.
- **Frame sequence:** full-frame hashes found 0 consecutive identical adjacent-frame pairs. This is useful evidence of temporal change, not a substitute for assessing the animation's visual quality.
- **Active-picture black intervals:** none detected with FFmpeg `blackdetect` after excluding the designed letterbox bars.
- **Audio signal:** FFmpeg `volumedetect` measured mean `−31.6 dB` and peak `−12.2 dBFS`. No clipping was observed in that analysis. These are signal measurements only—not a listening judgment, final mix approval or broadcast loudness certification.
- **Representative visual inspection:** extracted stills at 5, 18, 28, 42, 55 and 59 seconds were opened and visually reviewed. They show the rollout/workstation, the changing queue, the duplicate/late-receipt trace, publisher hold and end card. The character, interface or composition changes across the sampled moments. These were selected-frame inspections, not a complete visual review.
- **Sound synchronization:** no dialogue or lip-sync is present. Generated sound cues were placed in the code at typing/anomaly/trace/hold beats. Audio and video both start at 0.000 seconds and report 60.000 seconds duration. No end-to-end human listening/watch pass was completed.

## Visual and production limitations

- The actual scene is software-rendered procedural 3D, but its character/set are visibly **primitive, low-poly and stylized**. The face, body, hands, lighting and room are not cinematic or photorealistic. There is no live actor, recorded performance, motion capture, finished film-quality character rig, or lip-synced dialogue. The 3D requirement is met only as a narrow technical animation proof; the realism ambition is not met.
- The sound is a quiet, synthesized non-dialogue bed with generated effects, not a final film mix, song, score or spoken performance.
- Only the six representative frames were opened. Full real-time playback and audio listening, frame-by-frame art/continuity review, subjective legibility review, color-grade pass, legal review and creative sign-off remain outstanding.
- The existing screenplay says 44 scenes and a target runtime of approximately 30 minutes; its duration/dialogue estimate has not been validated by table read, real performances or measured scene durations. The full 44-scene/132-shot feature remains unproduced.
- This POC is 1280×720 and 60 seconds, not a 4K feature master. The FFmpeg build used is GPL-enabled and was not redistributed; no formal H.264 patent/commercial-distribution review is claimed. This is a technical preview, not a commercial master.

## Historical 2D prototype

The earlier `renders/previews/Project_Zero_Day_Proof_of_Concept_60s.mp4` remains preserved. It independently passed the validator: 60.000 seconds, H.264/AAC, 1280×720, 24 fps, 1,440 frames, complete decode, no consecutive identical frame pairs, and no active-picture black intervals. Its size is 5,071,735 bytes and SHA-256 is `77129504abfc087e1b794532c193a681862e4b66b0cfd5b7231cd8fdaa37a237`. It is an earlier flat 2D procedural prototype, not a substitute for the current 3D POC.

The 3D POC was pushed to the fixed Arena branch in commit `3a674a6109979d728a9fd94079d912f2accd9e22`. GitHub Contents API reported 6,284,063 bytes and blob SHA `060426f7f8192e20a2567b0e8b553119f7d73761`; the raw API download had the local SHA-256 and passed a byte-for-byte comparison. This is a verified branch POC only. No GitHub Release, 30-minute master or feature upload is claimed.
