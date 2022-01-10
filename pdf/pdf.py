#
# Copyright (c) 2021-2022 Christophe 'SntPx' RIVIERE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import pagesizes, colors
from reportlab.lib.units import cm
from functools import partial
import itertools
import uuid
import io
from __init__ import __version__
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from collections import deque

pdfmetrics.registerFont(
    TTFont('Playball',
           os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'Playball-Regular.ttf')
           )
)

PAGE_WIDTH, PAGE_HEIGHT = [x / cm for x in A4]
PAGESIZE = pagesizes.portrait(A4)
MARGINS = {
    'left': 0.5 * cm,
    'right': 0.5 * cm,
    'top': 1.5 * cm,
    'bottom': 1.5 * cm
}
STYLES = getSampleStyleSheet()


def get_colors():
    # List generated from snippet from
    # https://stackoverflow.com/questions/1573053/javascript-function-to-convert-color-names-to-hex-codes/24390910
    return ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black',
            'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
            'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
            'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen',
            'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue',
            'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray',
            'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite',
            'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred ',
            'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon',
            'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgrey', 'lightgreen',
            'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue',
            'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine',
            'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
            'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream',
            'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange',
            'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred',
            'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple',
            'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell',
            'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue',
            'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
            'yellow', 'yellowgreen', ]


DEFAULT_STYLE = {
            'parent': STYLES['Normal'],
            'fontName': 'Playball',
            'fontSize': 10,
            'leading': 12,
            'leftIndent': 0,
            'rightIndent': 0,
            'firstLineIdent': 0,
            'spaceBefore': 0,
            'spaceAfter': 0,
            'bulletFontName': 'Arial',
            'bulletFontSize': 10,
            'bulletIndent': 1,
            'textColor': 'black',
            'backColor': None,
            'wordWrap': None,
            'borderWidth': 0,
            'borderPadding': 0,
            'borderColor': None,
            'borderRadius': None,
            'allowWidows': 1,
            'allowOrphans': 0,
            'endDots': True,
            'splitLongWords': 1
        }


HEADER = {
    'text': f'Apix v{__version__}',
    'style': ParagraphStyle(
        'ky_header',
        fontName='Helvetica',
        fontSize=5,
        bulletFontName='Helvetica',
        bulletFontSize=9,
        bulletAnchor='start'
    )
}
FOOTER = {
    'text': f'Document généré par Apix v{__version__}',
    'style': ParagraphStyle(
        'ky_footer',
        fontName='Helvetica',
        fontSize=5,
        bulletFontName='Helvetica',
        bulletFontSize=9,
        bulletAnchor='start'
    )
}


DEFAULT_TITLE = 'Rapport Butineur Apix'
DEFAULT_HEADER = f'Butineur Apix v{__version__}'
DEFAULT_HEADER_STYLE = ParagraphStyle(
    'default_header_style',
    fontName='Playball',
    fontSize=8,
)
DEFAULT_FOOTER = DEFAULT_HEADER
DEFAULT_FOOTER_STYLE = DEFAULT_HEADER_STYLE


class BasePDF:

    def __init__(self, content=[], title=None):
        self.title = title
        self._templates = []
        self._pages_ids = []
        if self.title is None:
            self.title = DEFAULT_TITLE
        self.title = 'no'
        self.story = content
        self._story = self.story + []
        self._buffer = io.BytesIO()
        self.pdf = SimpleDocTemplate(self._buffer, pagesize=PAGESIZE,
                                     leftMargin=MARGINS['left'],
                                     rightMargin=MARGINS['right'],
                                     topMargin=MARGINS['top'],
                                     bottomMargin=MARGINS['bottom'],
                                     title=self.title,
                                     _pageBreackQuick=1
                                     )
        self.add_page(Frame(self.pdf.leftMargin, self.pdf.bottomMargin, self.pdf.width, self.pdf.height,
                            id='mainContent'))

    def add_page(self, frames):
        page_id = uuid.uuid4()
        #if not isinstance(frames, (list, tuple)):  # For a first version, let's hope it's a direct Frame instance
        #    frames = [frames]
        while page_id in self._pages_ids:
            page_id = uuid.uuid4()
        self._pages_ids.append(page_id)
        self._templates.append(
            PageTemplate(
                id=page_id,
                frames=frames,
                # TODO: Add onPage to get background, header and footer, plus watermark
            )
        )

    def make_pdf_classes(self, data):
        if not isinstance(data, (list, tuple)):
            raise TypeError(f'The data fed to the PDF generator MUST be a list or a tuple. Got {type(data)} instead!')

        for element in data:
            if not isinstance(element, dict):
                raise TypeError(f'The elements submitted to the PDF generator MUST return type dict. '
                                f'Got {type(element)} instead!')

            if 'type' not in element.keys():
                raise KeyError(f'Element to be added does not have a "type" key! This is necessary!')
            if 'content' not in element.keys():
                raise KeyError(f'Element to be added does not have a "content" key! This is necessary!')

            if 'style' not in element.keys():
                if element['type'].lower() == 'paragraph':
                    element['style'] = ParagraphStyle('default_style', **DEFAULT_STYLE)
                elif element['type'].lower() == 'table':
                    element['style'] = TableStyle([
                        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 11,),
                        ('FONT', (1, 1), (-1, -1), 'Playball', 10),
                        ('GRID', (0, 0), (-1, -1), 0.25, colors.lavender)
                    ])

            if element['type'].lower() == 'paragraph':
                self._story.append(Paragraph(element['content'], element['style']))

            elif element['type'].lower() == 'table':
                self._story.append(Table(element['content'], style=element['style']))

    def make_pdf(self):
        self.pdf.addPageTemplates(self._templates)
        self.pdf.build(self._story)
        self._buffer.seek(0)
        return self._buffer
