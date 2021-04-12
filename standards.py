#!/usr/bin/env python3

import os
import sys
import stat
import glob
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--hook", action="store_true")
parser.add_argument("--unhook", action="store_true")
parser.add_argument("--check", action="store_true")
parser.add_argument("--fix", action="store_true")

parser.add_argument("--tool-path", default="dotnet-format")
parser.add_argument("--project-path", default="testproject")
parser.add_argument("--project-glob", default="Unity.Multiplayer.MLAPI*.csproj")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    exit(1)

args = parser.parse_args()


hook_path = "./.git/hooks/pre-push"
hook_exec = f"python3 {os.path.basename(sys.argv[0])} --check"

if args.hook:
    print("hook: execute")

    if os.path.exists(hook_path):
        print(f"hook: git pre-push hook file already exists: `{hook_path}`")
        print("hook: please make sure to backup and delete the existing pre-push hook file")
        exit("hook: failed")

    print("hook: write git pre-push hook file contents")
    hook_file = open(hook_path, "w")
    hook_file.write(f"#!/bin/sh\n\n{hook_exec}\n")
    hook_file.close()

    print("hook: make git pre-push hook file executable")
    hook_stat = os.stat(hook_path)
    os.chmod(hook_path, hook_stat.st_mode | stat.S_IEXEC)

    print("hook: succeeded")


if args.unhook:
    print("unhook: execute")

    hook_path = "./.git/hooks/pre-push"
    if os.path.isfile(hook_path):
        print(f"unhook: found file -> `{hook_path}`")
        delete = False
        hook_file = open(hook_path, "r")
        if hook_exec in hook_file.read():
            delete = True
        else:
            print("unhook: existing git pre-push hook file was not created by this script")
            exit("unhook: failed")
        hook_file.close()
        if delete:
            os.remove(hook_path)
            print(f"unhook: delete file -> `{hook_path}`")

    print("unhook: succeeded")


if args.check or args.fix:
    glob_match = os.path.join(args.project_path, args.project_glob)
    print(f"glob: looking for files matching -> {glob_match}")
    glob_files = glob.glob(glob_match)
    print(f"glob: found {len(glob_files)} matching files")


if args.check:
    print("check: execute")

    for project_file in glob_files:
        print(f"check: project -> {project_file}")
        check_exec = os.system(f"{args.tool_path} {project_file} --fix-whitespace --fix-style error --check")
        if check_exec != 0:
            exit(f"check: failed, exit code -> {check_exec}")

    print("check: succeeded")


if args.fix:
    print("fix: execute")

    for project_file in glob_files:
        print(f"fix: project -> {project_file}")
        fix_exec = os.system(f"{args.tool_path} {project_file} --fix-whitespace --fix-style error")
        if fix_exec != 0:
            exit(f"fix: failed, exit code -> {fix_exec}")

    print("fix: succeeded")
