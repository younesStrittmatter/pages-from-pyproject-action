import sys
import toml

def create_index(file):
    # Read information from project.yml
    with open(file, "r") as f:
        pyproject = toml.load(f)
    markdown = ''
    markdown += f"# {pyproject['project']['name']}\n\n"
    markdown += f"{pyproject['project']['description']}\n\n"
    markdown += f"GitHub repository: [{pyproject['project']['urls']['repository']}]({pyproject['project']['urls']['repository']})\n\n"
    markdown += "### Authors:\n\n"
    for a in pyproject['project']['authors']:
        markdown += f"[{a['name']}](mailto:{a['email']})\n\n"

    return markdown

def create_quick_start(file):
    with open(file, "r") as f:
        pyproject = toml.load(f)
    project = pyproject['project']
    markdown = ''
    markdown += "# Quickstart Guide\n\n"
    markdown += "You will need:\n"
    markdown += f"`python` {project['requires-python']}: [https://www.python.org/downloads/](https://www.python.org/downloads/)\n\n"
    markdown += "!!! It is recommended to use a python environment manger like virtualenv\n\n"
    markdown += "Install the package via pip:\n\n"
    markdown += "```shell\n"
    pip_package_autora = "autora[{}]".format(project['name'].replace("-", "", 1))
    markdown += f"pip install \"{pip_package_autora}\"\n"
    markdown += "```\n\n"
    markdown += 'Check your installation by running:\n\n'
    markdown += "```shell\n"
    markdown += "```\n\n"
    markdown += '## Dependencies\n\n'
    for d in project['dependencies']:
        markdown += f"{d}, "
    markdown = markdown[:-2]
    markdown += '\n'
    return markdown



if __name__ == "__main__":
    src = sys.argv[1]
    out_index = sys.argv[2]
    out_quick = sys.argv[3]
    with open(out_index, 'w') as f:
        f.write(create_index(src))
    with open(out_quick, 'w') as f:
        f.write(create_quick_start(src))
