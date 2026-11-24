#!/usr/bin/env bash
set -euo pipefail

echo "=== Renovate Bot Suite Healthcheck ==="
python3 --version
bash scripts/validate-config.sh
echo "[OK] Healthcheck passed."
exit 0
