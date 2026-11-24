#!/usr/bin/env bash
# ==============================================================================
# Renovate Bot Configuration Schema Validator
# Runs local schema validation and regex verification.
# ==============================================================================

set -euo pipefail

echo "==========================================================="
echo "       RENOVATE CONFIGURATION SCHEMA VALIDATION            "
echo "==========================================================="

if command -v renovate-config-validator >/dev/null 2>&1; then
    echo "[*] Executing renovate-config-validator CLI..."
    renovate-config-validator --strict renovate.json
else
    echo "[*] Validating renovate.json JSON syntax and schema fields via Python..."
    python3 -c "
import json, sys, re

with open('renovate.json') as f:
    cfg = json.load(f)

assert '$schema' in cfg, 'Missing $schema'
assert 'packageRules' in cfg, 'Missing packageRules'
assert 'customManagers' in cfg, 'Missing customManagers'

# Test custom regex compilation (convert JS (?<group>...) to Python (?P<group>...))
for cm in cfg['customManagers']:
    for s in cm.get('matchStrings', []):
        py_compat = re.sub(r'\(\?<([a-zA-Z0-9_]+)>', r'(?P<\1>', s)
        try:
            re.compile(py_compat)
            print(f'  [PASS] Regex valid: {s[:50]}...')
        except re.error as e:
            print(f'  [FAIL] Regex error: {e}', file=sys.stderr)
            sys.exit(1)

print('[SUCCESS] All regex managers and schema fields valid.')
"
fi

echo "[OK] Renovate configuration validation complete."
exit 0
