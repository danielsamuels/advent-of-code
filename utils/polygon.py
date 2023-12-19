class Polygon:
    def __init__(self, corners):
        self.corners = corners

    def shoelace(self):
        """
        Use the shoelace formula to determine the area

        0 1 2 3
        ._._._. 0
        | | | |
        ._._._. 1
        | | | |
        ._._._. 2
        | | | |
        ._._._. 3

        (0, 0), (1, 0), (2, 0), (3, 0)
        (0, 1), (1, 1), (2, 1), (3, 1)
        (0, 2), (1, 2), (2, 2), (3, 2)
        (0, 3), (1, 3), (2, 3), (3, 3)
        -> 9 (counts the inner squares)
        """
        total = 0
        i = 0
        while i != len(self.corners) - 1:
            total += self.corners[i][0] * self.corners[i + 1][1]
            total -= self.corners[i + 1][0] * self.corners[i][1]
            i += 1
        return abs(total + self.corners[-1][0] * self.corners[0][1] - self.corners[-1][-1] * self.corners[0][0]) / 2

    def picks(self, area, perimeter) -> int:
        return int(area - perimeter / 2 + 1) + perimeter
