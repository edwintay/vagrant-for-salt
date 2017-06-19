# Symlink mapping
Host files are symlinked into `srv/` and exposed read/write to the guest via
NFS.

## Format
Nested dictionary with keys representing link names if their corresponding
value is a string, and representing directory names if their corresponding
value is a dict.

The link/directory names are relative to their parent, with the root
implicitly set to `srv/`.

## Path variables
Shell variables such as `~` and `$WORKSPACE` will be expanded using the
python library commands `os.path.expanduser()` and `os.path.expandvars()`

## Example
The following config file
```
{
  "salt": "$WORKSPACE/techops/engops-salt",
  "secret": "$WORKSPACE/techops/engops-secret",
  "formulas": {
    "ssh-formula": "$WORKSPACE/techops/salt-formulas/ssh-formula",
    "salt-formula": "$WORKSPACE/techops/salt-formulas/salt-formula"
  }
}
```
will result in the following directory structure
```
srv
├── formulas
│   ├── salt-formula -> /path/to/workspace/techops/salt-formulas/salt-formula
│   └── ssh-formula -> /path/to/workspace/techops/salt-formulas/ssh-formula
├── salt -> /path/to/workspace/techops/engops-salt
└── secret -> /path/to/workspace/techops/engops-secret
```
