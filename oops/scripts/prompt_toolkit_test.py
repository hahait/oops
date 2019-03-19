#/usr/bin/env python

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory,InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.lexers import HtmlLexer
from prompt_toolkit.layout.lexers import PygmentsLexer

SQLCompleter = WordCompleter([ 'select ', 'insert', 'update', 'delete', 'drop' ], ignore_case=True)

while True:
    user_input = prompt(message='>>>',
                        history=FileHistory("/tmp/myhaha.txt"),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter,
                        lexer=PygmentsLexer(HtmlLexer)
                        )
    print(user_input)