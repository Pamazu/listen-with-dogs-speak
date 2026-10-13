# Test: Coco, 2026-10-13

Imaginary dog (no photos), `examples/coco.json`, prompts from `scripts/view_prompts.py`, Seedream 5
Pro on Magnific, 1:1, 2k, 100 credits per image. Prompt 1 (front, neutral) made the anchor; every
other image had the anchor attached as an `image` reference.

| Image | Result |
|---|---|
| `coco-test/coco_front_neutral.jpg` (anchor) | Pass. White Bichon, round head trim, apricot patch on her left ear, mint collar, heart tag, slate-grey backdrop, strong contrast. Body slightly turned rather than square to the camera. |
| `coco-test/coco_back_neutral.jpg` | Pass. Same dog from behind; the apricot ear is on the correct side for a back view. |
| `coco-test/coco_left_happy.jpg` | Pass. Left profile, head to frame left, mouth open with tongue out, same collar and patch. |
| `coco-test/coco_three_quarter_left_sad.jpg` | Pass on the third run. |

The three-quarter sad view took three runs, and each failure changed the script:

1. **First wording** ("head slightly lowered, ears drooping back ... tail low"): right view and identity,
   but the face read as neutral. The sad description was made stronger (head hanging low, ears flat
   back, mournful eyes, tail between the hind legs, shoulders slumped).
2. **Stronger sad:** clearly sad, but the dog faced frame right (the mirror view). The profile views had
   worked because they say which way the head points in the frame; the three-quarter views now say so
   too ("head toward the left of the frame and the body extending back toward the right").
3. **Both fixes:** correct view, same dog, sad expression with the tail down. Kept.

Also learned: the identity text must describe the tail's look, not its position ("a long plumed
tail", not "carried over the back"), or it fights expressions like sad.

Not yet tested: a real dog from photos, the angry, surprised, curious and talking expressions, the right
profile, and a second model (Nano Banana Pro).
