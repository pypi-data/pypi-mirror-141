import os
from typing import NamedTuple, List, Union
import shutil
from tqdm import tqdm
import logging

from photoarchiver.helpers.path import get_destination_path, get_deduplicated_destination_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileOperation(NamedTuple):
    """A FileOperation is a simple container class describing the operations ran by the PhotoArchiver.
    These operations have a `source_path` and a `destination_path`.
    """
    source_path: str
    destination_path: str


class PhotoArchiver:
    """Provides the logic to execute a set of file operations to archive a set of files from a list or single
    `source_directory` into a `destination_directory`. Set `copy_files` to True if you are looking to copy the files,
    false to move them.
    """

    def __init__(self,
                 source_directories: Union[str, List[str]],
                 destination_directory: str,
                 copy_files: bool = True):
        self.source_directories = source_directories if isinstance(source_directories, list) else [source_directories]
        self.destination_directory = destination_directory
        self.copy_files = copy_files

    def run(self):
        logger.info("Running PhotoArchiver")
        file_operations = self._get_file_operations()
        self._execute_file_operations(file_operations)

    def _get_file_operations(self):
        logger.info("Getting FileOperation objects")
        return [
            FileOperation(
                source_path=file_path,
                destination_path=os.path.join(self.destination_directory, get_destination_path(file_path))
            )
            for file_path in tqdm(self._get_file_paths())
        ]

    def _execute_file_operations(self, file_operations: List[FileOperation]):
        logger.info("Executing file operations (move/copy)")
        for source_path, destination_path in tqdm(file_operations):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            destination_path = get_deduplicated_destination_path(destination_path)

            if self.copy_files:
                shutil.copy2(source_path, destination_path)
            else:
                shutil.move(source_path, destination_path)

    def _get_file_paths(self):
        return [os.path.join(dp, f)
                for source_directory in self.source_directories
                for dp, dn, filenames in os.walk(source_directory)
                for f in filenames]
