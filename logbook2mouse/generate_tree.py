def generate_tree(data, omit_keys=None, indent=0):
    """
    Recursively generate a tree representation of nested dictionaries or objects.

    :param data: The dictionary or object to represent.
    :param omit_keys: Keys to omit from the tree (supports nested keys with ':').
    :param indent: Current indentation level (used internally for recursion).
    :return: String representing the tree.
    """
    if omit_keys is None:
        omit_keys = []

    def should_omit(key_path):
        return any(key_path.startswith(ok) for ok in omit_keys)

    tree_lines = []
    prefix = "    " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            key_path = f"{key}" if indent == 0 else f"{key}"
            if should_omit(key_path):
                continue
            if isinstance(value, (dict, list)) or hasattr(value, "__attrs_attrs__"):
                tree_lines.append(f"{prefix}{key}:")
                tree_lines.append(generate_tree(value, omit_keys, indent + 1))
            else:
                tree_lines.append(f"{prefix}{key}: {value}")
    elif hasattr(data, "__attrs_attrs__"):
        for field in data.__attrs_attrs__:
            key = field.name
            key_path = f"{key}" if indent == 0 else f"{key}"
            if should_omit(key_path):
                continue
            value = getattr(data, key)
            if isinstance(value, (dict, list)) or hasattr(value, "__attrs_attrs__"):
                tree_lines.append(f"{prefix}{key}:")
                tree_lines.append(generate_tree(value, omit_keys, indent + 1))
            else:
                tree_lines.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            tree_lines.append(generate_tree(item, omit_keys, indent + 1))
    else:
        tree_lines.append(f"{prefix}{data}")

    return "\n".join(tree_lines)