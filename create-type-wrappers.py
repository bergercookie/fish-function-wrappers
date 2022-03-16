#!/usr/bin/env python3

from pathlib import Path
from shutil import which


# Change if necessary
FISH_FUNCTIONS_PATH = Path().home() / ".config" / "fish" / "functions"

# Edit this list according to to your preferences.
# Executables not found in your PATH will be skipped
COMMANDS = ["cat", "chmod", "gnvim", "gvim", "ls", "vi", "vim", "grep", "rg", "rm", "lddtree",
            "ldd", "file"]


def main():
    template = """function {cmd}T -d "Run 'type -pa' and pass the resulting path(s) to {cmd}."
    # All but the last argument are passed to "{cmd}" itself.
    set argc (count $argv)
    set cmd (status current-command)
    set args
    if test $argc -eq 0
        printf "I need at least 1 argument.\\nUSAGE: $cmd [flags-of-command] <name-of-fish-command-or-executable->\n"
        return 1
    else if test $argc -eq 1
        set args (type -pa $argv)
        set executable $argv
    else
        set args $argv[1..-2] (type -pa $argv[-1])
        set executable $argv[-1]
    end

    if ! type -pa $executable
        printf  "Command/Executable $executable was not found by 'type'"
        return 1
    end

    echo Running "{cmd} $args"
    {cmd} $args
    return 0
end

# tab completion - based on type
complete -c {cmd}T -a "(complete -C (printf %s\\n (commandline -ot)))" -x
"""
    for cmd in COMMANDS:
        if not which(cmd):
            print(f'Cannot find executable "{cmd}", skipping command registration')
            continue

        output = FISH_FUNCTIONS_PATH / f"{cmd}T.fish"
        conts = template.format(cmd=cmd)
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
