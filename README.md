# Function Wrappers for Fish

Python scripts for generating useful wrapper functions for commonly executed
UNIX executables for the [Fish shell](https://fishshell.com/).

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

## TODO `find` / `fd-find` Wrappres

## TODO `grep -l` / `ripgrep` Wrappers

## How can I add/remove executables for which to create wrappers

Just edit the COMMANDS variable of the python script(s) and rerun.
