import json
import os


def all_settings(file="./setting.json"):
    default_settings = {
        "persist_path": "./qdrant_data",
        "data_sources": [
            {"type": "folder", "path": "./sample_data/folder_1/*"},
            {"type": "file", "path": "./sample_data/file_1.csv"},
            {"type": "email", "path": "./sample_data/email_data"},
            {"type": "calendar", "path": "./sample_data/email_data"}
        ]
    }

    # check if file exists in location, otherwise create a file with that name
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write(json.dumps(default_settings, indent=4))
        settings = default_settings
    else:
        with open(file, "r") as f:
            settings = json.load(f)

    return(settings)
