// Simple taxonomy validator
// Usage:
//   npm install ajv ajv-formats (once)
//   node taxonomy/validate.js
// Exits non-zero on failure.

const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv); // adds date-time, uri, email etc.

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const schemaPath = path.join(__dirname, 'schema.json');
const dataPath = path.join(__dirname, 'requisite_variety_taxonomy.json');

const schema = loadJson(schemaPath);
const data = loadJson(dataPath);

const valid = ajv.validate(schema, data);
if (!valid) {
  console.error('INVALID');
  console.error(ajv.errors);
  process.exit(1);
}
console.log('VALID');
