import base64
import io
from kivy.base import runTouchApp
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

"""
pathstring64 is the last argument to read the file where this image base64 encoded and be rendered.
"""

class DecodeImage64(Image):
    def __init__(self, pathstring64, **k):
        super(DecodeImage64, self).__init__(**k)
        self.source="i.jpg"
        raw_base64_string = open(pathstring64,'r').read()
        self._data = io.BytesIO(base64.b64decode(raw_base64_string))
        self.coreimage=CoreImage(self._data, ext="jpg")
        self.texture=self.coreimage.texture
                

runTouchApp(DecodeImage64("path/to/img64.txt"))
