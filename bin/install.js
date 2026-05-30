#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");

const root = path.resolve(__dirname, "..");
const source = path.join(root, "skills", "ru-software-registry");
const targetBase = process.env.CODEX_HOME
  ? path.join(process.env.CODEX_HOME, "skills")
  : path.join(os.homedir(), ".codex", "skills");
const target = path.join(targetBase, "ru-software-registry");

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else fs.copyFileSync(from, to);
  }
}

if (!fs.existsSync(source)) {
  console.error(`Skill source not found: ${source}`);
  process.exit(1);
}

fs.rmSync(target, { recursive: true, force: true });
copyDir(source, target);
console.log(`Installed ru-software-registry skill to ${target}`);

