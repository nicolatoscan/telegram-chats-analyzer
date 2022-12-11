import fs from 'fs';

// load json file
const json = JSON.parse(fs.readFileSync('data/result.json', 'utf8'));
for (const key in json) {
  console.log(key);
}