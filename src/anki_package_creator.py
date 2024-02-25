from hashlib import md5
from genanki import Model, Deck, Note, Package

from note_dir import NoteDir

class AnkiPackageCreator:
  def create_anki_deck_id(deck_dir_path: str):
    hash = md5(deck_dir_path.encode('utf-8')).hexdigest()

    # We use just 8 bytes to keep the deck id within the 32-bit signed integer range
    return int(hash[:8], 16)

  def __init__(self, model_id: int = None, model_name: str = None):
    self.model_id = model_id or 1708878225
    self.model_name = model_name or 'a2md'

    self.model = self.create_anki_model()

  def from_note_dir(self, note_dir: NoteDir) -> Package | None:
    if note_dir.is_empty():
      return None

    deck = self.create_deck(note_dir)
    media_files = []

    for file in note_dir.get_files():
      result = file.parse()

      for note in result.notes:
        deck.add_note(
          Note(
            model=self.model,
            fields=[note.get('question'), note.get('answer')]
          )
        )

      for media in result.media:
        media_files.append(media.get('path'))

    return Package(deck, media_files=media_files)

  def create_deck(self, note_dir: NoteDir):
    return Deck(
      AnkiPackageCreator.create_anki_deck_id(note_dir.path),
      note_dir.get_full_deck_name()
    )

  def create_anki_model(self):
    return Model(
      self.model_id,
      self.model_name,
      fields=[
        { 'name': 'Question' },
        { 'name': 'Answer' },
      ],
     templates=[
      {
        'name': self.model_name,
        'qfmt': '<h1>{{Question}}</h1>',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])
