# Skills

The working methods behind these clips, written so they apply to any image or video model or
platform, and to dogs first. Any AI agent (or a person) can follow them.

| Skill | What it is for |
|---|---|
| [`consistent-character-images/`](consistent-character-images/SKILL.md) | For one dog (or person, or object): every image prompt for its reference pictures, one per view (front, back, both sides, three-quarter) and one per view for each expression (neutral, happy, sad, angry, surprised, curious, talking). Clean, high-contrast, plain backdrop, matched to the dog's photos. `scripts/view_prompts.py` writes the whole set from one character file; see the Coco example and test. No Soul ID needed. |
| [`timed-video-prompts/`](timed-video-prompts/SKILL.md) | Timed, multi-shot video prompts: fixed lines, talking dogs, voice and lip sync, cuts, fixed positions. `scripts/clip_spec.py` checks a clip plan before any paid generation and writes the prompt for a given model. |

`consistent-character-images/sources/higgsfield-ai-skills/` holds the original Higgsfield skills these
draw on, unmodified, under their MIT licence (see the `LICENSE` there).

These are copies. The skills are maintained elsewhere and refreshed here with `tools/sync-skills.sh`,
so edit them at the source, not in this folder.
