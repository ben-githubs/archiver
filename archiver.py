""" Archiver is a simple tool that allows recursively adding multiple directories to a zip archive. 
"""

from typing import Callable
import io
from os import PathLike
from pathlib import Path
from zipfile import ZipFile

from gitignore_parser import parse_gitignore

class Archiver:
    def __init__(self, filter_file: str | PathLike = None):
        if not filter_file is None:
            self.load_filter(filter_file)
        else:
            self.ignore = lambda *args, **kwargs: False
    
    """ Given a path to a .gitignore-syntax file, validates the path, then loads the contents into
    an internal filtering object.
    """
    def load_filter(self, filter_file: str | PathLike = None) -> None:
        if isinstance(filter_file, str):
            filter_file = Path(filter_file)
        if not isinstance(filter_file, PathLike):
            raise TypeError(' '.join(["'filter_file' must be a string or os.PathLike,",
                f"not '{filter_file.__class__.name}'."]))
        if not filter_file.exists():
            raise FileNotFoundError(f"No file exists with name '{filter_file}'.")
        if not filter_file.is_file():
            raise IsADirectoryError(f"Path '{filter_file} points to a directory, not a file.")
        
        self.ignore = parse_gitignore(str(filter_file))
    
    def archive(self, target: str | PathLike, *paths: str | PathLike):
        # Convert from str to Path, if needed.
        if isinstance(target, str):
            target = Path(target)
        paths = list(paths) # Cannot do item assignment with a tuple
        for x in range(len(paths)):
            if isinstance(paths[x], str):
                paths[x] = Path(paths[x])
        
        # Create a collection of paths to add to archive
        # We use a dict to allow us to have the archive-root path as the key, and the absolute path as 
        # the value.
        files = dict()

        # Scan the paths provided
        for path in paths:
            if path.is_dir():
                for p in path.rglob('*'):
                    if not self.ignore(str(p)):
                        key = path.name / p.relative_to(path)
                        files[key] = p
            else:
                files[path.name] = path

        # Create archive an add all files specified
        with ZipFile(target, mode='w') as archive:
            for rel_path, abs_path in files.items():
                print(rel_path)
                archive.write(abs_path, arcname=rel_path)

class Archive:
    def __init__(self, fname: str | PathLike, filter: str | PathLike = None):
        self.fname = fname
        if filter is None:
            self.ignore = lambda *args, **kwargs: False
        else:
            self.ignore = Archive.load_filter(filter)


    """ Given a path to a .gitignore-syntax file, validates the path, then loads the contents into
    an internal filtering object.
    """
    def load_filter(filter_file: str | PathLike = None) -> None:
        if isinstance(filter_file, str):
            filter_file = Path(filter_file)
        if not isinstance(filter_file, PathLike):
            raise TypeError(' '.join(["'filter_file' must be a string or os.PathLike,",
                f"not '{filter_file.__class__().name}'."]))
        if not filter_file.exists():
            raise FileNotFoundError(f"No file exists with name '{filter_file}'.")
        if not filter_file.is_file():
            raise IsADirectoryError(f"Path '{filter_file} points to a directory, not a file.")
        
        return parse_gitignore(filter_file)
    
    def clear(self):
        with ZipFile(self.fname, mode='w') as f:
            pass
    
    def write(self, *paths, name: str = None, filter: str | PathLike = None):
        self.clear()
        self.add(*paths, name=name, filter=filter)
        
    def add(self, *paths, name: str = None, filter: str | PathLike = None):
        # Lead filter if passed as arg, else fallback on default one
        ignore = Archive.load_filter(filter) if filter else self.ignore

        items = dict()

        for path in paths:
            if isinstance(path, str):
                path = Path(path)
            if path.is_dir():
                items.update(Archive.__add_dir(path, ignore, name))
            else:
                items.update(Archive.__add_file(path, ignore, name))
                

        with ZipFile(self.fname, mode='a') as f:
            for arcname, path in items.items():
                f.write(path, arcname=arcname)

    def __add_dir(path: Path, ignore: Callable, name: str = None):
        if name is None:
            name = path.parts[0]
        
        # Recursively map items to their archive locations
        items = dict()
        for item in path.rglob('*'):
            if ignore(str(item)):
                continue # Should be skipped
            # Rename root folder
            key = name / item.relative_to(path)
            items[key] = item
        return items

    def __add_file(path: Path, ignore: Callable, name: str = None):
        if name is None:
            name = path.name
        
        items = dict()
        if not ignore(str(path)):
            items[name] = path
        return items


if __name__ == "__main__":
    # Testing!
    a = Archive('archive.zip', filter='.s3ignore')
    a.write('venv_lambda/lib/python3.9/site-packages', name='Python')
    a.add('Shared', name='Python')

    with ZipFile('archive.zip') as f:
        f.printdir()