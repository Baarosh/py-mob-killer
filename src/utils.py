
from yaml import safe_load as yaml_safe_load, YAMLError
from typing import Dict, Optional

def load_yaml_document(path: str) -> Optional[Dict[str, Optional[int]]]:
    with open(path, "r") as stream:
        try:
            return yaml_safe_load(stream)
        except YAMLError as exc:
            # log instead
            print(f"Failed to load yaml document. Traceback: {exc}")
