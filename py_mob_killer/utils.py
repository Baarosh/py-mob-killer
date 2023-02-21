from yaml import safe_load as yaml_safe_load, safe_dump as yaml_safe_dump, YAMLError


def load_yaml_document(path):
    with open(path, "r") as stream:
        try:
            return yaml_safe_load(stream)
        except YAMLError as exc:
            # log instead
            print(f"Failed to load yaml document. Traceback: {exc}")


def dump_yaml_document(data, path):
    with open(path, "w") as stream:
        try:
            yaml_safe_dump(data, stream)
        except YAMLError as exc:
            # log instead
            print(f"Failed to dump yaml document. Traceback: {exc}")
