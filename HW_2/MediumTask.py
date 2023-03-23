import HW_1.main as astBuilder
from pdflatex import PDFLaTeX
import EasyTask
import subprocess


def write(array):
    astBuilder.build_graph("fib.py")
    with open("artifacts/image.tex", "w") as fout:
        fout.write("\\documentclass[a4paper, 12pt]{article}\n")
        fout.write("\\usepackage{graphicx}\n")
        fout.write("\\begin{document}\n")
        fout.write(EasyTask.write_table_latex(array))
        fout.write("\\begin{center}")
        fout.write("\\includegraphics[scale=0.25]{artifacts/result}")
        fout.write("\\end{center}")
        fout.write("\\end{document}")
    with open("artifacts/image.pdf", "wb") as out_pdf:
        out_pdf.write(
            PDFLaTeX.from_texfile('artifacts/image.tex').create_pdf()[0])
    subprocess.call(executable="rm", args=(" ", "artifacts/image.tex"))
    subprocess.call(executable="rm", args=(" ", "artifacts/result.pdf"))


write([["1", "2", "3"], ["2", "3"], ["3"]])
