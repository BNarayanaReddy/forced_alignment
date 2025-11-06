import sys
import argparse
import collections


def get_best_dict(filename: str, k: int = 3):
    model_oov_totals = collections.defaultdict(int)
    current_model_name = None
    try:
        with open(filename, "r") as f:
            for line_number, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                if line.startswith("Model Combination:"):
                    current_model_name = line.split("Model Combination:")[1].strip()
                    if current_model_name not in model_oov_totals:
                        model_oov_totals[current_model_name] = 0
                elif current_model_name:
                    parts = line.split("\t")
                    if len(parts) == 2:
                        count = int(parts[1].strip())
                        model_oov_totals[current_model_name] += count
                    else:
                        print(f"Summary is corrupted at line {line_number+1}: {line}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return
    if not model_oov_totals:
        print("No model data was found in the file.")
        return

    sorted_models = sorted(model_oov_totals.items(), key=lambda item: item[1])
    for rank, (model_name, count) in enumerate(sorted_models):
        print(f"{rank+1}. {model_name}:\t{count} OOVs")
    print(f"\n--- Top {k} Models ---")

    output = []
    for rank, (model_name, count) in enumerate(sorted_models[:k]):
        print(f"{rank+1}. {model_name}:\t{count} OOVs")
        output.append(model_name)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("summary_file", type=str)
    parser.add_argument("top_k", type=int, default=3)
    # INPUT_FILE = "/home/narayana/Projects/iiit_ssmt/mfa_alignment/run3/output/validation_oov_summary.txt"
    args = parser.parse_args()
    INPUT_FILE = args.oov_summary_file
    top_k = args.top_k
    top_dicts = get_best_dict(INPUT_FILE, top_k)
