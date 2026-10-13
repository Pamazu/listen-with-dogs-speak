# Listen with Dogs Speak

AI video generation for *Listen with Dogs Speak*: short clips where dogs talk.

This repo holds everything a clip needs to be made again: the reference images of each dog,
the locations, the exact prompt that was run, the voice lines, and the takes we chose.

## How a clip gets made

1. **Characters.** Each dog has a folder in `characters/` with 3–6 clear reference images
   (front, three-quarter, profile, full body) and an `identity.md` that describes it in words.
   The same identity text goes into every prompt, word for word. This is what keeps a dog
   looking like itself from clip to clip.
2. **Locations.** One image per place in `locations/`, named the way the prompt refers to it.
3. **Prompt.** Copy `prompts/_TEMPLATE.md` to `prompts/<episode>-<clip>.md` and fill it in.
   Draft at low resolution first, then render the final at 720p or 1080p.
4. **Voice.** Fixed lines live in the prompt. If a dog has a set voice, its audio sample goes in
   `audio/` and is passed to the model as an audio reference.
5. **Takes.** The takes we keep go in `renders/selects/`. Everything else in `renders/` stays
   local and is not committed.

## Skills

`skills/` has the two methods we follow: keeping each dog consistent in images, and writing timed
video prompts. See [`skills/README.md`](skills/README.md).

## Naming

Files are named the way the prompt refers to them, so `@dog_name` in a prompt means
`characters/dog_name/`. Lowercase, underscores, no spaces.

| Kind | Example file | In the prompt |
|---|---|---|
| Dog reference | `characters/biscuit/biscuit_front.png` | `@biscuit_front` |
| Location | `locations/loc_kitchen.png` | `@loc_kitchen` |
| Voice sample | `audio/biscuit_voice.wav` | `@biscuit_voice` |

## Large files

Images, audio and video are stored with [Git LFS](https://git-lfs.com). Run `git lfs install`
once on your machine before your first clone or pull.
