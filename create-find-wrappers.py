#!/usr/bin/env python3

import argparse
from enum import Enum, auto
from pathlib import Path
from shutil import which

# Change if necessary
FISH_FUNCTIONS_PATH = Path().home() / ".config" / "fish" / "functions"


class FindCommand(Enum):
    FD = auto()
    FD_FIND = auto()
    FIND = auto()


find_cmds = {
    FindCommand.FD: {"name": "fdfind", "command": 'fd -i "$pat" $path'},
    FindCommand.FD_FIND: {"name": "fdfind", "command": 'fdfind -i "$pat" $path'},
    FindCommand.FIND: {"name": "find", "command": 'find $path -iname "*$pat*"'},
}

# Edit this list according to to your preferences.
# Executables not found in your PATH will be skipped
COMMANDS = ["cat", "chmod", "gnvim", "gvim", "ls", "vi", "vim", "grep", "rg", "rm", "lddtree",
            "ldd", "file"]


def get_command_template_for(find_cmd: FindCommand, **kargs) -> str:
    name = find_cmds[find_cmd]["name"]
    find_command = find_cmds[find_cmd]["command"]

    return """function {cmd}F -d "Run {name} and pass the resulting executable(s) to {cmd}."
    # All but the last two arguments are passed to "{cmd}" itself.
    set argc (count $argv)
    set cmd (status current-command)
    set args
    if test $argc -eq 0; or test $argc -eq 1
        printf "I need at least 2 argument.\nUSAGE: {cmd}F [flags-of-{cmd}] <{name}-pattern> <path-to-search>
"
        return 1
    end

    if test $argc -eq 2
        set args
    else
        set args $argv[1..-3]
    end

    set pat "$argv[-2]"
    set path "$argv[-1]"
    set files ({find_command})

    if test -z "$files"
        printf "No files found by {name}"
        return 1
    end

    echo Running "{cmd} $files"
    {cmd} $args $files
    return 0
end""".format(
        find_command=find_command, name=name, **kargs
    )


def main():
    argparse.ArgumentParser(description="Create find/fd-find fish function wrappers")

    # if `fd-find` is installed use that, otherwise use vanilla `find`.
    # fdfind may be named either fd or fdfind, depending on the distro.
    if which("fdfind"):
        find_cmd = FindCommand.FD_FIND
    elif which("fd"):
        find_cmd = FindCommand.FD
    else:
        print("fd-find not found, using vanilla find command.")
        find_cmd = FindCommand.FIND

    print("[create-find-wrappers.py:76] DEBUGGING STRING ==> ", 3)
    for cmd in COMMANDS:
        if not which(cmd):
            print(f'Cannot find executable "{cmd}", skipping command registration')
            continue

        output = FISH_FUNCTIONS_PATH / f"{cmd}F.fish"
        conts = get_command_template_for(cmd=cmd, find_cmd=find_cmd)
        if output.is_dir():
            raise IsADirectoryError("{output} is a directory ?!")
        elif output.is_file():
            mode = "OVERWRITE"
        else:
            mode = "CREATE"

        with output.open("w") as f:
            print(f"[{mode}]\t{cmd}\t-> {output}")
            f.write(conts)


if __name__ == "__main__":
    main()
