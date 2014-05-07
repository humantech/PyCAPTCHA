""" Captcha.Visual.Text

Text generation for visual CAPTCHAs.
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

#import os
import re
import random
from PIL import ImageFont
from PIL import ImageDraw

from Captcha import Visual, File, get_random


class FontFactory(File.RandomFileFactory):
    """Picks random fonts and/or sizes from a given list.
       'sizes' can be a single size or a (min,max) tuple.
       If any of the given files are directories, all *.ttf found
       in that directory will be added.
    """
    extensions = [".ttf"]
    basePath = "fonts"

    def __init__(self, sizes, *fileNames):
        File.RandomFileFactory.__init__(self, *fileNames)

        if type(sizes) is tuple:
            self.minSize = sizes[0]
            self.maxSize = sizes[1]
        else:
            self.minSize = sizes
            self.maxSize = sizes

    def pick(self):
        """Returns a (fileName, size) tuple that can be passed to ImageFont.truetype()"""
        fileName = File.RandomFileFactory.pick(self)
        size = int(random.uniform(self.minSize, self.maxSize) + 0.5)
        return (fileName, size)

# Predefined font factories
defaultFontFactory = FontFactory((30, 50), "vera")


class TextLayer(Visual.Layer):
    """Represents a piece of text rendered within the image.
       Alignment is given such that (0,0) places the text in the
       top-left corner and (1,1) places it in the bottom-left.

       The font and alignment are optional, if not specified one is
       chosen randomly. If no font factory is specified, the default is used.
    """
    def __init__(self, text,
                 alignment   = None,
                 font        = None,
                 fontFactory = None,
                 textColor   = "black",
                 borderSize  = 0,
                 borderColor = "white",
                 ):

        if fontFactory is None:
            global defaultFontFactory
            fontFactory = defaultFontFactory

        if font is None:
            font = fontFactory.pick()

        if alignment is None:
            alignment = (random.uniform(0,1),
                         random.uniform(0,1))

        self.text        = text
        self.alignment   = alignment
        self.font        = font
        self.textColor   = textColor
        self.borderSize  = borderSize
        self.borderColor = borderColor

    def render(self, img):
        font = ImageFont.truetype(*self.font)
        textSize = font.getsize(self.text)
        draw = ImageDraw.Draw(img)

        # Find the text's origin given our alignment and current image size
        x = int((img.size[0] - textSize[0] - self.borderSize*2) * self.alignment[0] + 0.5)
        y = int((img.size[1] - textSize[1] - self.borderSize*2) * self.alignment[1] + 0.5)

        # Draw the border if we need one. This is slow and ugly, but there doesn't
        # seem to be a better way with PIL.
        if self.borderSize > 0:
            for bx in (-1,0,1):
                for by in (-1,0,1):
                    if bx and by:
                        draw.text((x + bx * self.borderSize,
                                   y + by * self.borderSize),
                                  self.text, font=font, fill=self.borderColor)

        # And the text itself...
        draw.text((x, y), self.text, font=font, fill=self.textColor)


class HtTextLayer(Visual.Layer):

    def __init__(self, text=None):
        self.list_captcha = {'number': {},
                             'lower': {},
                             'upper': {},
                             'captcha': None}
        if text is None:
            text = get_random()

        self.list_captcha['captcha'] = text

    def render(self, img):
        draw = ImageDraw.Draw(img)
        axisX = 10
        axisY = 19
        self._draw_text_lettler_by_lettler(
            draw, self.list_captcha['captcha'], axisX, axisY)

    def get_list_captcha(self):
        return self.list_captcha

    def _draw_text_lettler_by_lettler(self, draw, text, x, y):
        if(text.__len__() != 0):
            letter, remainder = self._separate_first_letter(text)
            x, font, color = self._get_axisx_color_font_from_text(letter, x)
            self._draw_and_add_list_captcha(draw, letter, font, color, x, y)
            self._draw_text_lettler_by_lettler(draw, remainder, x, y)

    def _draw_and_add_list_captcha(self, draw, letter, font, color, x, y):
        draw.text((x, y), letter, font=font, fill=color)
        self._add_list_captcha(color, letter)

    def _get_font(self):
        global defaultFontFactory
        fontFactory = defaultFontFactory
        return ImageFont.truetype(*fontFactory.pick())

    def _get_collor(self):
        return random.choice(['black', 'blue', 'green', 'red'])

    def _get_size(self, font, text):
        return font.getsize(text)

    def _add_list_captcha(self, color, text):
        if(self._get_first_number(text) is not None):
            self._create_new_node_or_set_more_one_color(color, text, 'number')
        if(self._get_first_lower_case(text) is not None):
            self._create_new_node_or_set_more_one_color(color, text, 'lower')
        if(self._get_first_upper_case(text) is not None):
            self._create_new_node_or_set_more_one_color(color, text, 'upper')

    def _create_new_node_or_set_more_one_color(self, text, color, node):
        if(text in self.list_captcha[node]):
            self.list_captcha[node][text].append(color)
        else:
            self.list_captcha[node][text] = [color]

    def _get_axisx_color_font_from_text(self, text, x):
        font = self._get_font()
        color = self._get_collor()
        size = self._get_size(font, text)[0] + x

        return size, font, color

    def _separate_first_letter(self, text):
        return text[0] + '', text[1:]

    def _get_first_number(self, text):
        numbers = re.compile('[0-9]')
        return numbers.search(text)

    def _get_first_lower_case(self, text):
        lowerCase = re.compile('[a-z]')
        return lowerCase.search(text)

    def _get_first_upper_case(self, text):
        upperCase = re.compile('[A-Z]')
        return upperCase.search(text)

### The End ###
