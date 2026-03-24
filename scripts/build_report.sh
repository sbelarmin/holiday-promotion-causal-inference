#!/bin/bash
set -e

echo "Building report..."

INPUT="reports/writeup/common_causal_traps.md"
OUTPUT="reports/common_causal_traps.html"

pandoc "$INPUT" \
-o "$OUTPUT" \
--standalone \
--toc \
--embed-resources \
--resource-path="reports:reports/writeup" \
--metadata title="Common Causal Traps" \
--css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.css

echo "Report built: $OUTPUT"