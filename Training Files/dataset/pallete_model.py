from ultralytics import YOLO
from IPython.display import display, Image

# load a model (in this case, a detection model)
# using an "s" model which means it's a small model (faster, but less model predictors)
# if we have time, we can try a medium or large model
model = YOLO("yolov8s.pt")

# to make the model use the GPU
# this requires the CUDA compiler, so that NVIDIA GPU operations can occur (for an NVIDIA RTX GPU)
# only use this if you're training locally
# model.to('cuda')

# perform a model action (in this case, training the model)
# PARAMETERS:
# data - the path to the yaml file for the testing, training & validation
# epochs - number of iterations of training to drive the error to be minimised (affects performance, we can maybe play around with this for the report)
# patience - number of iterations that will occur if no further decrements in the loss function have occurred (prevents overfitting by ending training early)
#          - by setting the number of epochs to a very large number, you can safely achieve a desirable performance in tandem with a patience count
# imgsz - dimensions that the images are all resized to for training (affects model accuracy & computational complexity, can maybe play around here)
#       - for this testing scenario, I made the image size match with the dimensions of the inference video, despite the training pics being another dimension
# plots - shows training and validation metrics, definitely good for the project & analysing error minimisation

# full list of parameters is on their github
# this daya.yaml path is only relevant when using Google Colab for model training, please adjust to your local environment if training locally
# the results of training can be used in the Palette Video Run and Pallete Live Track python scripts
results = model.train(data = r"/content/drive/MyDrive/YOLOv8 Custom Pallet Detection/Training Files/data.yaml",
                      epochs = 2000,
                      patience = 50,
                      imgsz = 1080,
                      plots = True)

