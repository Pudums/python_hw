import subprocess


def max_line_size(current, index, array):
    if index == len(array):
        return current
    return max(len(array[index]), max_line_size(current, index + 1, array))


def printline(line, index, left):
    if index < len(line):
        if left == 1:
            return line[index] + "\\\\ \n"
        return line[index] + "&" + printline(line, index + 1, left - 1)
    if left == 1:
        return "\\\\ \n"
    return "&" + printline(line, index + 1, left - 1)


def write_begin():
    return "\\documentclass[a4paper, 12pt]{article}\n \\begin{document}\n"


def write_lines(array, line_size, index):
    if index == len(array):
        return ""
    return printline(array[index], 0, line_size) + write_lines(array, line_size, index + 1)


def write_table_latex(array):
    line_size = max_line_size(1, 0, array)
    return "\\begin{center}\n" + "\\begin{tabular}{" + "c " * line_size + "}\n" + write_lines(array, line_size,
                                                                                              0) + "\\end{tabular}\n" + "\\end{center}\n"


def write_end():
    return "\\end{document}"


def write_full(array):
    with open("artifacts/table.tex", "w") as fout:
        fout.write(write_begin() + write_table_latex(array) + write_end())


write_full([["1", "2", "3"], ["2", "3"], ["3"]])
