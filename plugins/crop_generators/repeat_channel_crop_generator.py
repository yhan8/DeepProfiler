import numpy as np
import tensorflow as tf
import deepprofiler.imaging.cropping
from keras.applications import inception_resnet_v2

def repeat_channels(crops, network_input_size):
    resized_crops = tf.image.resize_images(crops, size=(network_input_size, network_input_size))
    reordered_channels = tf.transpose(resized_crops, [3, 0, 1, 2])
    reshaped_data = tf.reshape(reordered_channels, shape=[-1, network_input_size, network_input_size, 1])
    rgb_data = tf.image.grayscale_to_rgb(reshaped_data)
    return rgb_data


class GeneratorClass(deepprofiler.imaging.cropping.CropGenerator):

    def generate(self, sess, global_step=0):
        raise NotImplementedError()


class SingleImageGeneratorClass(deepprofiler.imaging.cropping.SingleImageCropGenerator):

    def __init__(self, config, dset):
        super().__init__(config, dset)
        width = self.config["dataset"]["locations"]["box_size"]
        height = width
        channels = len(self.config["dataset"]["images"]["channels"])
        self.crop_ph = tf.placeholder(tf.float32, (None, width, height, channels))
        self.resized = repeat_channels(self.crop_ph, self.config["profile"]["use_pretrained_input_size"])

    def generate(self, session, global_step=0):
        crops = session.run(self.resized, feed_dict={self.crop_ph:self.image_pool})
        labels = np.tile(self.label_pool, [3,1])

        global_step += 1

        yield (crops, labels)

