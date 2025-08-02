# language-map-lexer-parser
A lexer and parser for handing txt files that map words from one language to another. Aims to let the user write as casually as possible while following a basic syntax to make one-to-one, one-to-many and many-to-many connections with support for comments associated with each line.

Welcome to this lexer and parser for interpretting inter-language notes.
This program aims to address the issue of freely written notes being
interpretable by other systems.
Thus, the lexer and parser present here can parse notes with very
little syntax contrains so that you can make notes freely.

## Idea:
input file with notes, output file with parsed notes as JSON

## Syntax:

`~` for comments. Comments will be stored and used for context during quizzes.

`#` for Hard comments. These will be completely ignored.

`,` or `/` to delimit synonyms/words that mean the same or a different meaning of the word

`==` to assert equivalence

1) `spaces` between words will be stored as is

2) `spaces` between words and special chars will be ommited.

## Usage:
python `<python_file> <file_read> [<file_write>] lang1 lang2`
trailing words will be omitted
*Note:* if `<file_write>` isn't given, file_read with a .json 
extention will be used to write onto.
Also, the comments file is simply `file_read` (without extentions) `+ "_comm.json"`
