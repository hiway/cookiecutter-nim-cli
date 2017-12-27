import os
import unittest
import osproc
import sequtils
import future
import strutils


suite "Test cookiecutter-nim-cli":

  test "Execute cookiecutter":
    discard execCmdEx("rm -r tests/testproject")
    let cmd_out = execCmdEx("cd tests && python3 ../tests/cookierun.py")
    check:
      $cmd_out.output.strip == ""
      existsDir("tests/testproject")
      existsFile("tests/testproject/testproject.nimble")

  test "Execute nimble build inside testproject":
    let cmd_out = execCmdEx("cd tests/testproject && nimble build")
    check:
      cmd_out.output.find("testproject/testproject using c backend") > 0

  test "Execute testproject cli":
    let cmd_out = execCmdEx("tests/testproject/bin/testproject")
    echo cmd_out.output.strip
    check:
      cmd_out.output.find("TestProject") == 0
      cmd_out.output.find("---") > 0
      cmd_out.output.find("Hello, world.") > 0

  test "Execute testproject tests":
    let cmd_out = execCmdEx("cd tests/testproject && nimble test")
    echo cmd_out.output.strip

