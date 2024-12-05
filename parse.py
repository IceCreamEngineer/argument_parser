import sys

from adapters.printer_presenter import PrinterPresenter
from adapters.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from entities.argument_error import ArgumentError
from entities.argument_schema import ArgumentSchemaElement
from use_cases.parse_arguments import ParseArgumentsUseCase
from use_cases.present_help_message import PresentHelpMessageUseCase


def main():
    help_message_presenter, presenter = setup_presenters()
    schema = [ArgumentSchemaElement('s', '*', 'A string argument', is_required=True, long_name='string'),
              ArgumentSchemaElement('a', '[*]', "A string array argument", False, 'string-array')]
    try_to_parse_arguments_for(schema, help_message_presenter, presenter)


def setup_presenters():
    presenter = PrinterPresenter()
    help_message_presenter = (
        PresentHelpMessageUseCase(program_filename="parse.py", description="A CLI argument parser.", presenter=presenter))
    return help_message_presenter, presenter


def try_to_parse_arguments_for(schema, help_message_presenter, presenter):
    try:
        parse_arguments_for(schema, help_message_presenter, presenter)
    except ArgumentError as e:
        handle_argument_error(e, schema, help_message_presenter)


def parse_arguments_for(schema, help_message_presenter, presenter):
    parser = ParseArgumentsUseCase(schema, sys.argv[1:], StringsArgumentMarshalerFactory(), help_message_presenter)
    presenter.present(parser.get_value_of(('s', 'string')))
    if parser.has('a'):
        presenter.present(parser.get_value_of(('a', 'string-array')))


def handle_argument_error(e, schema, help_message_presenter):
    help_message_presenter.present_help_message(schema)
    sys.stderr.write(e.error_message())


if __name__ == '__main__':
    main()
