# Montreal Forced Aligner (MFA) Project

## Project Overview

This project provides **Forced Alignment using Montreal Forced Aligner (MFA)** on an audio dataset. The goal is to generate time-aligned phonetics and word level transcriptions from audio files and their corresponding text transcripts.

## 1. Environment Setup

### Prerequisite
- Conda environment (version used: 24.9.2)

### Installing Montreal Forced Aligner
- Instructions to install MFA.
- Create conda environment:
```bash
cd forced_alignment
mkdir envs
conda create --prefix envs/mfa_env python=3.11
conda activate envs/mfa_env
conda install -c conda-forge montreal-forced-aligner
```
- Used latest (version: 3.3.8) montreal-forced-aligner

## 2. Data Preparation

- Place your audio and text files in `data/`, such that the **`basename of corresponding files`** should be same except extension

```
data
|-- /example_corpus
|   |-- F2BJRLP1.wav
|   |-- F2BJRLP1.txt
|   |-- F2BJRLP2.wav
|   |-- F2BJRLP2.txt
|   |-- F2BJRLP3.wav
|   |-- F2BJRLP3.txt
    ...
```
- Note:
  - `*.wav`: Audio files.
  - `*.txt`: Corresponding text transcriptions.


## 3-1. Align with pre-trained models - Option 1

### a. Retrieve TOP dictionaries
- Decide the top dictionaries based on the number of oov (out-of-vocabulary) words
- Usage
  ```bash
  python src/validate_dicts.py `input_dir` `out_dir` `lang`
  ```

- Example:
  ```bash
  python src/validate_dicts.py --input_dir "data/example_corpus" --out_dir "egs/validation_output" --lang "english"
  ```

### b. Align the Data for Top 3 Dictionaries
- Perform the forced alignment on the audio and transcription files using the top dictionaries we get from validation
- Usage:
  ```bash
  python src/align_data.py `input_dir` `oov_summary_file` `lang` `top_k`
  ```

- Example:
  ```bash
  python src/align_data.py --input_dir "data/example_corpus" --oov_summary_file "egs/validation_output/validation_oov_summary.txt" --lang "english" --top_k 3
  ```

## 3-2. Align with Pre-trained Models - Option 2
- Perform validation and alignment using a single bash file
- Example:
  ```bash
  bash egs/align_data.sh
  ```

## 4. Training Custom Dictionary: 
- As the corpus goes on increasing the number of out-of vocabulary words also increases.
- Token for OOV words corresponding phonemes - `spn`
- Using a pre-trained G2P (grapheme to Phoneme) model, we can estimate pronounciation for those OOVs
- By combining G2P generated dict for OOVs can be combined with the pre-trained to perform the alignments
- Usage:
  ```bash
  python src/train_dict.py `txt_dir` `corpus_dir` `base_dictionary` `g2p_model` `acoustic_model` `output_dir`
  ```

- Example
  ```bash
  python src/train_dict.py --txt_dir "data/txt_corpus" --corpus_dir "data/example_corpus" --base_dictionary "dictionaries/english_us_arpa.dict" --g2p_model "english_us_arpa" --acoustic_model "english_us_arpa" --output_dir "egs/custom_dict/aligned_data"
  ```

