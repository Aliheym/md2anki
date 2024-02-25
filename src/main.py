import argparse

from program import Program

def create_args_parser():
  parser = argparse.ArgumentParser(
    prog='md2anki',
    description='Convert markdown notes to Anki decks',
  )

  parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')

  parser.add_argument('-p', '--path', required=True, help='Path to the directory containing the notes')
  parser.add_argument('-o', '--output', help='Path to the directory where the Anki packages will be saved')
  parser.add_argument('-i', '--auto-import', action=argparse.BooleanOptionalAction, default=False, help='Automatically import the Anki packages into Anki. Requires AnkiConnect to be installed.')

  return parser

if __name__ == '__main__':
  args_parser = create_args_parser()
  args = args_parser.parse_args()

  program = Program(
    root_dir=args.path,
    auto_import=args.auto_import,
    output_dir=args.output
  )

  program.run()
