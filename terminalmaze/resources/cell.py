class Cell:
    def __init__(self, row: int, col: int) -> None:
        """
        Create a new node and set its row and column attributes.

        :param row: the row number of the cell
        :param col: the column number of the cell
        """
        self.row: int = row
        self.column: int = col
        self.links: set["Cell"] = set()
        self.neighbors: dict[str, "Cell"] = {}

    def link(self, cell: "Cell", bidi: bool = True) -> None:
        """
        Add a link to the cell.

        :param cell: the cell to link to
        :param bidi: If True, the link is bidirectional, defaults to True (optional)
        """
        self.links.add(cell)
        if bidi:
            cell.link(self, False)

    def unlink(self, cell: "Cell", bidi: bool = True) -> None:
        """
        Remove the cell from the list of links.

        :param cell: the cell to unlink from
        :param bidi: If True, the cell will unlink itself from the other cell, defaults to True (optional)
        """
        self.links.remove(cell)
        if bidi:
            cell.unlink(self, False)

    def get_links(self) -> set["Cell"]:
        """
        The function returns a set of cells linked to this cell.
        :return: Set of cells linked to this cell
        """
        return self.links

    def is_linked(self, cell: "Cell") -> bool:
        """
        Return if this cell is linked to the given cell.

        :param cell: the cell that is being checked
        :return: True if cell is linked else False
        """
        return cell in self.links
