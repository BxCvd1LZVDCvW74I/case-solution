FROM python:3.6

RUN pip install joblib
RUN pip install Pillow
RUN pip install numpy
RUN pip install pandas
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.1.0-cp36-cp36m-manylinux2010_x86_64.whl
RUN pip install keras

RUN mkdir model
RUN mkdir val-images

ENV MODEL_FILE=/home/inference/model_serial.joblib

COPY inference.py /home/inference/inference.py
COPY model_serial.joblib /home/inference/model_serial.joblib
COPY val-images/. /home/inference/val-images/.

RUN python3 /home/inference/inference.py



