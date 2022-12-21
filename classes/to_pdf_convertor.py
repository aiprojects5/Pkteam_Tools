import config
import shutil
import aspose.slides as slides

from docx2pdf import convert


class To_pdf_convertor:
    def __init__(self, file, filename, api):
        self.file = file
        self.filename = filename[:-4]
        self.api = api
        if self.api == 'image_to_pdf':
            self.returned_value = self.image_to_pdf()
        elif self.api == 'docx_to_pdf':
            self.returned_value = self.docx_to_pdf()
        elif self.api == 'ppt_to_pdf':
            self.returned_value = self.ppt_to_pdf()

    def image_to_pdf(self):
        self.file[0].save(f"{config.pdf}/{self.filename}.pdf", save_all=True, append_images=self.file[1:])
        return f"{config.pdf}/{self.filename}.pdf"

    def docx_to_pdf(self):
        with open(f"{config.docx}/{self.filename}.docx", "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)
        convert(f"{config.docx}/{self.filename}.docx", f"{config.pdf}/{self.filename}.pdf")
        return f"{config.pdf}/{self.filename}.pdf"

    def ppt_to_pdf(self):
        with open(f"{config.pptx}/{self.filename}.pptx", "wb") as buffer:
            shutil.copyfileobj(self.file.file, buffer)
        pres = slides.Presentation(f"{config.pptx}/{self.filename}.pptx")
        pres.save(f"{config.pdf}/{self.filename}.pdf", slides.export.SaveFormat.PDF)
        return f"{config.pdf}/{self.filename}.pdf"