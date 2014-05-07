from Captcha.Visual import Text, Backgrounds, Distortions, ImageCaptcha
from Captcha import Words

import random


class HTStyle(ImageCaptcha):
    textLayer = None

    def __init__(self, text=None):
        self.textLayer = Text.HtTextLayer(text)
        ImageCaptcha.__init__(self)

    def getLayers(self):
        return [random.choice([
                Backgrounds.CroppedImage(),
                Backgrounds.TiledImage(),
                        ]),
                self.textLayer,
                Distortions.SineWarp(), ]

    def get_list_captcha(self):
        return self.textLayer.get_list_captcha()


if __name__ == "__main__":
    """Humantech Test Captcha """
    g = HTStyle()
    i = g.render()
    i.save("output.png")
    i.show()
    print g.solutions
    print g.get_list_captcha()
