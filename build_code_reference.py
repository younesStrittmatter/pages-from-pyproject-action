import os
import ast
import re
import sys


def process_file(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    markdown_text = generate_markdown(tree)
    return markdown_text


def get_node_source(node):
    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
        arg_list = []
        defaults = node.args.defaults

        num_args_with_defaults = len(defaults)
        num_args_without_defaults = len(node.args.args) - num_args_with_defaults

        arg_str_list = []

        for idx, arg in enumerate(node.args.args):
            arg_name = arg.arg
            arg_type = ast.unparse(arg.annotation) if arg.annotation else ""

            if idx >= num_args_without_defaults:
                default_idx = idx - num_args_without_defaults
                default_value = ast.unparse(defaults[default_idx])
            else:
                default_value = None

            arg_list.append((arg_name, arg_type, default_value))

            if arg_type:
                arg_type_str = f"{arg_name}: {arg_type}"
            else:
                arg_type_str = arg_name

            if default_value is not None:
                arg_str_list.append(f"{arg_type_str} = {default_value}")
            else:
                arg_str_list.append(arg_type_str)

        args_str = ", ".join(arg_str_list)
        return f"def {node.name}({args_str})", arg_list
    elif isinstance(node, ast.ClassDef):
        return f"class {node.name}", []
    else:
        return "", []




def parse_docstring(docstring):
    description = ""
    arguments = {}
    examples = []
    return_value = ""

    lines = [line.strip() for line in docstring.split("\n")]

    param_pattern = re.compile(r":param (\w+): (.+)")
    return_pattern = re.compile(r":return: (.+)")

    mode = "description"
    for line in lines:
        if mode == "description":
            if line.startswith(":param"):
                mode = "params"
            elif line.startswith("Examples:"):
                mode = "examples"
            else:
                description += f"{line}\n"

        if mode == "params":
            param_match = param_pattern.match(line)
            if param_match:
                param_name, param_desc = param_match.groups()
                arguments[param_name] = param_desc
            elif line.startswith(":return:"):
                mode = "return"

        if mode == "return":
            return_match = return_pattern.match(line)
            if return_match:
                return_value = return_match.group(1)

        if mode == "examples":
            if line.startswith("-"):
                examples.append(line[1:].strip())

    return description, arguments, examples, return_value


def generate_markdown(tree):
    markdown = ""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definition, arg_list = get_node_source(node)
            docstring = ast.get_docstring(node)

            if docstring:
                description, arguments, examples, return_value = parse_docstring(docstring)

                markdown += f"## {definition}\n\n"
                markdown += f"{description}\n\n"

                if arguments or arg_list:
                    markdown += "### Arguments\n\n"
                    markdown += "| Name | Type | Description | Default |\n"
                    markdown += "|------|------|-------------|---------|\n"
                    for arg_name, arg_type, arg_default in arg_list:
                        arg_desc = arguments.get(arg_name, "")
                        markdown += f"| {arg_name} | {arg_type} | {arg_desc} | {arg_default} |\n"
                    markdown += "\n"

                if return_value:
                    markdown += f"### Returns\n\n{return_value}\n\n"

                if examples:
                    markdown += "### Examples\n\n"
                    for example in examples:
                        markdown += f"- {example}\n"
                    markdown += "\n"

            if isinstance(node, ast.ClassDef):
                for child_node in node.body:
                    if isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        markdown += generate_markdown(child_node)
    return markdown


def walk_directory(directory, out):
    markdown = ""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                markdown += process_file(file_path)
    with open(out, 'w') as f:
        f.write(markdown)


if __name__ == "__main__":
    src = sys.argv[1]
    out = sys.argv[2]

    
    start_directory = "src"
    walk_directory(src, out)
