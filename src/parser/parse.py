from logging import raiseExceptions
from typing import List
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexNode
from parser.models import FlashCard
import sys
import json

# not very beautiful, but gets the job done
def recurse_env(nodes: List[LatexNode], name: str)-> List[LatexEnvironmentNode]:
    found= []
    for node in nodes:
        if isinstance(node, LatexEnvironmentNode):
            if node.environmentname == name:
                found.append(node)
                continue
        try:
            found += recurse_env(node.nodelist, name)
        except:
            pass
    return found

def parse_flashcards(src: str, env: str = "flashcard") -> List[FlashCard]:
    nodes, _, _ = LatexWalker(src).get_latex_nodes()

    # retain preamble but remove rest of document
    doc = recurse_env(nodes, "document")[0]

    preamble = src[:doc.pos]
    flashcards: List[FlashCard] = []
    card_nodes = recurse_env(nodes, env)
    for card in card_nodes:
        # a flashcard looks like this \begin{flashcard}[id]{question}
        # We check if an id was supplied
        try:
            id_str = card.nodelist[0].chars
            if id_str[0] != "[" or id_str[-1] != "]":
                raise Exception # found no valid id
            id = id_str[1:-1]
            front = card.nodelist[1]
        except:
            id = None
            front = card.nodelist[0]

        front_str = src[front.pos+1:front.pos+front.len-1]
        back_str = src[card.pos:card.pos+card.len]
        # print(f"front_str is {front_str}")
        if len(front_str) == 0 or front_str.isspace():
            front_src = None
        else:
            front_src = preamble + "\n\\begin{document}\n" + front_str + "\n\\end{document}"

        back_src = preamble + "\n\\begin{document}\n" + back_str + "\n\\end{document}"

        flashcard = FlashCard(id=id, front=front_src, back=back_src)
        flashcards.append(flashcard)

    return flashcards

def main():
    source = sys.argv[1]
    cards = parse_flashcards(source, env="flashcard")
    card_json = []
    for card in cards:
        card_json.append(card.model_dump(mode='json'))

    json.dump(card_json, sys.stdout)

if __name__ == '__main__':
    main()
