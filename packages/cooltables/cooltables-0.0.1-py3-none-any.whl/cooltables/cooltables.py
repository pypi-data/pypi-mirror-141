from typing import List, Optional

from .themes import DEFAULT_THEME


def _find_lengths(data: List[List[str]]) -> List[int]:
    lengths = [0]*len(data[0])

    for column in data:
        for i, row in enumerate(column):
            length = max(map(len, row.split('\n')))
            if length > lengths[i]:
                lengths[i] = length

    return lengths


def create_table(data: List[List[str]], *, theme: Optional[List[str]] = DEFAULT_THEME, header: Optional[bool] = True, separated: Optional[bool] = False) -> str:
    """Creates ascii table from list

    Note:
        Lenght of table is read from length of first row

    Args:
        data (List[List[str]]): Two dimensional list, with same length
        theme (Optional[List[str]]): Theme of table
        header (Optional[bool]): Whether first row is header of table, will separate and make text bold
        separated (Optional[bool]): Whether to put horizontal cell dividers

    Returns:
        str: Table
    """
    res = []

    lengths = _find_lengths(data)

    res.append("")

    # Top row
    # Ex: ╔═══╤═══╤═══╗
    res[-1] += theme[5]
    for i, length in enumerate(lengths):
        res[-1] += theme[3]*(length+2)
        res[-1] += theme[6]

    res[-1] = res[-1][:-1]+theme[7]

    # Column data
    # Ex: ║ x │ x │ x ║
    for i, column in enumerate(data):
        res.append("")
        for j, row in enumerate(column):
            if j == 0:
                res[-1] += theme[4]+" "
            else:
                res[-1] += " "+theme[0]+" "

            row = str(row).ljust(lengths[j])

            if header and i == 0:
                row = '\033[1m'+row+'\033[0m'

            res[-1] += row

            if j == len(lengths)-1:
                res[-1] += " "+theme[4]

        # Separator
        # Ex: ╟───┼───┼───╢
        if (header and i == 0) or (separated and i != len(lengths)):
            res.append("")

            res[-1] += theme[8]

            for j, length in enumerate(lengths):
                res[-1] += theme[1]*(length+2)
                res[-1] += theme[2]

            res[-1] = res[-1][:-1] + theme[9]

    # Bottom
    # Ex: ╚═══╧═══╧═══╝
    res.append("")

    res[-1] += theme[10]
    for i, length in enumerate(lengths):
        res[-1] += theme[3]*(length+2)
        res[-1] += theme[11]

    res[-1] = res[-1][:-1]+theme[12]

    return '\n'.join(res)
