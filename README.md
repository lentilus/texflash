# TexFlash

## Idea
Manually creating flashcards can be tedious, therefor you might want create flashcards based of of the content of a document that you have already written. With flashtex you encapsulate content that you want to put on a flashcard with a 'flashcard' environment. The parser will generate source code that can be compiled standalone for each flashcards front and back. The beautiful thing is, that you can put anything on the flashcards that you are able to compile. It is therfor 100% intentional, that the parser is seperated from all that. It is important that your flashcard does not depend on anything outside the preamble and the flashcard itself though, as those things simply do not make it into the source code for the flashcard.

My implementation uses latexwalkter from pylatexenc.

## Installation
This project is not (yet?) on pipy, so just install from the url. I recommend installing via pipx, but of course you can theoretically use pip as well, though I do not recommend so.
```bash
pipx install git+https://gitlab.com/lentilus/texflash.git
```

## Usage
Encapsulate the code for your flashcard with a 'flashcard' environment like so

```latex
% foo.tex
\documentclass{article}
\input{preamble.tex}
\begin{document}

\begin{flashcard}
    \begin{question} What is $1+1$ equal to? \end{question}
    \[ 1+1=2. \]
\end{flashcard}

Here is some other stuff that I am not interested in seeing on a flashcard.

\begin{flashcard}
    But this is relevant too.
\end{flashcard}

\end{document}
```

As you can see, you can supply a question as well. Question means "front" of the flashcard. You must call the parse-command with fallback question, which is used for flashcards where no question is supplied. This is handy for autmated workflows, where the filename or something else might become the question.

calling
```bash
 flashtexparse "$(cat foo.tex )" "my fallback question" | jq
```
yields
```json
[
  {
    "question": "\\documentclass{article}\n\\input{preamble.tex}\n\n\\begin{document}\n\\begin{question} What is $1+1$ equal to? \\end{question}\n\\end{document}\n",
    "source": "\\documentclass{article}\n\\input{preamble.tex}\n\n\\begin{document}\n\\begin{flashcard}\n    \\begin{question} What is $1+1$ equal to? \\end{question}\n    \\[ 1+1=2. \\]\n\\end{flashcard}\n\\end{document}\n"
  },
  {
    "question": "\\documentclass{article}\n\\input{preamble.tex}\n\n\\begin{document}\nmy fallback question\n\\end{document}\n",
    "source": "\\documentclass{article}\n\\input{preamble.tex}\n\n\\begin{document}\n\\begin{flashcard}\n    But this is relevant too.\n\\end{flashcard}\n\\end{document}\n"
  }
]
```

The json returned contains an array of flashcards, each with a question and source field. The values correspond to the source-code necessary for compiling the front (question) and back (source). You can use jq or any other json parser to process the json. You can do something like this to create source files for your flashcards:


```bash
flashtexparse "$(cat foo.tex )" "my fallback question" | jq -r ".[0] .question" > card_01_front.tex
flashtexparse "$(cat foo.tex )" "my fallback question" | jq -r ".[0] .source" > card_01_back.tex
```

```latex
% card_01_front.tex
\documentclass{article}
\input{preamble.tex}

\begin{document}
\begin{question} What is $1+1$ equal to? \end{question}
\end{document}
```

```latex
% card_01_back.tex
\documentclass{article}
\input{preamble.tex}

\begin{document}
\begin{flashcard}
    \begin{question} What is $1+1$ equal to? \end{question}
    \[ 1+1=2. \]
\end{flashcard}
\end{document}
```

Have fun!

