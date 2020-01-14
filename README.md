# Recursive compare and delete

Recursively compare a *old* directory with a *new* directory. Delete *old*
files which are unchanged.

Useful for pruning down old backups after making new backups.

Any *old* file will only be deleted if:

  - The script is given the `-d` flag.
  - There is a *new* file with the exact same path and name.
  - The old and new file are the exact name size and content.

## Use

```
./recursive-compare-del.py -d old_dir new_dir
```

### Windows

Assuming `python` is Python 3 in `%PATH%`.

```
python recursive-compare-del.py -d old_dir new_dir
```

**Watch out**: PowerShell tab-completes directory names containing spaces with
a trailing backslash before the closing quote, which Python interprets as an
escaped quote. Remove the final slash to run the script.

## Requirements

Tested on Python 3.7.3 on Windows 10 in PowerShell.

  - [Python 3](https://www.python.org/)
