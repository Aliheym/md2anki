from os import path
from markdown import Markdown

from note_file import NoteFile

class NoteDir:
  def is_metadata_file_path(file_path) -> bool:
    return path.isfile(file_path) and path.basename(file_path) == 'metadata.md'

  def __init__(self, path, name = None):
    self.path = path
    self.name = name
    self.parent_dir = None
    self.dirs = []
    self.files = []

  def get_dirs(self):
    return self.dirs

  def get_files(self) -> list[NoteFile]:
    return self.files

  def is_empty(self) -> bool:
    return len(self.files) == 0

  def get_full_deck_name(self) -> str:
    prefix = self.parent_dir.get_full_deck_name() if self.parent_dir else ''
    base = self.name or path.basename(self.path)

    if not prefix:
      return base

    return prefix + '::' + base

  def add_dir(self, dir):
    dir.parent_dir = self

    self.dirs.append(dir)

  def add_file(self, file_path):
    if NoteDir.is_metadata_file_path(file_path):
      self.parse_metadata_from_file(file_path)
    else:
      self.files.append(NoteFile(file_path))

  def parse_metadata_from_file(self, file_path):
    with open(file_path, 'r') as file:
      content = file.read()

    md = Markdown(extensions=['meta'])
    md.convert(content)

    metadata = md.Meta

    if 'name' in metadata and len(metadata['name']) > 0:
      self.name = metadata['name'][0]
