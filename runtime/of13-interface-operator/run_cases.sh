#!/usr/bin/env bash
set -eo pipefail

phase=environment
trap 'status=$?; printf "phase=%s\nexit_code=%s\n" "$phase" "$status" > /probe/run-script-state.txt' EXIT

source /opt/openfoam13/etc/bashrc > /probe/log.openfoam-environment 2>&1
set -eo pipefail

{
    printf 'WM_PROJECT=%s\nWM_PROJECT_VERSION=%s\nWM_OPTIONS=%s\n' \
        "$WM_PROJECT" "$WM_PROJECT_VERSION" "$WM_OPTIONS"
    foamVersion
    g++ --version
    uname -a
} > /probe/runtime-environment.log 2>&1
dpkg-query -W -f='${binary:Package}\t${Version}\n' > /probe/package-inventory.log 2>&1
while IFS= read -r relative_path; do
    sha256sum "/opt/openfoam13/$relative_path"
done < /probe/app/package-source-paths.txt > /probe/package-source-sha256.log

phase=build
cd /probe/app
wmake > /probe/build.log 2>&1
test -x /probe/interfaceOperatorProbe
sha256sum /probe/interfaceOperatorProbe > /probe/binary-sha256.txt
ldd /probe/interfaceOperatorProbe > /probe/linked-libraries.log 2>&1
awk '/=> \// {print $3} /^\// {print $1}' /probe/linked-libraries.log \
    | sort -u | xargs -r sha256sum > /probe/linked-library-sha256.log

for nx in 16 32 64; do
    case_directory="/probe/cases/nx${nx}"
    phase="nx${nx}-blockMesh"
    blockMesh -case "$case_directory" > "$case_directory/log.blockMesh" 2>&1
    phase="nx${nx}-operator"
    /probe/interfaceOperatorProbe -case "$case_directory" \
        > "$case_directory/log.interfaceOperatorProbe" 2>&1
    grep -Fqx INTERFACE_OPERATOR_PROBE_COMPLETE "$case_directory/log.interfaceOperatorProbe"
    for output in arithmetic/before.json arithmetic/after.json \
                  harmonic/before.json harmonic/after.json constant/before.json; do
        test -s "$case_directory/probe/$output"
    done
done

phase=complete
printf '%s\n' RUN_CASES_COMPLETE > /probe/COMPLETED
