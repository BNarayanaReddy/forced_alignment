#!/bin/bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/..")

CORPUS_DIR="$PROJECT_ROOT/data/example_corpus"
VALIDATION_OUTPUT_DIR="$SCRIPT_DIR/validation_output"
ALIGNMENT_OUTPUT_DIR="$SCRIPT_DIR/aligned_data"
LANG="english"
TOP_K="3"

echo $CORPUS_DIR
echo $VALIDATION_OUTPUT_DIR
echo $ALIGNMENT_OUTPUT_DIR

OOV_SUMMARY_FILE="$VALIDATION_OUTPUT_DIR/validation_oov_summary.txt"

mkdir -p "$VALIDATION_OUTPUT_DIR"
mkdir -p "$ALIGNMENT_OUTPUT_DIR"

echo "Step 1: Validating dictionaries to find the best performers"
python3 "$PROJECT_ROOT/src/validate_dicts.py" \
    "$CORPUS_DIR" \
    "$VALIDATION_OUTPUT_DIR" \
    --lang "$LANG"

echo "Validation complete. OOV summary written to $OOV_SUMMARY_FILE"

echo "Step 2: Running alignment with the top $TOP_K dictionaries"
python3 "$PROJECT_ROOT/src/align_data.py" \
    "$CORPUS_DIR" \
    "$OOV_SUMMARY_FILE" \
    "$ALIGNMENT_OUTPUT_DIR" \
    "$LANG" \
    "$TOP_K"

echo "Alignment process finished"
echo "TextGrids are saved in subdirectories within: $ALIGNMENT_OUTPUT_DIR"