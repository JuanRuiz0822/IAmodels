#Librerias necesarias
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from IPython.display import display, Image as IPImage
import os

!pip install ultralytics
import cv2
from PIL import Image
from IPython.display import display
from ultralytics import YOLO
import yaml

from google.colab import drive
drive.mount('/content/drive')
