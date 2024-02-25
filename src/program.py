from genanki import Package
from os import path, listdir, makedirs

from anki_client import AnkiClient

from note_dir import NoteDir
from note_file import NoteFile

from anki_package_creator import AnkiPackageCreator

class Program:
  def __init__(self, root_dir: str, auto_import: bool = False, output_dir: str = None) -> None:
    # `root_dir` is the root directory containing the notes
    self.root_dir = path.abspath(root_dir)
    # `auto_import` is a flag indicating whether the Anki packages should be automatically imported into Anki
    self.auto_import = auto_import
    # `output_dir` is the directory where the Anki packages will be saved
    self.output_dir = path.abspath(output_dir) if output_dir else None

    if not path.isdir(self.root_dir):
      raise ValueError(f'Expected a directory, but got: {self.root_dir}')

    if not self.output_dir and not self.auto_import:
      raise ValueError('Either `output_dir` or `auto_import` must be set')

    self.anki_client = AnkiClient()
    self.package_creator = AnkiPackageCreator()

  def run(self):
    print(f'🚀 Starting exporting notes from the #{self.root_dir} directory...')

    # Scan the root directory for notes and all subdirectories
    root_note_dir = self.scan_note_dir(name="a2md", dir_path=self.root_dir)

    # Convert the notes to Anki packages
    packages = self.convert_note_dirs_to_packages(root_note_dir)

    # Export the Anki packages
    for package in packages:
      self.import_package(package)

    print('🎉 Finished exporting notes')

  def scan_note_dir(self, dir_path: str, name: str = None) -> NoteDir:
    note_dir = NoteDir(name=name, path=dir_path)

    for file_name in listdir(dir_path):
      file_path = path.join(dir_path, file_name)

      if path.isdir(file_path):
        note_dir.add_dir(self.scan_note_dir(dir_path=file_path))

      if NoteFile.is_note_file_path(file_path):
        note_dir.add_file(file_path)

    return note_dir

  def convert_note_dirs_to_packages(self, note_dir: NoteDir) -> list[Package]:
    packages: list[Package] = []

    package = self.package_creator.from_note_dir(note_dir)

    if package:
      packages.append(package)

    for dir in note_dir.get_dirs():
      packages += self.convert_note_dirs_to_packages(dir)

    return packages

  def import_package(self, package: Package) -> None:
    deck_name = package.decks[0].name
    output_dir = self.output_dir or '/tmp/md2anki/output'

    if not path.exists(output_dir):
      makedirs(output_dir)

    if not path.isdir(output_dir):
      raise ValueError(f'Expected a directory, but got: {output_dir}')

    package_path = path.abspath(path.join(output_dir, f'{deck_name}.apkg'))
    package.write_to_file(package_path)

    if self.output_dir:
      print(f'📦 Anki package created: {package_path}')

    if self.auto_import:
      self.anki_client.import_package(package_path)
      print(f'🚚 Anki package imported: {deck_name}')
