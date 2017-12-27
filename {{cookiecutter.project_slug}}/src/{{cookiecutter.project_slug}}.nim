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

# Uncomment the next line to include and show banner.txt
# include banner

let args = docopt(doc, version = "{{cookiecutter.version}}")

let name = $args["--name"]

echo "Hello, " & name & "."
