import shutil

import aspose.slides as slides
import pandas as pd
import pdftotree
import pytesseract
from PIL import Image
from pdf2docx import Converter
from pdf2image import convert_from_path

import config
import os
from functions.function import zip


class Pdf_convertor:
    def __init__(self, file, filename, api):
        self.file = file.file
        self.filename = filename[:-4]
        self.api = api
        self.returned_value = self.save_pdf()

    def save_pdf(self):
        with open("{0}/{1}.pdf".format(config.pdf, self.filename), "wb") as buffer:
            shutil.copyfileobj(self.file, buffer)
        # self.file.save("{0}/{1}.pdf".format(config.pdf, self.filename))
        if self.api == 'pdf_to_jpg':
            return self.pdf_to_jpg()
        elif self.api == 'pdf_to_png':
            return self.pdf_to_png()
        elif self.api == 'pdf_to_docx':
            return self.pdf_to_docx()
        elif self.api == 'pdf_to_pptx':
            return self.pdf_to_pptx()
        elif self.api == 'pdf_to_excel':
            return self.pdf_to_jpg()
        elif self.api == 'pdf_to_html':
            return self.pdf_to_html()
        elif self.api == 'pdf_compress':
            return self.pdf_compress()

    def pdf_to_jpg(self):
        files_path = []
        images = convert_from_path('{0}/{1}.pdf'.format(config.pdf, self.filename), poppler_path=config.poppler)
        os.remove('{0}/{1}.pdf'.format(config.pdf, self.filename))
        for i in range(len(images)):
            images[i].save('{0}/{1}{2}.jpg'.format(config.images, self.filename, i), 'JPEG')
            files_path.append('{0}/{1}{2}.jpg'.format(config.images, self.filename, i))
        if self.api == 'pdf_to_excel':
            return self.pdf_to_excel(files_path)
        else:
            zip(files_path, config.images, self.filename)
            return f'{config.images}/{self.filename}.zip'

    def pdf_to_png(self):
        files_path = []
        images = convert_from_path('{0}/{1}.pdf'.format(config.pdf, self.filename), poppler_path=config.poppler)
        os.remove('{0}/{1}.pdf'.format(config.pdf, self.filename))
        for i in range(len(images)):
            images[i].save('{0}/{1}{2}.png'.format(config.images, self.filename, i), 'PNG')
            files_path.append('{0}/{1}{2}.png'.format(config.images, self.filename, i))

        zip(files_path, config.images, self.filename)
        return f'{config.images}/{self.filename}.zip'

    def pdf_to_docx(self):
        cv = Converter(f'{config.pdf}/{self.filename}.pdf')
        cv.convert(f'{config.docx}/{self.filename}.docx')
        cv.close()
        docx = f'{config.docx}/{self.filename}.docx'
        return docx

    def pdf_to_pptx(self):
        # subprocess.run(["pdf2pptx", f'{config.pdf}/{self.filename}.pdf', '-o' f'{config.pptx}/{self.filename}.pptx'])
        with slides.Presentation() as presentation:
            presentation.slides.remove_at(0)
            presentation.slides.add_from_pdf(f'{config.pdf}/{self.filename}.pdf')
            presentation.save(f'{config.pptx}/{self.filename}.pptx', slides.export.SaveFormat.PPTX)
        return f'{config.pptx}/{self.filename}.pptx'

    def pdf_to_excel(self, files_path):
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        final_text = pd.Series()
        for file in files_path:
            text = pytesseract.image_to_string(Image.open(f"{file}"))
            text = pd.Series(text.split('\n'))
            final_text = pd.concat([final_text, text])
        final_text.to_excel(f"{config.excel}/{self.filename}.xlsx", sheet_name='Sheet1')
        return f"{config.excel}/{self.filename}.xlsx"

    def pdf_to_html(self):
        pdftotree.parse('{0}/{1}.pdf'.format(config.pdf, self.filename), html_path=f'{config.html}/{self.filename}.html', model_type=None, model_path=None, visualize=False)
        return f'{config.html}/{self.filename}.html'

    # def pdf_compress(self):
    #     reader = PdfReader(f"{config.pdf}/{self.filename}.pdf")
    #     writer = PdfWriter()
    #
    #     for pages in reader.pages:
    #         pages.compress_content_streams()
    #         writer.add_page(pages)
    #     writer.add_metadata(reader.metadata)
    #     with open(f"{config.compressed_pdf}/{self.filename}.pdf", "wb") as fp:
    #         writer.write(fp)
