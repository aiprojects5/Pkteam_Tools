import tensorflow as tf
import cv2
import numpy as np
import config
import os
import qrcode

from functions.metrics import iou, dice_coef, dice_loss
from keras.utils import load_img, img_to_array
from keras.preprocessing import image


class Background_remove:
    def __init__(self, file, filename, api):
        self.file = file
        self.filename = filename[:-4]
        self.api = api
        self.file_path = f"{config.rm_bg}/{self.filename}.png"
        self.returned_value = self.save_image()

    def save_image(self):
        cv2.imwrite(self.file_path, self.file)
        if self.api == 'image_background':
            return self.remove_background()
        elif self.api == 'image_to_qrcode':
            return self.image_to_qrcode()

    def remove_background(self):
        model = tf.keras.models.load_model("model.h5",
                                           custom_objects={'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss})
        """ Read The Image """
        target_shape = (512, 512, 3)

        temp_img = load_img(self.file_path, target_size=target_shape)
        img = img_to_array(temp_img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        pred = model.predict(img.reshape(1, 512, 512, 3))
        pred[pred > 0.5] = 1.0
        pred[pred < 0.5] = 0.0

        img = cv2.convertScaleAbs(pred, alpha=255.0)
        cv2.imwrite(f'{config.rm_bg}/segmented_{self.filename}.png', img.reshape(512, 512))

        img_org = cv2.imread(self.file_path)
        img_mask = cv2.imread(f'{config.rm_bg}/segmented_{self.filename}.png')
        img_org = cv2.resize(img_org, (400, 400), interpolation=cv2.INTER_AREA)
        img_mask = cv2.resize(img_mask, (400, 400), interpolation=cv2.INTER_AREA)

        for h in range(len(img_mask)):
            for w in range(len(img_mask)):
                if img_mask[h][w][0] == 0:
                    for i in range(3):
                        img_org[h][w][i] = 0
                else:
                    continue

        tmp = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)

        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(img_org)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        cv2.imwrite(f"{config.rm_bg}/{self.filename}_final_image.png", dst)
        os.remove(f'{config.rm_bg}/segmented_{self.filename}.png')
        os.remove(self.file_path)
        return f"{config.rm_bg}/{self.filename}_final_image.png"

    def image_to_qrcode(self):
        img = qrcode.make(self.file_path)
        img.save(f"{config.qr_images}/{self.filename}.png")
        return f"{config.qr_images}/{self.filename}.png"
