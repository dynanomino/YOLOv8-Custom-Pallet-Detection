import supervision as sv
import numpy as np
from ultralytics import YOLO
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'Training Files\\dataset\\runs\\detect\\train6\\weights\\', 'best.pt')

# providing the video path, on which we want to perform predictions
source = os.path.join(script_dir, 'Validation Video.mov')

# Initialize the YOLOv8 model we've trained for the pallete
# Parameters:   model_path  ->  path to our custom mode
#               device      ->  the processing unit to use
pallete_detector = YOLO(model_path)

# loading the video from memory
video_info = sv.VideoInfo.from_video_path(source)


#####################################################################


                    # BACKGROUND KNOWLEDGE


#####################################################################


# now we perform model inference with our custom model
# model inference is the act of using a trained ML model to perform predictions on never-seen data
# Hyperparameters:
#             conf              ->  minimum level of certainty that the model should acquire to predict that an object is a pallete
#             iou               ->  a hyperparameter that quantifies the ratio of overlap between "ground truth"...
#  (intersection over union)        ... (actual object location on screen) and the prediction of our model (where it thinks ...
#                                   ... the object is via the box annotation), it's important for penalising wrong predictions
#                               ->  IoU score of 0 means no overlap, IoU score of 1 means perfect overlap


# a callback (function) to return frames with prediciton annotations
def process_frame(frame: np.ndarray, _) -> np.ndarray:
    
    # the neural network performs predictions from the frame
    results = pallete_detector.predict(frame, imgsz=1080)[0]
    
    # a tensor is acquired, in which the confidence score of the prediciton is embedded
    # if we were detecting for more than just a pallete, this would be a very very big tensor
    detections = sv.Detections.from_ultralytics(results)
    
    # a bounding box object, which has properties for describing how the box is rendered on the screen
    pallete_annotator = sv.BoundingBoxAnnotator(thickness=4)
    
    # a labelling object that will extract the labels that the model has been trained for
    label_annotator = sv.LabelAnnotator(text_thickness=4, text_scale=2)
    
    # print("Detection Data \n \n")
    # print(detections)
    # print(" \n \n")
    
    # the bounding box prediction of where the pallete may be is placed on the frame 
    # this uses the passed frame to the callback & the tensor output from the model that embeds predictions
    frame = pallete_annotator.annotate( scene = frame,
                                        detections = detections)
    
    # we then acquire the actual label ("pallete") from the tensor that the model has produced
    # again, if predicting for more than just the pallete, the tensor would be very large (justification for GPUs)
    labels = [f"{pallete_detector.names[class_id]} {confidence:0.2f}" for _, _, confidence, class_id, _, _ in detections]
    
    # places the appropriate labels to the predictions in the frame
    # in our case, it's placing the pallete label, with a confidence score of at least 0.5
    frame = label_annotator.annotate(   scene=frame, 
                                        detections=detections, 
                                        labels = labels)
    
    # and the processed frame is then returned, eventually the video is post-processed
    return frame

# process the video, returns the video with annotations applied to it
sv.process_video(source_path=source, target_path=f"Pallete_Results.mp4", callback=process_frame)