# Package

version       = "0.2.0"
author        = "Harshad Sharma"
description   = "Nim cli cookiecutter."
license       = "MIT"

# Dependencies

requires "nim >= 0.17.2"

# Tasks

task test, "Run test suite":
  exec "nim c -r tests/tester"
