import subprocess
import os
import argparse
from utils import combine_dictionaries


def generate_dictionary(corpus_dir, g2p_model, output_dict_path, base_dictionary):
    dwnld_g2p = [
        "mfa", "model", "download", "g2p", g2p_model
    ]
    subprocess.run(dwnld_g2p, check=True)
    print(f"Downloaded G2P model")
    command = [
        "mfa",
        "g2p",
        corpus_dir,
        g2p_model,
        output_dict_path,
        "--num_pronunciations",
        "1",
        "--dictionary_path",
        base_dictionary,
    ]

    subprocess.run(command, check=True)
    print(f"Generated dictionary saved to: {output_dict_path}")


def train_dictionary(corpus_dir, combined_dict_path, acoustic_model, output_dict_path):
    command = [
        "mfa",
        "train_dictionary",
        corpus_dir,
        combined_dict_path,
        acoustic_model,
        output_dict_path,
        "--clean",
    ]
    print(f"Training dictionary")
    subprocess.run(command, check=True)
    out_dict_path = os.path.join(output_dict_path, os.path.basename(combined_dict_path))
    print(f"Trained dictionary model saved to: {out_dict_path}")


def align_with_trained_model(
    corpus_dir, trained_dict_path, acoustic_model, output_alignment_path
):
    command = [
        "mfa",
        "align",
        corpus_dir,
        trained_dict_path,
        acoustic_model,
        output_alignment_path,
        "--clean",
    ]
    print(f"Running alignment: {' '.join(command)}")
    subprocess.run(command, check=True)
    print(f"Alignments saved to: {output_alignment_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a dictionary and align a corpus using MFA."
    )
    parser.add_argument(
        "txt_dir", type=str, help="Path to the text only corpus directory."
    )
    parser.add_argument("corpus_dir", type=str, help="Path to the corpus directory.")
    parser.add_argument(
        "base_dictionary",
        type=str,
        help="Path to the base dictionary (e.g., english_us_arpa).",
    )
    parser.add_argument(
        "g2p_model", type=str, help="Name of the G2P model to use (e.g., english_g2p)."
    )
    parser.add_argument(
        "acoustic_model",
        type=str,
        help="Name of the acoustic model to use for alignment (e.g., english_us_arpa).",
    )
    parser.add_argument("output_dir", type=str, help="Directory to save all outputs.")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    generated_dict_path = os.path.join(args.output_dir, "generated.dict")
    combined_dict_path = os.path.join(args.output_dir, "combined.dict")
    trained_dict_output_path = os.path.join(args.output_dir, "trained_dictionary_model")
    final_alignment_path = os.path.join(args.output_dir, "final_alignments")

    # Step 1: Generate a dictionary from corpus OOVs
    generate_dictionary(
        args.txt_dir,
        args.g2p_model,
        generated_dict_path,
        base_dictionary=args.base_dictionary,
    )

    # Step 2: Combine the base dictionary with the newly generated one
    print(
        f"Combining {args.base_dictionary} and {generated_dict_path} into {combined_dict_path}"
    )
    combine_dictionaries(args.base_dictionary, generated_dict_path, combined_dict_path)

    # Step 3: Train a new dictionary model
    train_dictionary(
        args.corpus_dir, combined_dict_path, args.g2p_model, trained_dict_output_path
    )

    # Step 4: Align using the newly trained dictionary
    final_trained_dict = os.path.join(
        trained_dict_output_path, os.path.basename(combined_dict_path)
    )
    align_with_trained_model(
        args.corpus_dir, final_trained_dict, args.acoustic_model, final_alignment_path
    )

    print("\nProcess finished successfully.")
