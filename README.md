# TexFlash 

> The texflash parser takes latex source code as an input and extract flashcards from it. It preserves the preamble but removes everything else inside the document that is not wraped in a flashcard environment. This results in new source code that can be used to compile the flashcards individually.

Warning! The parser is not very robust as it is just a quick and dirty solution to make my life a little easier.

## Installation

I recommend to install `texflash` via  `pipx` but of course you could use pip as well.
```bash
pipx install git+https://github.com/lentilus/texflash.git
```

## Usage
Wrap the the appropriate lines with a flashcard environment. Like so
```latex
% myfile.tex

% ...
\begin{flashcard}[nutg9tmn]{What is the definition of Baz?}
	Baz is defined as Bamboosel.
\end{flashcard}
% ...
```
Make sure to add the flashcard as a new environment in the preamble. You can decide if you want to render it in a special way.

Pass the source code as the first and only argument to the parser.
```bash
flashtexparse "$(cat myfile.tex)" | jq
```

The parser returns a json-string of the form
```json
[
  {
    "id": "nutg9tmn",
    "front": "\\documentclass{article}\n\\input{preamble}\n% more preamble\n\n\n\\begin{document}\ndefintion of Baz\n\\end{document}",
    "back": "\\documentclass{article}\n\\input{preamble}\n% more preamble\n\n\n\\begin{document}\n\\begin{flashcard}[nutg9tmn]{defintion of Baz}\n\tBaz is defined as Bamboosel.\n\\end{flashcard}\n\\end{document}"
  },
  {
    ...
  },
  ...
]
```

`jq` or any other json parser can be used to work with the output. You can do anything you like with it.

## About
The parser uses latexwalkter from pylatexenc to determine the location of environments in the source code. I found the solution of cutting out all code except for the preamble and flashcard itself to be surprisingly robust, when it comes to generating source code that compiles. The nice thing is, that everything critical is usually defined in the preamble.
