import tempfile
import shutil
import os
import subprocess

from parser import parse
from importer import anki_import

def compile_svg(main_file):
    latexmk=["latexmk",
             "-pdf",
             "-f" ,"-norc",
             "-lualatex",
             "-interaction=batchmode",
             "-outdir=build",
             "-cd", main_file]

    subprocess.call(latexmk)

    dir=os.path.dirname(main_file)
    name=os.path.basename(main_file)
    name=main_file.split("/")[-1].rpartition('.')[-3]
    print(name)

    pdf=os.path.join(dir, f"build/{name}.pdf")
    svg=os.path.join(dir, f"build/{name}.svg")

    print(f"svg after joining {svg}")
    subprocess.call(["pdf2svg", pdf, svg])
    return svg

def main(tex_main="./testibunti/main.tex"):

    # tex_main=os.path.join(root, main)
    root = os.path.dirname(tex_main)
    with open(tex_main, "r") as f:
        source=f.read()
        cards=parse.parse_flashcards(source, env='flashcard', question_env='question')
        print(cards)
            
    for card in cards:
        with tempfile.TemporaryDirectory() as tmp:
            # copy tex files
            shutil.copytree(root, tmp, dirs_exist_ok=True)

            front_file=os.path.join(tmp,"front.tex")
            back_file=os.path.join(tmp,"back.tex")

            with open(back_file, "w") as f:
                f.write(card.source)

            if card.question == "":
                continue

            svg = compile_svg(back_file)
            print(f"svg file is{svg}")

            print("importing...")
            print(os.listdir(os.path.join(tmp, "build")))
            anki_import.import_card("", svg)
            
if __name__ == "__main__":
    main("./testibunti/main.tex")
