import os
import subprocess
from typing import List
from utils import clean_mfa_out
from dotenv import load_dotenv
import argparse

load_dotenv(override=True)


def get_models_by_lang(lang: str) -> List[tuple]:
    token_args = []
    github_token = os.environ.get("MFA_GITHUB_TOKEN")
    if github_token:  # to increase dwnld limit
        token_args = ["--github_token", github_token]

    command = ["mfa", "model", "download"]

    acoustic_cmd = command + ["acoustic"] + token_args
    dict_cmd = command + ["dictionary"] + token_args

    acoustic_models = subprocess.run(acoustic_cmd, capture_output=True, text=True)
    phone_dicts = subprocess.run(dict_cmd, capture_output=True, text=True)

    acoustic_data = clean_mfa_out(acoustic_models)
    dict_clean = clean_mfa_out(phone_dicts)

    acoustic_models = [model for model in acoustic_data if lang in model]
    dictionaries = [d for d in dict_clean if lang in d]

    # Models we have locally
    check_dwnlds_cmd = ["mfa", "model", "list"]
    acoustic_dwnlds_cmd = check_dwnlds_cmd + ["acoustic"]
    dict_dwnlds_cmd = check_dwnlds_cmd + ["dictionary"]

    acoustic_dwnlds = subprocess.run(
        acoustic_dwnlds_cmd, capture_output=True, text=True
    )
    acoustic_dwnlds = clean_mfa_out(acoustic_dwnlds)

    dict_dwnlds = subprocess.run(dict_dwnlds_cmd, capture_output=True, text=True)
    dict_dwnlds = clean_mfa_out(dict_dwnlds)

    for acoustic_model in acoustic_models:
        if acoustic_model not in acoustic_dwnlds:
            print(f"Downloading {acoustic_model}")
            dwnld_model = acoustic_cmd + [acoustic_model]
            subprocess.run(dwnld_model)
            print(f"Downloaded {acoustic_model}")

    for dict in dictionaries:
        if dict not in dict_dwnlds:
            print(f"Downloading {dict}")
            dwnld_model = dict_cmd + [dict]
            subprocess.run(dwnld_model)
            print(f"Downloaded {dict}")

    return (acoustic_models, dictionaries)


if __name__ == "__main__":
    # lang = "english"
    # models, dicts = get_models_by_lang(lang)
    # print(f"Final models for {lang}: {models}")
    # print(f"Final dictionaries for {lang}: {dicts}")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", type=str)
    args = parser.parse_args()
    lang = args.lang
    models, dicts = get_models_by_lang(lang)
    print(f"Final models for {lang}: {models}")
    print(f"Final dictionaries for {lang}: {dicts}")
