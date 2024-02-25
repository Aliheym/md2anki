import json
import urllib.request

class AnkiClient:
  def request(action, **params):
    return {
      'action': action,
      'params': params,
      'version': 6
    }

  def __init__(self, anki_url: str = None):
    self.anki_url = anki_url or 'http://localhost:8765'

  def import_package(self, path: str):
    return self.invoke('importPackage', path=path)

  def invoke(self, action, **params):
    request_json = json.dumps(AnkiClient.request(action, **params)).encode('utf-8')

    response = json.load(urllib.request.urlopen(urllib.request.Request(self.anki_url, request_json)))

    if len(response) != 2:
      raise Exception('response has an unexpected number of fields')

    if 'error' not in response:
      raise Exception('response is missing required error field')

    if 'result' not in response:
      raise Exception('response is missing required result field')

    if response['error'] is not None:
      raise Exception(response['error'])

    return response['result']
