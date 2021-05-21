#!/usr/bin/env python3

from pathlib import Path


# Change if necessary
FISH_FUNCTIONS_PATH = Path().home() / ".config" / "fish" / "functions"


def main():
    template = """function {cmd}W -d "Run {cmd}W and pass the result to which so that you open the executable directly"
    # All the arguments except the last one are passed to {cmd} itself.
    set argc (count $argv)
    set cmd (status current-command)
    set args
    if test $argc -eq 0
        printf "I need at least 1 argument.\nUSAGE: $cmd [flags-of-command] <name-of-executable>\n"
        return 1
    else if test $argc -eq 1
        set args (which $argv)
        set executable $argv
    else
        set args $argv[1..-2] (which $argv[-1])
        set executable $argv[-1]
    end

    if ! which $executable
        printf  "Executable $executable was not found by 'which'"
        return 1
    end

    echo Running "{cmd} $args"
    {cmd} $args
    return 0
end
"""
    commands = [
        "cat",
        "ls",
        "vim",
        "chmod",
    ]

    for cmd in commands:
        output = FISH_FUNCTIONS_PATH / f"{cmd}W.fish"
        conts = template.format(cmd=cmd)
        if output.is_dir():
            raise IsADirectoryError("{output} is a directory ?!")
        elif output.is_file():
            mode = "OVERWRITE"
        else:
            mode = "CREATE"

        print(f"[{mode}]\t{cmd} -> {output}")

        with open(output, "w") as f:
            f.write(conts)


if __name__ == "__main__":
    main()
