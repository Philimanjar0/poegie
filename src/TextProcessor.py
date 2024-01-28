from common import reference_enum

class ImageProcessor():
    def __init__(self):
        pass

    def parseClipboard(self, input):
        split = input.split("\n")
        split2 = split[2].split(" ")
        name = split2[0]
        return reference_enum.index(name)
        