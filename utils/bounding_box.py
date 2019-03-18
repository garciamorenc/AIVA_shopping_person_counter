class Bbox:
    """
    Class that defines the type bounding box used by the rest of the application to indicate zones of interest,
    detection of pedestrians and basic operations. Corresponds to the representation of the coordinates of
    a rect angle
    """

    def __init__(self, x0, y0, x1, y1):
        self.x0 = int(x0)
        self.y0 = int(y0)
        self.x1 = int(x1)
        self.y1 = int(y1)
