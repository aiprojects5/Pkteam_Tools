import os

root_path = os.path.dirname(os.path.abspath(__file__))

static = os.path.join(root_path, 'static')
images = os.path.join(static, 'images')
pdf = os.path.join(static, 'pdf')
docx = os.path.join(static, 'docx')
pptx = os.path.join(static, 'pptx')
excel = os.path.join(static, 'excel')
html = os.path.join(static, 'html')
compressed_pdf = os.path.join(static, 'compressed_pdf')
qr_images = os.path.join(static, 'qr_images')
images_audio_video = os.path.join(static, 'images_audio_video')
images_video = os.path.join(static, images_audio_video, 'images')
audio = os.path.join(static, images_audio_video, 'audio')
video = os.path.join(static, images_audio_video, 'video')
rm_bg = os.path.join(static, 'rm_bg')
# zip = os.path.join(static, 'zip')
poppler = os.path.join(root_path, 'poppler-22.04.0/Library/bin')
