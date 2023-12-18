from utils.grid import Position


class RangeGrid:
    """
    Allow borders of a grid to be defined as ranges
    """
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

        self.width = max(max(r) for ranges in rows.values() for r in ranges)
        self.height = max(max(r) for ranges in columns.values() for r in ranges)

    @property
    def corners(self):
        result = []
        for column, ranges in self.columns.items():
            for r in ranges:
                result.append((column, min(r)))
                result.append((column, max(r)))

        for row, ranges in self.rows.items():
            for r in ranges:
                result.append((min(r), row))
                result.append((max(r), row))

        return result

    def __contains__(self, item: Position):
        column, row = item
        found = False

        column_ranges = self.columns.get(column, [])
        row_ranges = self.rows.get(row, [])

        for r in column_ranges:
            if row in r:
                return True

        for r in row_ranges:
            if column in r:
                return True

        return False
