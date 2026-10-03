#!/usr/bin/env bash
# Resume the same immutable package after partial transfers; trust only its hash.
set -euo pipefail
package_url="$1"
package_sha256="$2"
package_destination="$3"
for package_attempt in {1..12}; do
    if test -f "$package_destination" && printf '%s  %s\n' "$package_sha256" "$package_destination" | sha256sum -c -; then
        exit 0
    fi
    printf 'Pinned package download attempt %s (resume any partial file)\n' "$package_attempt"
    curl --fail --location --connect-timeout 20 --max-time 120 --retry 0 \
        --continue-at - "$package_url" --output "$package_destination" || true
done
printf '%s  %s\n' "$package_sha256" "$package_destination" | sha256sum -c -
