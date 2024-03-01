import argparse
import importlib
import io
import os
import traceback
from pathlib import Path
from threading import Event

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class CustomizedHandler(FileSystemEventHandler):
    def __init__(self, target, module, only_changes):
        self.offsets = {}
        self.target = target

        module_name, function_name = module.split('.')
        self.listen = getattr(
            importlib.import_module(module_name),
            function_name
        )

        for entry in Path(self.target).glob('**/*'):
            if entry.is_dir():
                continue
            try:
                self.read(entry, only_changes=only_changes)
            except:
                traceback.print_exc()

    def on_modified(self, event):
        if event.is_directory:
            return

        try:
            self.read(event.src_path)
        except:
            traceback.print_exc()

    def read(self, file_path, only_changes=False):
        try:
            file_path = os.path.abspath(file_path)
            offset = self.offsets.get(file_path, 0)

            fp = open(file_path, 'r')
            if only_changes:
                fp.seek(0, io.SEEK_END)
            else:
                fp.seek(offset)
            data = fp.read()
            offset = fp.tell()

            self.offsets[file_path] = offset
            data and self.listen(data)
        except:
            traceback.print_exc()

    def run(self):
        observer = Observer()
        observer.schedule(self, self.target, recursive=True)
        observer.start()
        Event().wait()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True)
    parser.add_argument('--module', required=True)
    parser.add_argument('--only-changes', action='store_true')
    args = parser.parse_args()

    try:
        CustomizedHandler(
            args.target,
            args.module,
            args.only_changes,
        ).run()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
