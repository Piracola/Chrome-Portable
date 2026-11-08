const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const config = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'browser.json'), 'utf8'));
const targets = Object.entries(config.targets);
assert.equal(targets.length, 4);
const versions = {};
const filenames = {};
for (const [id, target] of targets) {
  assert.equal(target.exe_name, '..\\chrome.exe', `${id}: executable path`);
  assert.equal(target.layout, 'move_version_root', `${id}: package layout`);
  assert.equal(target.version_root, 'Chrome-bin');
  assert.equal(target.release.asset_match_mode, 'regex');
  assert.equal(target.provider.type, 'google_omaha');
  assert.equal(targets.filter(([, t]) => t.env_prefix === target.env_prefix).length, 1, 'unique env prefix');
  const arm64 = id.endsWith('_arm64');
  assert.equal(target.architecture, arm64 ? 'arm64' : 'x64');
  if (arm64) {
    assert.equal(target.setdll_name, 'setdll-x64.exe', 'patcher must run on the x64 build host');
    assert.match(target.provider.request.os, /arch="arm64"/);
    assert.match(target.provider.request.os, /version="10\.0\.26100\.1742"/);
    assert.match(target.provider.request.app, id.includes('stable') ? /ap="arm64-stable"/ : /ap="1\.1-beta-arch_arm64"/);
  }
  // Distinct sample versions expose incorrect release-body regex matches.
  versions[id] = `123.456.789.${Object.keys(versions).length + 1}`;
  filenames[id] = target.archive_name.replace('{version}', versions[id]).replace('{date}', '2099-12-31');
}
for (const [id, target] of targets) {
  const matcher = new RegExp(target.release.asset_match, 'i');
  for (const [owner, filename] of Object.entries(filenames)) {
    assert.equal(matcher.test(filename), owner === id, `${id} must only match its own archive, not ${owner}`);
  }
}
const body = config.release.body.replace(/\{(chrome_\w+)_version\}/g, (_, id) => versions[id]);
for (const [id, target] of targets) {
  assert.equal(new RegExp(target.release.version_pattern).exec(body)?.[1], versions[id], `${id}: release version round trip`);
}
console.log('Configuration passed: four targets, unique prefixes, disjoint assets, ARM64 Omaha parameters, release round trips.');
