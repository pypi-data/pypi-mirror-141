class SnekRay(object):
    WIDTH = 640
    HEIGHT = 360

    def __init__(self, width=WIDTH, height=HEIGHT) -> None:
        self.height = height
        self.width = width

    @classmethod
    def get_default_dimensions(cls):
        return (cls.WIDTH, cls.HEIGHT)

    def get_dimensions(self):
        return (self.width, self.height)
