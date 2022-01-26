class Image_Index(object):
    def __init__(self, max_index: int, start_index: int = 0):
        self.index = start_index
        self.max_index = max_index

    def next(self) -> int:
        if self.index < self.max_index:
            self.index += 1

        return self.index

    def prev(self) -> int:
        if self.index > 0:
            self.index -= 1

        return self.index
