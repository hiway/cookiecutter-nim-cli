# Package

version       = "{{cookiecutter.version}}"
author        = "{{cookiecutter.full_name}}"
description   = "{{cookiecutter.project_short_description}}"
license       = "MIT"
installFiles = @["{{cookiecutter.project_slug}}.nim"]
bin = @["{{cookiecutter.project_slug}}"]
srcDir = "src"

# Dependencies

requires "nim >= 0.17.2", "docopt"

