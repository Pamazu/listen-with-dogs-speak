---
name: consistent-character-images
description: For ONE character or object (e.g. a dog called Coco), write the full set of image-generation prompts for its reference images, one prompt per view (front, back, left side, right side, three-quarter) and one per view for each useful expression (neutral, happy, sad, angry, surprised, curious, talking ...), each producing one clean image on a plain neutral background that contrasts with the character, precisely matching the reference photos. Real characters start from reference photos; imaginary ones from a description and an anchor image. The images then serve as references for a video model. Dogs and animals first, people and objects too; any image model or platform (Seedream, Nano Banana, GPT Image, Higgsfield Soul 2.0, our own), no Soul ID needed. Never a video prompt, a scene or a multi-character set. Places and props use the same discipline (section 3b).
---

# Consistent character images

**Input:** one character or object, usually with reference photos. **Output:** every prompt needed to
make its reference images, one image per prompt:

- one prompt per **view**: front, back, left side, right side, three-quarter;
- one prompt per view for each **expression**: neutral, happy, sad, angry, surprised, curious, and
  talking if the character speaks (more on request).

For Coco with the defaults that is 5 views × 7 expressions = 35 prompts. The finished images become
Coco's references for a video model later (`timed-video-prompts`).

**Not this skill:** a video prompt, a scene with the character acting, or several characters at once.
One character per run; one view and one expression per image. **A place or a prop** uses the same
discipline (section 3b).

Write every prompt in English; talk to J in his language.

## 1. Start from the reference photos

