import cv2
from ultralytics import YOLO
import supervision as sv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
pallete_model_path = os.path.join(script_dir, 'Training Files\\dataset\\runs\\detect\\train6\\weights\\', 'best.pt')

# do research into compiling opencv-python for NVIDIA GPUs, so that frame processing is faster

# put the resolution of your webcam here, may need optimising
webcam_res = 720

# bringing in the pallete model
# pallete_model_path = r".\Training Files\dataset\runs\detect\train6\weights\best.pt"
pallete_model = YOLO(pallete_model_path)

# accessing the webcam as an object (0 - hardware ID for a default webcam)
webcam = cv2.VideoCapture(0)

# with the webcam accessible, we now just run an infinite loop to process video
# if a user presses "q" the window will close
while webcam.isOpened() and cv2.waitKey(1) != 113:
    
    # reading a frame returns a tuple (boolean if we had a successful read, actual frame matrix)
    success, frame = webcam.read()
    
    if success:
        
        # getting prediction results from our pallete model
        results = pallete_model.predict(frame, imgsz=webcam_res)[0]
        
        # getting the detection tensor, which holds confidence scores
        detections = sv.Detections.from_ultralytics(results)
        
        # building a bounding box object for detected palletes
        pallete_annotator = sv.BoundingBoxAnnotator(thickness=4)
        
        # a labelling object that will extract the labels that the model has been trained for
        label_annotator = sv.LabelAnnotator(text_thickness=4, text_scale=2)
        
        # the bounding box prediction of where the pallete may be is placed on the frame 
        # this uses the passed frame to the callback & the tensor output from the model that embeds predictions
        frame_preditcs = pallete_annotator.annotate(    scene = frame,
                                                        detections = detections)
        
        # we then acquire the actual label ("pallete") from the tensor that the model has produced
        # again, if predicting for more than just the pallete, the tensor would be very large (justification for GPUs)
        labels = [f"{pallete_model.names[class_id]} {confidence:0.5f}" for _, _, confidence, class_id, _, _ in detections]
        
        # places the appropriate labels to the predictions in the frame
        # in our case, it's placing the pallete label, with its confidence score
        frame_annotated = label_annotator.annotate(     scene=frame_preditcs, 
                                                        detections=detections, 
                                                        labels = labels)
        
        # now we show the labelled frame onto the screen
        cv2.imshow("Near Real-Time Pallet Detection", frame_annotated)
        
    
    
# once a user chooses to quit, RELEASE THE HARDWARE
webcam.release()
cv2.destroyAllWindows()