let doc = """
{{cookiecutter.project_slug}}

Usage:
  {{cookiecutter.project_slug}} [options]

Options:
  -h --help         Show this screen.
  --version         Show version.
  --name=<name>     EXAMPLE: Your name [default: world]
"""
import docopt
include constants

echo banner_txt
echo "---"

let args = docopt(doc, version = "{{cookiecutter.version}}")

let name = $args["--name"]

echo "Hello, " & name & "."
