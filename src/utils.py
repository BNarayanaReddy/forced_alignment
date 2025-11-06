import os
import shutil
import re
import ast


def copy_file(oov_file, out_fldr):
    if os.path.exists(oov_file):
        shutil.copy(oov_file, out_fldr)
        print(f"Copied OOV file to {out_fldr}")
    else:
        print("No OOV file found.")


def clean_mfa_out(std_out):
    try:
        clean = re.sub(r"\x1b\[[0-9;]*m", "", std_out.stdout).replace("│", "").strip()
        clean = ast.literal_eval(clean)
    except Exception as e:
        print(f"Warning: Could not parse local models/dictionaries: {std_out.stderr}")
    return clean


def write_oov(data, filepath):
    with open(filepath, "w") as f:
        for model_combo, oov_data in data.items():
            f.write(f"Model Combination: {model_combo}\n")
            for oov_word, freq in oov_data.items():
                f.write(f"{oov_word}\t{freq}\n")
            f.write("\n")


def combine_dictionaries(generated_dict, pretrained_dict, combined_dict):
    with open(combined_dict, "w") as combined:
        # Copy pre-trained dictionary
        with open(pretrained_dict, "r") as pretrained:
            combined.write(pretrained.read())

        # Combine with G2P-generated pronunciations
        with open(generated_dict, "r") as g2p:
            combined.write(g2p.read())