**Real character (the usual case):** the photos are the truth. Before writing anything, look at every
photo and write down precisely what is there; never invent a detail the photos do not show.
- **Animal:** species, size and build described in plain words (never the breed name in a prompt: it pulls in that breed's typical anatomy, see section 3), real proportions (shoulder height, leg length against chest depth, body length against height), coat colour, length and texture, every marking
  and which side it is on, eye colour, ear set, nose colour, tail shape and length (not its position: where the ears and tail sit belongs to the expression), collar and tag.
- **Person:** face shape and width (broad or narrow, square or oval), the eyebrows' shape, thickness and
  the gap between them, eyes, nose, lips, skin tone and real texture, hair colour, length, texture and
  style, build, and every garment, shoe and accessory with its colour. **Write how this person smiles**,
  from their own smiling photo (how much tooth shows, whether the cheeks lift): on 2026-10-18 every
  generated J smiled with a full grin and round raised cheeks, and J's first words were that his cheeks do
  not do that. Video-Editor 1 found the same misses in all 42 pictures of round 6, each scoring 0.61 or
  more on the face-identity gate: invented glasses, brows set apart, a narrower and younger face,
  retouched skin, salon hair. A high score only says "not a stranger"; it never says "looks like him".
- **Name materials and measures, not impressions:** glasses by frame material, colour and thickness
  ("clear transparent plastic, medium thickness", never "light gold/clear"), a beard by length and
  where it is denser ("a few millimetres, denser on the chin"). A close-up renders the words literally:
  in a 2026-10-16 test, "a light gold/clear metal frame" put gold wire glasses on every close-up of a
  person whose frames are clear plastic.
- **Object:** shape, size, colours, materials, finish, printed marks.

Pick the 4-6 best photos to attach to every prompt. Good photos: only this subject, sharp, eyes visible,
at least 1024 px, no filters, front, three-quarters and both sides (markings differ by side), mouth
closed and open. If the photos miss a side or a detail, say so: the prompt for that view will be a
guess until a photo exists. **A person needs at least one neutral, mouth-closed photo:** on 2026-10-17
all four of J's photos smiled, and his neutral, surprised and curious images stayed below the likeness
bar after three tries each.

**The photos stay the references, for the set and for every later use of the character.** Never replace
them with generated images: a copy of a copy drifts. Measured on J, same three prompts: his four
generated pictures as references scored 0.63, 0.60 and 0.49; his real photos 0.65, 0.76 and 0.63.

**Imaginary character (no photos):** the description carries everything. The first prompt (front,
neutral) makes the **anchor image**; generate it, let J approve it, then attach it to every other
prompt. From then on the anchor is the character's reference photo.

## 2. Write the character file

```json
{
  "name": "Coco", "handle": "coco", "kind": "animal", "species": "dog",
  "tone": "light",
  "references": ["coco_photo_1.jpg", "coco_photo_2.jpg", "coco_photo_3.jpg", "coco_photo_4.jpg"],
  "identity": "<the precise description from section 1, one paragraph>",
  "drift": "<the 2-3 details most likely to change between images, e.g. the patch on the LEFT ear only>",
  "views": ["front", "back", "left", "right", "three_quarter_left"],
  "expressions": ["neutral", "happy", "sad", "angry", "surprised", "curious", "talking"]
}
```

- `kind`: `animal`, `person` or `object` (objects get views only, no expressions).
- `tone`: the subject's main colour, `light`, `mid` or `dark`. It picks a plain backdrop that contrasts
  with it: light subject on mid-dark slate grey, mid on light cool grey, dark on light warm grey.
- `references`: empty for an imaginary character.
- `tail_carriage` (animals, optional): how the tail is ALWAYS carried, e.g. "short, hanging relaxed in a slight
  downward arc". It replaces every tail phrase of the mood table, so no mood can raise or curl it.
- `framing`: `full_body` (default for animals and objects), `waist_up` (default for people, whose faces
  are too small to judge at full body) or `head_shoulders`. The `face` view is always a close-up.
- Extra views: `three_quarter_right`, `face` (a close-up, useful for expressions and lip sync).
- Extra expressions: `scared`, `excited`, `sleepy`; anything else goes in `custom_expressions` with its
  body-language description.
- People only, all optional:
  - `glasses`: `"none"` or the frames by material, colour and thickness. Glasses are an attribute, never
    part of `identity`: the script refuses `"none"` while `identity` or `drift` still mentions glasses.
  - `smile`: how this person smiles, from their own photo. It goes into happy, excited, curious and
    laughing; the default happy line no longer says "cheeks lifted".
  - `hair`: the haircut the person chose, when it differs from their photos (J has no clean cut now and
    picked one from older photos). The prompt says this haircut wins over the photos' hair length and style.
  - `held_expressions`: expressions no real photo of the person shows (J has no photo laughing). They are
    left out until such a photo exists, because the likeness gate has nothing true to compare them with.

`examples/coco.json` is a complete one.

**A person's set:** the neutral views at full body (outfit and build), every expression waist-up or
as a face close-up (at full body a face is about 60 px tall, too small to check or to reference).

## 3. Generate the prompts

```
python3 scripts/view_prompts.py coco.json          # Markdown, to read and copy
python3 scripts/view_prompts.py coco.json --json   # JSON, for batch runs or our own platform
```

The script refuses a file with a missing field, an unknown view or expression, or a tone that is not
light, mid or dark. Every prompt shares the same wording; only the view line and the expression line
change. That shared wording is what keeps the character identical, so do not hand-edit single prompts:
change the character file and run it again. `examples/coco-prompts.md` is the full output for Coco.

Each prompt carries, in order: the view, the expression written as body language, the identity text
(introduced by "the dog in the attached reference photos, reproduced exactly"), the details to keep
exactly, the identity lock (people: "do not beautify, smooth, slim, narrow, de-age or restyle the face",
naming face width, the eyebrows' shape and gap, and real skin texture with no retouching; animals:
"do not turn it into a generic dog of its breed"), the framing, the plain contrasting backdrop with soft even light
and a gentle rim light, camera at eye level with an 85mm lens, and "photorealistic, tack sharp,
colours true to the reference; only this one dog, no text, no props".

**Fixed features win over moods and over "make it visible" (J-approved 2026-10-19).** State each feature that never
changes (tail length and carriage, a patch, a pure-white area, leg shape) ONCE, in one wording, and remove every line
that pulls against it: a mood never changes it (`tail_carriage` does this for tails), and a visibility demand never
says "fully visible from base to tip", which models answer by making the part longer and sticking it out; say where it
sits and how short it is. A stronger rule added on top of a conflicting prompt does not work: the model averages every
mention (Coco, 18 Oct: "curves under" on top of "mid-wag" and "fully visible" still gave an upturned tail). Before
handing over a revised set, grep every prompt for each corrected feature and confirm every mention agrees.

**Never name what must not appear (J-approved 2026-10-19).** Image models draw what a prompt names, even after "no":
92 mentions of "no dewclaws" in Coco's set and every image had dewclaws. Describe the correct shape positively ("every
leg is a smooth, straight column; its inside edge is one unbroken line to the paw"); name the unwanted thing only in a
tool's separate negative-prompt field, never in an Avoid line. An edit prompt is the one exception: it may name the
thing once, to point at what to remove. Same rule as `timed-video-prompts` §4 "Write positives".

**Size comes from words AND a picture.** Words like "long legs", "whippet" or "like a deer" made Coco tall in every
image. Give real proportions in plain measures, and once one generated image has the right size, attach it as a
"height and proportions only" reference with a line saying what to ignore in it.

**Expressions are body language**, because image models draw "a sad dog" as stock. The script's
table: happy = soft eyes, open relaxed mouth, tongue slightly out, tail mid-wag; sad = head hanging
low, ears flat back, eyes looking up mournfully, tail down, shoulders slumped (milder wording came out
looking neutral in the test); angry = muzzle wrinkled, front teeth showing, ears
pinned, body stiff; surprised = eyes wide, ears up, mouth slightly open; curious = head tilted, ears
up; talking = mouth half open mid-word, real dog mouth, no human lips. From behind, the mood shows in
ears, tail and posture.

## 3b. Places and props: the same discipline

A location (a yard, a kitchen) drifts exactly like a character: on 2026-10-19 two images of "the same" yard put the
fence, house and steps in different places, because the prompt only described what the camera saw.

1. **Write the map first**: every fixed object of the whole place and where it is, by edge and corner, with rough
   sizes ("lawn 10 x 7 m; LEFT edge the house wall; BACK-LEFT corner the yellow steps; fence along the BACK and down
   the RIGHT; one big tree behind the back-right corner; FRONT open"). The map goes word for word into every image
   prompt of the place and every video prompt set there.
   **Leave nothing to guess (J, 19 Oct: "You need to be very specific ... not to leave questions or space for
   assumptions").** For every object write: its size in metres, its exact position (which edge, how far from what),
   what it is attached to or in front of and why it is there (steps lead to a DOOR, so the door is in the map), its
   material and colour, and how many there are ("exactly one tree", "two openings"). Then write what is NOT there and
   would otherwise be invented: neighbour houses, paths, flower beds, furniture, windows. On 2026-10-19 two runs of
   one yard prompt disagreed on every object that had no size, place or relation: steps against the wall vs
   free-standing with no door, different trees, neighbour houses in one and not the other.
   **Describe structures by how they are built, and place them where a builder would (J, 19 Oct).** "A deck with
   steps" came out as a slab in one run and a table on legs with side steps in the other: say what its sides are
   closed with, which way the boards run, how many steps, their height and depth, and whether they run its full
   length. And check the plan makes sense as architecture: a back door belongs in the middle of a wall with the deck
   centred on it, not squeezed into the corner by the fence; a model draws an odd plan faithfully and it looks wrong.
   **Put the place on one measured grid, and draw it (J, 19 Oct: "be very precise with angles, where everything is
   placed").** Pick an origin corner and axes, then give every object coordinates: where each wall and fence STARTS
   and ENDS, where corners meet (and that they meet AT a post, no gap, no overlap), where a building ends, and how far
   outside the place each outside object stands (a tree's trunk position AND its crown radius, so its nearest edge is
   known). Then draw that grid as a simple plan image from the same numbers (a script, never by hand) and attach it to
   every view as "where things are", while the chosen first view stays "how things look". On 2026-10-19 a top-down
   view ran the house past the fence corners and put a tree that stands 9 m outside onto the corner, because the map
   had edges but no ends and "behind the corner" but no distance. Give each later camera as a grid point and a
   direction, not "from the corner".
2. **One prompt per view**, each opening with where the camera stands and what that puts on the left, centre and
   right of the frame, then the full map. Make the first view with no place reference (style photos only); make
   every other view with the first attached FIRST.
3. **Light and mood from photos**: attach style photos the person likes (light, haze, colour), saying they set the
   light only.
4. **The angle of a video shot lives in the video prompt**, not in the place images: the images only need to show the
   place clearly and consistently, in any aspect.
   **A place gets a 360 set, not one angle (J, 19 Oct).** Scenes move the camera, so the references must cover every
   direction: the first view, then a straight-down plan (every object and its relation to everything), then views
   from the opposite corner, from inside the place looking out, and square-on to the main structure. Close the place
   on all sides (a fence, a wall) so every direction has something fixed to show. **Never write "copy the image" for
   a later view:** a model then copies the picture and ignores the new camera (19 Oct: a "straight-on" view came out
   as a twin of view 1). Say the reference sets only how things LOOK, never its camera, and add a "THIS FRAME MUST
   SHOW (unlike view 1)" line naming what is newly visible.
   **Text AND picture for every later view (J, 19 Oct: "apart from being extremely specific with the text, we'll
   also show the reference so that the other angles are extremely consistent").** Once the first view passes the twin
   test, pick one of the twins; every other view attaches it FIRST, keeps the full map text, and says the image wins
   over the text on how any detail looks (a window's panes, a door's panels), never on where the camera stands.
5. **The twin test (J, 19 Oct):** run the first view's prompt TWICE. If the two images show the same place, the
   prompt is exact enough; every difference between them is a gap in the map: write what was missing into the map,
   then run the twin test again. Never go on to the other views until the twins match. The same test works for a
   character's first image.
5. **Check every view against the map** (each object on its edge) before keeping it; one view that disagrees is
   regenerated, never kept.
6. **Props** (a ball, a hand, a cup): a short description with size, colour and which hand or side, and an image only
   when a draft gets it wrong.

## 4. Run them

- Same model and settings for the whole set (1:1 or 16:9, 2k). Attach the reference photos (or the
  anchor) to every prompt.
- Imaginary character: prompt 1 first, approval, then the rest with the anchor attached.
- On Magnific: `images_generate`, `mode: seedream-5-pro`, references of type `image`; 100 credits per
  image at 2k (2026-10-13), so a 35-image set costs about 3,500. Check `simulate_cost` first.
- On any other platform or our own: the same prompts; only how photos are attached changes.

## 5. Check every image before keeping it

**A real person: the measured likeness score decides, never the eye.** On 2026-10-16 a by-eye check
passed 42 of 42 images of J that he then found not quite him, and a stranger drawn from his text
description alone (no photos) looked like him at a glance. A face-identity model tells them apart at
once. Score each image's face against the person's real photos: ArcFace (InsightFace buffalo_l, SCRFD
alignment), cosine to the mean of the real photos, run on the PC through sDelegate, never on the Mac
and never at a third party (StoryStudio `tools/likeness/score.py`; StoryStudio's engine runs the same
gate on every persona generation). Bars measured on J (`tools/likeness/calibration-j-2026-10-17.json`):

| Score | Meaning |
|---|---|
| below 0.35 | not this person (strangers top out at 0.24, even ones drawn from his description) |
| front-facing below 0.67 | less like him than any photo of him (from his own photos' spread; his lowest real photo 0.76) |
| three-quarter below 0.50 | provisional, from one real photo at that angle |
| profile | the 0.35 floor only: the model is unreliable side-on |

A new person gets their own bars the same way: their real photos against each other, against about 8
strangers made from their description with the same prompts and no photos, and against 600 LFW faces.
SFace and dlib were measured and do not separate the description-strangers (2026-10-17). Animals and
objects have no measured score yet (UNTESTED): check them by eye and say so.

Then the eye, for what a score cannot see. **Zoom in** (crop each area to full size) on every fixed feature, not
the whole frame: the far legs (an extra claw shows there first), the white areas (specks), the tail tip, the side of
each marking. On 2026-10-18 both of Coco's far front legs had a dewclaw that the full-frame view hid.

- **It is the same character as the references:** each drift detail, markings on the correct side, eye
  and nose colour, ears, collar and tag, outfit.
- **The view is the one asked for:** left profile shows the left side with the head to frame left.
  Check the side with something asymmetric (a watch, a marking, a parting): reference photos taken
  from one angle pull the opposite view to that angle. On 2026-10-16 every "three-quarter right" of a
  person came out as his left side, the angle of two of his photos; the three-quarter views now name
  which shoulder is nearest the camera, as the profiles name where the head points. Judge which side
  is NEAREST, not whether the far side is hidden: at three-quarter the far arm and wrist still show.
- **The expression reads**, and anatomy is right: four legs, one tail, paws not hands, correct teeth.
- **Clean:** plain backdrop, whole body in frame, nothing else, no text.

Generate again with the same prompt at most twice (a retry moves the score by about 0.05 either way).
Still below the bar: hold the image out of the set and say why. Then fix:
- **One detail wrong:** a surgical edit with that image as the only input: "Change ONLY <the detail>.
  Keep everything else exactly unchanged." Score the edit too.
- **Keeps drifting:** add a real photo of that angle or expression; never a generated image (section 1).
  Nano Banana Pro was not more like J than Nano Banana 2.1 (3 prompts, 2.7 times the price).

If you cannot look at the image, say so instead of passing it.

## 6. The cast file and platform cast features

The images are half of a character. Keep with them a **cast file** (`<name>.md` next to the images): the identity
text, a MOVEMENT section (how it walks, runs, turns, holds still, its signature moves and timing), and its fixed
features. Example: `Business & Career/projects/build-listen-when-dogs-speak/reference/Coco/coco.md`.

When the video platform has a cast feature (Dreamina **elements**, a Higgsfield character, StoryStudio cast members),
load the images and the cast file into it once, and call the character by name in every video prompt; the scene
prompt then never restates its look or movement (J, 19 Oct: "the scene prompts should not describe anything about
how Coco looks"). Without one, paste the cast file unchanged at the top of each prompt.

## 7. Trained identities (optional)

Soul ID, a LoRA or a platform "character" can be trained from the same photos once a character recurs
a lot. Higgsfield's Soul ID is documented for people's faces; whether it holds a dog is UNTESTED. Use
one only if a side-by-side test against this method shows it wins.

## 8. Tested

2026-10-13, Seedream 5 Pro on Magnific, imaginary Coco, no photos: see `examples/coco-test.md`.

2026-10-17, J, a real person, 6 views x 7 expressions on Nano Banana 2.1 with four of his photos: every
image recognisably him (lowest 0.40) but below his real photos (median 0.57 vs 0.87); 40 of 47 passed
the measured bar after remakes. Scores, the test and the held images:
http://js-macbook-pro.tail0b0e20.ts.net:8890/b/j-reference-set/r5/ (task 7f9a9e59).

## Files

- `scripts/view_prompts.py`: character file → every view and expression prompt.
- `examples/coco.json`, `examples/coco-prompts.md`: a complete character file and its 35 prompts.
- `examples/coco-test.md` and its images: what four of those prompts produced.
- `references/sources.md`: which Higgsfield skills this draws on, and what was taken and left.
- `sources/higgsfield-ai-skills/`: the eight original Higgsfield skills, unmodified. Not loaded as
  skills.
