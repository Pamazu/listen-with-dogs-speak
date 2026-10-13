---
title: Video platforms for timed-video-prompts
description: How each video platform takes references, audio and lip sync, its limits, and its measured or published price; the adapter notes clip_spec.py renders for.
---

# Video platforms

Each row says where the fact came from and when. Prices move; re-check before a spend decision.

## Magnific (MCP, J's Premium account)

- **Models (catalog read 2026-10-13):** `bytedance-seedance-pro-2.5` (rated the best overall model;
  4-30 s, 1080p/720p/480p/Draft, prompt ≤ 10,000 chars, up to 30 image or character references, 10
  video, 10 audio, lip sync, native audio), `bytedance-seedance-pro-2.0` (4-15 s, up to 4K, prompt ≤
  40,000, 9 images, 3 video, 3 audio), `bytedance-seedance-fast-2.0` (720p/480p drafts),
  `minimax-video-3_0-max` (fast drafts).
- **References:** `video_generate` `references[]` with `type` `image`, `character`, `video`, `audio`,
  `product`, `style`; start and end frames go in `keyframes.{start,end}` and **cannot be combined with
  references**. Audio references need a visual reference on 2.0, not on 2.5.
- **Measured price** (`simulate_cost`, 10 s, 9:16, 2026-10-13): Seedance 2.5 Draft 2,000 credits, 720p
  4,400, 1080p 7,900; Seedance 2.0 720p 2,800; Seedance 2.0 Fast 720p 2,350. Check the live balance
  with `account_balance` before a batch.
- Run `simulate_cost` with the exact arguments before every paid generation.

## Dreamina (ByteDance / CapCut, the maker of Seedance)

- **Audio and lip sync:** Seedance 2.x on Dreamina generates voice and lip-synced dialogue in the same
  pass as the picture, in 8+ languages; OmniHuman 1.5 animates a presenter to an uploaded voice or
  song; every paid plan lists "lip sync audio generations" (J's plan screenshot, 2026-10-13). Whether
  OmniHuman handles animal faces is UNTESTED.
- **References:** an @ picker in the prompt box labels uploaded images, videos and audio itself. Map
  spec handles to those labels when pasting; check the labels in the live UI before the first run.
- **Price (J's screenshot, 2026-10-13, monthly billing):** Basic €8 then €13.99 (no Seedance);
  Standard €19 then €31, about 47 ten-second clips; Advanced €83 then €138, about 217; Ultra €270 then
  €450, about 729. Banner: "Seedance 2.5 from €0.04/sec", about €0.40 per 10 s clip in month one and
  €0.62-0.66 after. The model and resolution assumed by "47 videos" are cut off in the screenshot.

## Higgsfield

- **References:** `@<file name>` handles in the prompt. Soul ID (a trained character from photos) and
  Soul 2.0 (image model) are optional; nothing in this skill needs them.
- **Published price (Higgsfield's own articles):** Seedance 2.5 720p 8 s = 52 credits ≈ $2.55
  (2026-08-06); Seedance 2.0 720p 8 s = 36 credits ≈ $1.55-1.76 (2026-06-24); Seedance 2.5 from the
  ~$49 plan. Their pricing page needs JavaScript and was not read. About 4-8× Dreamina's price per clip
  for the same model.

## Our own platform

Read the clip spec JSON directly: it already separates identity (assets + identity text), positions,
timed shots, lines and sound. A platform adds a row to `MODELS` (limits) and `PLATFORMS` (handle
syntax) in `scripts/clip_spec.py`, or calls `check` and `render` as functions.

## Which platform wins for which job

UNTESTED. The first real clips decide it; record the winner and the evidence in
`0_Global/reference/best-model-per-job.md` (its video-generation row is open).
