from os import path
from markdown import markdown
from bs4 import BeautifulSoup

from parse_note_file_result import ParseNoteFileResult
from utils import is_absolute_url

question_tag = 'h1'

class NoteFile:
  def __init__(self, path):
    self.path = path

  def is_note_file_path(file_path) -> bool:
    return path.isfile(file_path) and file_path.endswith('.md')

  def parse(self) -> ParseNoteFileResult:
    html = self.open_as_html()
    result = ParseNoteFileResult()

    self.parse_media_from_html(html, result)
    self.parse_notes_from_html(html, result)

    return result

  def open_as_html(self):
    with open(self.path, 'r') as file:
      content = markdown(file.read(), extensions=['fenced_code'])

    return BeautifulSoup(content, 'html.parser')

  def parse_notes_from_html(self, html: BeautifulSoup, result: ParseNoteFileResult):
    question = None
    answer = ''

    for node in html.contents:
      if node.name == question_tag:
        #  If there is a current question, add it to the result
        if question:
          result.add_note(question, answer.strip())

        question = node.text
      else:
        if not question:
          raise Exception('No question found for note. Check the file: ' + self.path)

        answer += str(node)

    # Add the last question to the result
    if question:
      result.add_note(question, answer.strip())

  def parse_media_from_html(self, html: BeautifulSoup, result: ParseNoteFileResult):
    for img in html.find_all('img'):
      if not is_absolute_url(img['src']):
        image_full_path = path.join(path.dirname(self.path), img['src'])
        image_file_name = path.basename(image_full_path)

        img['src'] = image_file_name

        result.add_media(image_full_path, image_file_name)
