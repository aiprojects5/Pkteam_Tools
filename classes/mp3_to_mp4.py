import shutil
import config
import cv2
import os

from mutagen.mp3 import MP3
from PIL import Image
from moviepy import editor
from pathlib import Path


class MP3ToMP4:
    def __init__(self, images_list, images_names, audio, audio_name):
        self.images_list = images_list
        self.images_names = images_names
        # self.image_name = image_name
        self.audio = audio
        self.audio_name = audio_name
        self.video_path_name = config.video
        self.returned_value = self.save()

    def save(self):
        for index, image in enumerate(self.images_list):
            cv2.imwrite(f"{config.images_video}/{self.images_names[index]}", image)

        with open(f"{config.audio}/{self.audio_name}", "wb") as buffer:
            shutil.copyfileobj(self.audio.file, buffer)
        return self.create_video()

    def get_lenth(self):
        song = MP3(f"{config.audio}/{self.audio_name}")
        return int(song.info.length)

    def get_images(self):
        images_list = list()
        for images in os.listdir(config.images_video):
            image = Image.open(f"{config.images_video}/{images}").resize((800, 800), Image.ANTIALIAS)
            images_list.append(image)
            os.remove(f"{config.images_video}/{images}")
        return images_list

    def create_video(self):
        length_audio = self.get_lenth()
        images_list = self.get_images()
        duration = int(length_audio / len(images_list)) * 1000
        images_list[0].save(f"{config.video}/temp.gif", save_all=True, append_images=images_list[1:], duration=duration)
        return self.combine_audio()

    def combine_audio(self):
        video = editor.VideoFileClip(f"{config.video}/temp.gif")
        audio = editor.AudioFileClip(f"{config.audio}/{self.audio_name}")
        final_video = video.set_audio(audio)
        final_video.write_videofile(f"{config.video}/{self.audio_name[:-4]}.mp4", fps=60)
        return f"{config.video}/{self.audio_name[:-4]}.mp4"
