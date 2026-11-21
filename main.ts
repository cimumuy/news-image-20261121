// main.ts -- hand-in program for the news-image-20261121 entry, an entry
// for the make.fun bounty "Sum up 21 November's world news in one image".
//
// The picture itself is drawn ahead of time by compose.py (see README.md);
// this program's whole job is to deliver it: copy the repository's
// entry.png into $MAKEFUN_OUTPUT_DIR (falling back to /output).
//
// Plain CommonJS-flavoured syntax inside a .ts file, so any Node.js
// runtime can run it as-is:  node main.ts

const fs = require("fs");
const path = require("path");

function deliver(): void {
  const targetDir: string = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const from: string = path.join(__dirname, "entry.png");
  const to: string = path.join(targetDir, "entry.png");
  fs.mkdirSync(targetDir, { recursive: true });
  fs.copyFileSync(from, to);
  const bytes: number = fs.statSync(to).size;
  console.log("delivered " + from + " -> " + to + " (" + bytes + " bytes)");
}

deliver();
