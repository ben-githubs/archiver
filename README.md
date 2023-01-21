# Archiver
This simple module allows you to create a zip archive, combining multiple directories and allowing you to specify a filter file with gitginore rule syntax.

## How to Install
I haven't bothered to add to pypi so just copy `archiver.py` and place it somewhere in your Python path.

## How to Use
It's pretty simple. Import the archiver into your file:

```
from archiver import Archiver
```

Next, create the archiver object. You can optionally specify a filter file to ignore particular paths.
```
a = Archiver
```
or
```
a = Archiver(filter_file=".ignore")
```
If you specify a filter file, the path must be relative to where the command is executed from. The rules for filtering are the same as when using a `.gitignore` file.

Finally, to archive a directory, simply use the archive function. Specify a target, and one or more source directories.
```
a.archive('myzip.zip', 'dir_1', 'dir_2/dir_3')
```

Archiver will add all files to the archive root as they are relative to their original source folder. For example:
```
dir_1/foo              ->  /foo
dir_1/subdir/foo       ->  /subdir/foo
dir_2/dir_3/bar        ->  /bar
dir_2/dir_3/dir_4/foo  ->  /dir_4/bar
```

In the case of multiple files mapping to the same archive path, the one specified later will overwrite the previous one. For example, if both `dir_1/foo` and `dir_2/dir_3/foo` exist, then only `dir_2/dir_3/foo` will be added as `/foo` to the final zip archive.

When archiving individual files, they are saved in the root of the archive, regardless of where they were originally located relative to the current working directory. `a.archive('myzip.zip', 'foo/myfile.bar')` will result in an archive with `myfile.bar` at it's root.

There's currently no way to specify a different target path for individual files.