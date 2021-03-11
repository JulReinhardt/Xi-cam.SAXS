from xicam.core.intents import ImageIntent


class SAXSImageIntent(ImageIntent):

    canvas = "saxs_image_intent_canvas"

    def __init__(self, name:str, image, *args, **kwargs):
        super(SAXSImageIntent, self).__init__(name, image, *args, **kwargs)

        self.geometry = None

#TODO have a base overlay intent with mixin for SAXSintent
# class OverlayIntent(SAXSImageIntent):
#     canvas = "image_canvas"
#     # def __init__(self, *args, opacity: float=0.2, mask: np.ndarray, **kwargs):
#     def __init__(self, *args, opacity: float=0.2, **kwargs):
#         super(OverlayIntent, self).__init__(*args, **kwargs)
#         self.opacity = opacity
#         # self.mask = mask
