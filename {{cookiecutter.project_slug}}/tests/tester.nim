import unittest
import osproc
import sequtils
import future
import strutils

const src_path = "./src/{{cookiecutter.project_slug}}.nim"
const bin_path = "./bin/{{cookiecutter.project_slug}}"

# Compile binaries
doAssert execCmdEx("nim c -o:" & bin_path & " " & src_path).exitCode == QuitSuccess


proc runCli(args: varargs[string]): tuple[output: string, exitCode: int] =
  var quotedArgs = @args
  quotedArgs.insert(bin_path)
  quotedArgs = quoted_args.map((x: string) => ("\"" & x & "\""))
  result = execCmdEx(quotedArgs.join(" "))
  checkpoint(result.output)


suite "Test cli":
  let
    default_output = "Hello, world."
    test_name = "Tester"
    test_output = "Hello, Tester."

  test "Execute default":
    let cmd_out = runCli()
    check:
      cmd_out.output.strip.find(default_output) > 0

  test "Execute with --name":
    let cmd_out = runCli("--name=" & test_name)
    check:
      cmd_out.output.strip.find(test_output) > 0
