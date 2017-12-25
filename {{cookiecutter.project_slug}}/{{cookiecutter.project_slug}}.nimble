# Package

version       = "{{cookiecutter.version}}"
author        = "{{cookiecutter.full_name}}"
description   = "{{cookiecutter.project_short_description}}"
license       = "MIT"
installFiles = @["{{cookiecutter.project_slug}}.nim"]
bin = @["{{cookiecutter.project_slug}}"]
binDir = "bin"
srcDir = "src"
skipExt = @["nim"]

# Dependencies

requires "nim >= 0.17.2"
requires "docopt"

# Tasks

task test, "Run test suite":
  exec "nim c -r tests/tester"
