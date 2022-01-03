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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from functools import partial
import uuid
import io

PAGE_WIDTH, PAGE_HEIGHT = [x/cm for x in A4]
PAGESIZE = pagesizes.portrait(A4)
MARGINS = {
    'left': 2.2 * cm,
    'right': 2.2 * cm,
    'top': 1.5 * cm,
    'bottom': 1.5 * cm
}
STYLES = getSampleStyleSheet()


def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()


def header(canvas, doc, content):
    canvas.saveSate()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h)
    canvas.restoreState()


def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, header_content)
    footer(canvas, footer_content)


class PDF:

    def __init__(self, content, title, header, footer, **kwargs):
        self.title = title
        self.content = []
        self._templates = []
        self._page_ids = []
        self._header = header
        self._footer = footer
        self._buffer = io.BytesIO()
        self.content = content
        self._author = 'Anononymous'
        if "author" in kwargs:
            self._author = kwargs['author']
        self.pdf = SimpleDocTemplate(self._buffer, pagesize=PAGESIZE,
                                     lefMargin=MARGINS['left'],
                                     rightMargin=MARGINS['right'],
                                     topMargin=MARGINS['top'],
                                     bottomMargin=MARGINS['bottom'],
                                     title=self.title,
                                     _pageBreackQuick=1
                                     )
        self.add_page(Frame(self.pdf.leftMargin, self.pdf.bottomMargin, self.pdf.width, self.pdf.height, id='mainContent'))


    def get_pdf(self):
        return self.pdf

    def _set_author(self, canvas, _):
        canvas.setAuthor(self._author)

    def add_page(self, frames):
        page_id = uuid.uuid4()
        while page_id in self._page_ids:
            page_id = uuid.uuid4()
        self._page_ids.append(page_id)
        self._templates.append(
            PageTemplate(
                id=page_id,
                frames=frames,
                #onPage=partial(header_and_footer, header_content=self._header, footer_content=self._footer)
            )
        )

    def make_pdf(self):
        self.pdf.addPageTemplates(self._templates)
        self.pdf.build(self.content, onFirstPage=self._set_author)
        self._buffer.seek(0)
        return self._buffer
