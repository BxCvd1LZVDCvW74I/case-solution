import pandas as pd
import numpy as np
import os
import tensorflow as tf
import keras
from joblib import load
from PIL import Image
from glob import glob

pd.options.display.max_rows = 9999

## Preprocess data (imagenet normalization)

def preprocess_imagenet(x):
    
    x /= 255.
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    x[..., 0] -= mean[0]
    x[..., 1] -= mean[1]
    x[..., 2] -= mean[2]

    x[..., 0] /= std[0]
    x[..., 1] /= std[1]
    x[..., 2] /= std[2]
        
    return x

## Read Images

def image_to_array(file_path):
    data = []
    for file in file_path:
        img = Image.open(file)
        img = img.resize((200, 200))
        img = np.asarray(img,dtype='float32')
        data.append(preprocess_imagenet(img))
    return np.array(data)

## Load inference model, define classes and data_path

MODEL_FILE = os.environ["MODEL_FILE"]
classes = ['shaver','smart-baby-bottle','toothbrush','wake-up-light']
data_path = sorted(glob('/home/inference/val-images/*'))

model = load(MODEL_FILE)

## Get predictions

preds = model.predict(image_to_array(data_path))
prediction = np.argmax(preds, axis=-1) 

## Print results and save as csv file

result = [classes[pred] for pred in prediction]
names = [name.split("/")[-1].split(".")[0] for name in data_path]

result_csv = pd.DataFrame({"Filename": names, "Class": result})
result_csv.to_csv("Predictions.csv", index = False)
print(result_csv)
