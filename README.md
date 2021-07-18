# Function Wrappers for Fish

![badge](https://img.shields.io/badge/fish--shell-fish--function--wrappers-blueviolet)

Python scripts for generating useful wrapper functions for commonly executed
UNIX executables for the [Fish shell](https://fishshell.com/).

## Usecases

How frequently do you have to forward the result of `which`, `find` etc. to
executables like `vim` or `chmod`?

```sh
# I want to chmod an executable:
# I can either specify the full path manually..
chmod u+x /long/path/to/my/executable

# Or I can use which to do that for me.
chmod u+x (which executable)
```

However both of the above syntaxes are copious to write. Hence here are wrapper
`fish` functions that will do that for you.

## How do they work?

The scripts of this repo will create new fish functions, by default under
`~/.config/fish/functions`, one function for each command specified in the
`COMMANDS` variable at the beginning of that script.

This is what it looks like when running these scripts:

```sh
14:38:58 ➜ ./create-find-wrappers.py
[CREATE]        cat     -> /home/berger/.config/fish/functions/catF.fish
[CREATE]        chmod   -> /home/berger/.config/fish/functions/chmodF.fish
[CREATE]        gvim    -> /home/berger/.config/fish/functions/gvimF.fish
[CREATE]        ls      -> /home/berger/.config/fish/functions/lsF.fish
[CREATE]        vi      -> /home/berger/.config/fish/functions/viF.fish
[CREATE]        vim     -> /home/berger/.config/fish/functions/vimF.fish
[CREATE]        grep    -> /home/berger/.config/fish/functions/grepF.fish
[CREATE]        rg      -> /home/berger/.config/fish/functions/rgF.fish

14:39:02 ➜ ./create-which-wrappers.py
[CREATE]        cat     -> /home/berger/.config/fish/functions/catW.fish
[CREATE]        chmod   -> /home/berger/.config/fish/functions/chmodW.fish
[CREATE]        gvim    -> /home/berger/.config/fish/functions/gvimW.fish
[CREATE]        ls      -> /home/berger/.config/fish/functions/lsW.fish
[CREATE]        vi      -> /home/berger/.config/fish/functions/viW.fish
[CREATE]        vim     -> /home/berger/.config/fish/functions/vimW.fish
[CREATE]        grep    -> /home/berger/.config/fish/functions/grepW.fish
[CREATE]        rg      -> /home/berger/.config/fish/functions/rgW.fish
```

Each of these auto-generated functions looks like the following.

<details>
  <summary>catW.fish</summary><p>

```sh
function catW -d "Run which and pass the resulting executable(s) to cat."
    # All but the last argument are passed to "cat" itself.
    set argc (count $argv)
    set cmd (status current-command)
    set args
    if test $argc -eq 0
        printf "I need at least 1 argument.\nUSAGE: $cmd [flags-of-command] <name-of-executable>
"
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

    echo Running "cat $args"
    cat $args
    return 0
end

# tab completion - based on which
complete -c catW -a "(complete -C (printf %s\n (commandline -ot)))" -x
```

</p></details>

## `which` Wrappers

Generate wrapper functions for commands so that you don't have to type out the
following:

```sh
vim (which python-executable)
```

Instead, you can now run:

```sh
vimW python-executable
```

## `fd` / `find` Wrappers

Generate wrapper functions for commands such as the following:

```sh
vim (find path/for/find -iname "*my-pat*")
```

Instead, you can now run:

```sh
vimF my-pat path/for/find
```

By default it uses the `find` executable. If you want to use [fd-find](https://github.com/sharkdp/fd) specify the `--fd` flag

## TODO `grep -l` / `ripgrep` Wrappers

## How can I add/remove to the list of executables to create wrappers for?

Just edit the COMMANDS variable of the python script(s) and rerun.
