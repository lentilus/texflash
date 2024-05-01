from typing import List
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexNode
from parser.models import FlashCard
import sys
import json

def recurse_env(nodes: List[LatexNode], name: str)-> List[LatexEnvironmentNode]:
    found= []
    for node in nodes:
        if isinstance(node, LatexEnvironmentNode):
            if node.environmentname == name:
                found.append(node)
                continue

        # not very beautiful, but gets the job done
        try:
            found += recurse_env(node.nodelist, name)
        except:
            pass
    return found

def parse_flashcards(src: str, env: str = "flashcard", question_env: str = "question", fallback_question="no question...")-> List[FlashCard]:
    nodes, _, _ = LatexWalker(src).get_latex_nodes()

    # retain preamble but remove rest of document
    doc = recurse_env(nodes, "document")[0]
    dstart = doc.pos
    dstop = doc.len + dstart

    filtered = recurse_env(nodes, env)

    flashcards: List[FlashCard] = []

    for card in filtered:
        cstart = card.pos
        cstop = card.len + cstart
        card_code = src[cstart:cstop]

        embedded_card = src[0:dstart] + "\n\\begin{document}\n" + card_code + "\n\\end{document}\n" + src[dstop:]

        question = recurse_env(card.nodelist, question_env)
        if len(question) == 0:
            question_code=fallback_question
        else:
            qstart = question[0].pos
            qstop =  question[0].len + qstart
            question_code = src[qstart:qstop]

        embedded_question = src[0:dstart] + "\n\\begin{document}\n" + question_code + "\n\\end{document}\n" + src[dstop:]

        flashcard = FlashCard(question=embedded_question, source=embedded_card)
        flashcards.append(flashcard)
    return flashcards

def main():
    source = sys.argv[1]
    fallback = sys.argv[2]
    cards = parse_flashcards(source, fallback_question=fallback)
    card_json = []
    for card in cards:
        card_json.append(card.model_dump(mode='json'))

    json.dump(card_json, sys.stdout)

if __name__ == '__main__':
    main()
