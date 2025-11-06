import os
import subprocess
import shutil
import argparse
from utils import copy_file, write_oov
from get_models import get_models_by_lang


def validate_mfa_models(
    input_dir, out_dir, temp_fldr="tmp/mfa_validate", lang="english", debug=True
):
    _, dictionaries = get_models_by_lang(lang)
    corpus_name = os.path.basename(input_dir)

    if not os.path.exists(temp_fldr):
        os.makedirs(temp_fldr, exist_ok=True)
        print(f"Created temporary directory: {temp_fldr}")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        print(f"Created out directory: {out_dir}")

    output = {}

    for dictionary in dictionaries:
        command = [
            "mfa",
            "validate",
            input_dir,
            dictionary,
            "--clean",
            "--no_final_clean",
            "-t",
            temp_fldr,
            "--ignore_acoustics",
        ]
        try:
            result = subprocess.run(command)
            oov_file = [
                os.path.join(temp_fldr, corpus_name, file)
                for file in os.listdir(os.path.join(temp_fldr, corpus_name))
                if file.startswith("oov_counts")
            ][0]

            if debug:
                out_fldr = os.path.join(out_dir, dictionary)
                if not os.path.exists(out_fldr):
                    os.makedirs(out_fldr, exist_ok=True)
                copy_file(oov_file, out_fldr)
            oovs_freq = {}
            with open(oov_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, freq = line.split()
                    oovs_freq[key] = freq

            print(oovs_freq)

            output[dictionary] = oovs_freq

        except Exception as e:
            print(e)
    oov_summary_file = os.path.join(out_dir, "validation_oov_summary.txt")
    write_oov(output, oov_summary_file)
    # print(output)

    return oov_summary_file


# if __name__ == "__main__":
#     input_dir = "/home/narayana/Projects/iiit_ssmt/mfa_alignment/data/example_corpus"
#     out_dir = "/home/narayana/Projects/iiit_ssmt/mfa_alignment/run3/output"
#     temp_fldr = "/home/narayana/Projects/iiit_ssmt/mfa_alignment/run3/temp"
#     lang = "english"
#     validate_mfa_models(input_dir, out_dir, temp_fldr=temp_fldr, lang=lang, debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str)
    parser.add_argument("out_dir", type=str)
    parser.add_argument("--temp_fldr", type=str, default="tmp/mfa_validate")
    parser.add_argument("--lang", type=str, default="english")
    parser.add_argument("--debug", default=False)

    args = parser.parse_args()

    oov_summary_file = validate_mfa_models(
        args.input_dir,
        args.out_dir,
        temp_fldr=args.temp_fldr,
        lang=args.lang,
        debug=args.debug,
    )
