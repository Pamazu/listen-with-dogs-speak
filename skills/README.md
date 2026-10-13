# Skills

The working methods behind these clips, written so they apply to any image or video model or
platform, and to dogs first. Any AI agent (or a person) can follow them.

| Skill | What it is for |
|---|---|
| [`consistent-character-images/`](consistent-character-images/SKILL.md) | The same dog (or person) in new still images: the photos each dog needs, a character sheet, the identity-lock paragraph, scene prompts, expressions as body language, edits, and the check after each image. No Soul ID or other trained identity needed. |
| [`timed-video-prompts/`](timed-video-prompts/SKILL.md) | Timed, multi-shot video prompts: fixed lines, talking dogs, voice and lip sync, cuts, fixed positions. `scripts/clip_spec.py` checks a clip plan before any paid generation and writes the prompt for a given model. |

`consistent-character-images/sources/higgsfield-ai-skills/` holds the original Higgsfield skills these
draw on, unmodified, under their MIT licence (see the `LICENSE` there).

These are copies. The skills are maintained elsewhere and refreshed here with `tools/sync-skills.sh`,
so edit them at the source, not in this folder.
