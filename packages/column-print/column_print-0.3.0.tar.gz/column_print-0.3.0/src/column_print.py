"""Print in columns.

Unlike many similar utilities, it is NOT necessary for the strings to be
in a list before printing. column_print can print any sequence of strings
without knowing the length or number of strings in advance.

Note that this is NOT intended for printing tables, but simply to display
a long list more conveniently. For printing tables, "tabulate" or "columnize"
may be more suitable.


ColumnPrinter
-------------

A context manager class to print strings with padding to form columns.

Args:
    columns : int, default=2
        The number of columns in layout.

    width : int, default=80
        Total width of layout.
        If not supplied, column_print will attempt to read the width of the
        terminal (using shutil), and will fall back to 80 character with if
        the terminal with cannot be determined.

    colsep : str, default=" "
        Column separator.

Note that if a string is longer than the width of a column, it will
occupy more than one column, and the next printed item will be shifted
to the next available column.


"""

import logging

from shutil import get_terminal_size

logging.basicConfig(
    filename='column_print.log',
    filemode='w',
    level='DEBUG')


class ColumnPrinter:
    """Context manager class for printing columns.

    Attributes
    ----------
    columns : int, default=2
        Number of columns in layout.
    width : int, default=80
        Total width of layout (in characters).

        If not supplied, ColumnPrinter attempts to calculate width of terminal.
    colsep : str, default=" "
        Column separator.

    """
    def __init__(self, columns=2, width=None, colsep=" "):
        self.columns = columns
        # default width to terminal with or 80 if width can't be determined.
        self.width = width
        if width is None:
            self.width = get_terminal_size().columns
        self.colsep = colsep
        self._col_count = 0
        self._col_width = self.width // columns


    def __enter__(self):
        return self

    def __call__(self, txt):
        """Print in columns."""
        txt = str(txt)
        txt_len = len(txt + self.colsep)
        col_required = 1 + (txt_len // self._col_width)
        col_remain = self.columns - self._col_count
        # If can't fit on line, start new line.
        if col_required > col_remain:
            print('')
            self._col_count = 0
        print_width = 0
        # If not filling line, calculate total width to print.
        if self._col_count + col_required < self.columns:
            print_width = self._col_width * col_required
            # Add colsep space when spanning multiple columns.
            print_width += (col_required - 1) * len(self.colsep)
            print(txt.ljust(print_width), end=self.colsep)
        else:
            print(txt, end='')
        # Increment column count.
        if self._col_count >= self.columns:
            self._col_count = col_required
        else:
            self._col_count +=  col_required

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('')


def print_list(data, width=None, colsep=" "):
    """Print a list of items in equal spaced columns.

    The column width is calculated so that most, if not all the printed
    items fit in a single column, but if there is an occasional longer
    item, it may occupy  two or more columns.

    Note that this is NOT intended for printing tables, but simply to display
    a long list more conveniently.

    Parameters
    ----------

    data : list
        The list of printable items.

    width : int, default=80
        Total width of layout.
        If not supplied, column_print will attempt to read the width of the
        terminal (using shutil), and will fall back to 80 character with if
        the terminal with cannot be determined.

    colsep : str, default=" "
        Column separator.

    """
    if width is None:
        width = get_terminal_size().columns
    lengths = [len(str(val)) for val in data]
    lengths.sort()
    # 95th percentile
    p95 = lengths[int(round(len(data) * 0.95)) - 1]
    p100 = lengths[-1]
    width_p95 = int(((width - p95) / (p95 + len(colsep))) + 1)
    width_p100 = int(((width - p100) / (p100 + len(colsep))) + 1)
    logging.debug('%f  %f diff: %f', width_p95, width_p100, width_p95 - width_p100)
    if width_p100 >= 2 and width_p95 - width_p100 <= 1:
        columns = width_p100
        logging.debug('P100')
    else:
        columns = width_p95
        logging.debug('p95')
    with ColumnPrinter(columns, width, colsep) as cprint:
        for txt in data:
            cprint(txt)
