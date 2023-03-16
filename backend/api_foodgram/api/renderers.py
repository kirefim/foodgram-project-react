from io import BytesIO
import os

from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import renderers


class PDFRenderer(renderers.BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'

    def _get_http_response(self, obj):
        response = HttpResponse(content_type=self.media_type)
        response['Content-Disposition'] = ('attachment;'
                                           'filename="shopping_cart.pdf"')
        response.write(obj)
        return response

    @staticmethod
    def get_topic():
        buffer = BytesIO()
        doc = canvas.Canvas(buffer, A4)
        font_filename = os.path.join(
            settings.BASE_DIR, 'data', 'Montserrat Alternates.ttf'
        )
        pdfmetrics.registerFont(TTFont('Montserrat_Alternates', font_filename))
        doc.setFont('Montserrat_Alternates', 45)
        doc.drawCentredString(x=300, y=800, text='Проект FOODGRAM')
        return buffer, doc

    def render(self, data, accepted_media_type=None, renderer_context=None):
        buffer, doc = self.get_topic()
        doc.setFont('Montserrat_Alternates', 30)
        if len(data) != 0:
            doc.drawCentredString(x=300, y=700, text='Список покупок')
            textobject = doc.beginText()
            textobject.setTextOrigin(50, 650)
            textobject.setFont('Montserrat_Alternates', 20)
            ingredients = [
                f'{item.name} - {item.amount} ({item.measurement_unit})'
                for item in data
            ]
            textobject.textLines(ingredients)
            doc.drawText(textobject)
        else:
            doc.drawCentredString(x=300, y=700,
                                  text='Ваш список покупок пуст :(')
        doc.showPage()
        doc.save()
        pdf = buffer.getvalue()
        buffer.close()
        return self._get_http_response(pdf)
