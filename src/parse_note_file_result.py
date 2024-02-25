class ParseNoteFileResult:
  def __init__(self):
    self.media = []
    self.notes = []

  def add_media(self, path: str, alias: str) -> None:
    if not path or not alias:
        raise ValueError("Path and alias must be provided.")

    self.media.append({ 'path': path, 'alias': alias, })

  def add_note(self, question: str, answer: str) -> None:
    if not question or not answer:
        raise ValueError("Question and answer must be provided.")

    self.notes.append({ 'question': question, 'answer': answer })
