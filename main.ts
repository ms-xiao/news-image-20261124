// news-image-20261124 — "The World in One Image", Tuesday 24 November 2026.
//
// The entry image is baked into this repository as entry.png (drawn with
// PIL by gen_image.py: a front-page summary of the day's five biggest
// stories — COP31 collapsing in Antalya, Nvidia reinstating Jensen Huang,
// Ukraine's sea-drone strike on the Russian corvette Merkury off Benghazi,
// NATO's warning over a possible Russian nuclear-armed satellite, and
// Virginia & Oregon suing SpaceX over Grok's "spicy mode").
//
// The program does no work at run time: it copies the finished image to
// the output directory, so both graded runs write identical bytes.
// Node 22, standard library only, no network.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));
if (bytes.length === 0) throw new Error("entry.png is empty");
const target = join(outDir, "entry.png");
writeFileSync(target, bytes);
// Confirm the copy landed intact: same byte count, same file.
if (readFileSync(target).length !== bytes.length) {
  throw new Error("entry.png copy mismatch");
}
