# Argument Parser
A command line argument parser based on the [Args kata](https://codingdojo.org/kata/Args/) [implementation](https://github.com/unclebob/javaargs/tree/master) by</br> 
[Robert C. Martin](https://en.wikipedia.org/wiki/Robert_C._Martin), translated into Python and extended to cover missing </br> 
and required arguments, as well as present help messages.
## Example Usage
```python3
import sys

from adapters.printer_presenter import PrinterPresenter
from adapters.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from entities.argument_error import ArgumentError
from entities.argument_schema import ArgumentSchemaElement
from use_cases.parse_arguments import ParseArgumentsUseCase
from use_cases.present_help_message import PresentHelpMessageUseCase


try:
    parser = ParseArgumentsUseCase(
        [ArgumentSchemaElement(name='a', argument_type='*', 
            description='A str argument', is_required=False, long_name='argument')], 
        sys.argv[1:], StringsArgumentMarshalerFactory(), 
        PresentHelpMessageUseCase('your_program.py', 'Your program description', PrinterPresenter()))
    
    if parser.has('argument'):
        argument_value = parser.get_value_of(('a', 'argument'))
except ArgumentError as e:
    sys.stderr.write(e.error_message())
# See argument_parser/parse.py for a more detailed example
```
## Tests
Perform the following to run all corresponding tests:
```bash
cd argument_parser
python3 -m unittest tests/*.py
```
## Module Integration
For now, to integrate the module you will need to update the ```import``` </br>
statements of most files to include the path of where you store the </br>
package. For example, if you place the ```argument_parser``` package at</br>
the root of your project, you'll need to adjust the ```import``` </br>
statements like this:
```python
from argument_parser.ports.argument_marshaler import ArgumentMarshaler
```
instead of:
```python
from ports.argument_marshaler import ArgumentMarshaler
```
## Acknowledgments
* [Robert C. Martin](https://en.wikipedia.org/wiki/Robert_C._Martin)
* [Robert Frost's "The Road Not Taken"](https://www.poetryfoundation.org/poems/44272/the-road-not-taken)
* [Mary Shelley's "Frankenstein"](https://en.wikipedia.org/wiki/Frankenstein)
## License
You may use this program and source code for any purpose at all at your own risk. It is not copyrighted. Have fun!