---
title: Sources for consistent-character-images
description: The Higgsfield skills reviewed on 2026-10-13, what each contributed, what was left out, and the licence.
---

# Sources

Reviewed `github.com/higgsfield-ai/skills` at commit `f83af0b` (2026-09-26), skills version 0.13.0,
MIT licence, "Copyright (c) 2026 Higgsfield AI". It was read from a clone, not installed into a harness.
The eight original skill folders, their README and LICENSE are kept unmodified in
`../sources/higgsfield-ai-skills/` for comparison; they are not loaded as skills.
Everything taken was rewritten to work on any platform and for animals; no Higgsfield command or
model id is needed to use it.

Most of these skills drive Higgsfield's command-line tool, and their actual prompt templates for Soul,
photoshoots and marketplace cards stay on Higgsfield's servers ("backend owns prompt assembly"). So
the transferable craft is smaller than the repo.

| Higgsfield skill | Verdict | Taken |
|---|---|---|
| `higgsfield-soul-id` | Useful | The photo guide (count, angles, light, expressions, distances, what to avoid) → the photo rules, rewritten for dogs. |
| `higgsfield-generate` | Useful in parts | Job → model routing (character sheets, cartoon characters, empty locations, cinematic stills) → which kind of model to run the prompts on, as jobs, not model names. Prompt basics: describe the change on image-to-image, describe motion on image-to-video, positive phrasing, short prompts → the fix path for a bad image and `timed-video-prompts`. Media roles (start, end, reference, audio) → `timed-video-prompts`. |
| `higgsfield-youtube-thumbnail` | Most useful | The identity-lock block, the reference manifest line, the ordered prompt contract, the surgical-edit prompt, one prompt per variant, the post-render check → the identity text, the check and the surgical fix. The 16 thumbnail frameworks are kept for a later thumbnail skill. |
| `higgsfield-video-explainer` | Useful | Style descriptor + one style-key image on every generation, the mascot key, and "generate every voice take first, then the clips" → `timed-video-prompts`. |
| `higgsfield-product-photoshoot` | Partly | The short labelled-options interview and the shoot modes (studio, lifestyle, close-up, pin, banner, carousel, ad pack, try-on, conceptual, restyle) are a good menu for pet-product shoots later; its prompts are server-side, nothing else to take. |
| `higgsfield-marketplace-cards` | Not now | Routing only; templates are server-side. |
| `higgsfield-brandkit` | Not for this | Brand systems and logos are covered by the designer craft and its logo standard. |
| `higgsfield-websites` | Not for this | Website and game building. |
