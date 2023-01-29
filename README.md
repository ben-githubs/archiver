# Archiver
This simple module allows you to create a zip archive, combining multiple directories and allowing you to specify a filter file with gitginore rule syntax.

## How to Install
I haven't bothered to add to pypi so just copy `archiver.py` and place it somewhere in your Python path.

## How to Use
It's pretty simple. Import the archive class into your file:

```
from archiver import Archive
```

Next, create the archive object wih the desired archive path. You can optionally specify a filter file to ignore particular paths.
```
a = Archiver("my_archive.zip")
```
or
```
a = Archiver("my_archive.zip", ".ignore")
```
If you specify a filter file, the path must be relative to where the command is executed from. The rules for filtering are the same as when using a `.gitignore` file.

Finally, to archive a directory, simply use the archive function. Specify a target, and one or more source directories.
```
a.write("dir_1", "dir_2/dir_3")
```

Archiver will write all files to the archive root as they are relative to their original source folder. For example:
```
dir_1/foo               ->  /dir_1/foo
dir_1/subdir/foo        ->  /dir_1/subdir/foo
dir_2/dir_3/bar         ->  /dir_3/bar
dir_2/dir_3/subdir/foo  ->  /dir_3/subdir/foo
```

Be cautious of name collisions. In the case of multiple files mapping to the same archive path, the one specified later will overwrite the previous one. For example, in the following command, `a.archive('target.zip', 'a/foo', 'b/c/foo')`, a file `a/foo/bar` would be ignored in favour of `b/c/foo/bar`, if it exists.

### Deleting Archive Contents
You can clear the contents of an archive by using `clear`:
```
a = Archive("my_archive.zip")
a.clear()
```

### Add to Archive without Clearing Contents First
If you want to add individual items to an archive without removing the pre-existing contents, use `add`:
```
a = Archive("my_archive.zip")
a.add("path_to_item")
```
As with `write`, you can specify multiple items to add in a single call:
```
a.add("foo/item1", "bar/item2", ... )
```

### Changing the Name
You can specify a different name for an item when it's saved to the archive.

For a single file, the entry is added as the new name. To save `./foo` as `./bar`, use:
```
a.add("foo", name="bar")
```

This works for saving single files in a subfolder as well:
```
a.add("foo", name="subdir/bar")
```

When using the `name` option for archiving directories, the name of the directory is changed, but the files within retain their original names, relative to the source folder. For example:
```
a.add("my_dir", name="new/dir/name")
```
will result in
```
my_dir          ->  /new/dir/name
my_dir/foo      ->  /new/dir/name/foo
my_dir/bar/baz  ->  /new/dir/name/bar/baz
```

### Filtering
You may specify an ignore filter when creating the archive object by providing the path to the filter configuration file:
```
a = archive("my_archive.zip", ".ignore")
```

The path is evaluated relative to the working directory.

Additionally, you can optionally utilize the `filter` option in the `write` and `add` commands, to use a different set of filtering rules which apply only to the items being uploaded in that command:
```
a = archive("my_archive.zip", ".ignore")     # specify '.ignore' as the default filter
a.add("my_items/")                           # no filter specified, so defaults to '.ignore'
a.add("my_other_items/", filter=".ignore2")  # uses rules in '.ignore2' instead of '.ignore'
```
Note that when using the `filter` option, the rules within the default filter are ignored, and only rules defined within the new filter will be adhered to. So, if your original `.ignore` says "ignore all `.env` files", but `.ignore2` doesn't define any filters on `.env`, then it's possible to archive `.env` files when using `filter=".ignore2"`.