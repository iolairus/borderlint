## 1. Additive KB merge (jurisdiction-classification)

- [ ] 1.1 Load the bundled KB, then merge a user-supplied KB on top — append providers; user entries override on a host/SDK/package conflict
- [ ] 1.2 Support a flat `endpoints` map (`host → jurisdiction`) in the user file, merged additively, validating each jurisdiction against the recognised token set (ccTLD/ISO + `CN-GBA`/`GBA`/`local`/`unknown`) and erroring on an unrecognised token

## 2. Tests & docs

- [ ] 2.1 Tests: bundled providers still resolve when a custom KB is supplied; an internal `endpoints` map resolves each host (cn/sg/hk) to its jurisdiction; a user override of a bundled host (and of a bundled provider) wins; an invalid jurisdiction token is rejected; a wrong-endpoint config is a violation under a strict allow-list (via existing deny-by-default)
- [ ] 2.2 Add an example internal-endpoints file and a README note on the multi-region wrong-endpoint guard
