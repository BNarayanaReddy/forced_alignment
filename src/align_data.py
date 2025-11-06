import os
import subprocess
import argparse
from select_dict import get_best_dict
from get_models import get_models_by_lang


def align_with_top_models(corpus_dir: str, oov_summary_file: str, output_dir: str, lang: str, top_k: int = 3):
    top_dictionaries = get_best_dict(oov_summary_file, k=top_k)
    print(f"Top dicts: {top_dictionaries}")

    available_acoustic_models, _ = get_models_by_lang(lang)
    print(f"Available acoustic models for '{lang}': {available_acoustic_models}")

    fallback_model = f"{lang}_mfa" 
    if fallback_model not in available_acoustic_models:
        print(f"Warning: Fallback model '{fallback_model}' is not available locally.")
        fallback_model = None

    for dictionary in top_dictionaries:
        acoustic_model_to_use = None
        # Get more relevant acoustic model
        if dictionary in available_acoustic_models:
            acoustic_model_to_use = dictionary
        # Choose other if not avail
        else:
            acoustic_model_to_use = fallback_model

        alignment_output_dir = os.path.join(output_dir, f"{dictionary}_aligned") # save alignments to {dictionary}_aligned folder
        os.makedirs(alignment_output_dir, exist_ok=True)

        

        command = [
            "mfa", "align",
            corpus_dir,
            dictionary,
            acoustic_model_to_use,
            alignment_output_dir,
            "--clean" 
        ]

        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True, text=True, capture_output=True)
        
        print(f"Textgrids saved at: {alignment_output_dir}")
        print(f"Alignment successful for dictionary: '{dictionary}'")

    print("\n Alignment process finished \n")


# if __name__ == "__main__":
    
#     align_with_top_models(
#             "/home/narayana/Projects/iiit_ssmt/mfa_alignment/data/example_corpus",
#             "/home/narayana/Projects/iiit_ssmt/mfa_alignment/run3/output/validation_oov_summary.txt",
#             "run3/final_alignment_output",
#             "english",
#             3
#         )
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=str)
    parser.add_argument("oov_summary_file", type=str)
    parser.add_argument("output_dir", type=str)
    parser.add_argument("lang", type=str)
    parser.add_argument("top_k", type=int, default=3)
    args = parser.parse_args()

    align_with_top_models(
        args.corpus_dir,
        args.oov_summary_file,
        args.output_dir,
        args.lang,
        args.top_k
    )

