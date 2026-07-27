Hello, welcome to the YOLOv8 Custom Pallet Detection model repo!

**Credits:** <\n> 
**Danny Wanjohi (@dynanomino)** - Research, image dataset collection plan, image labelling, model training & inference
**Arie Fawwaz** - Research, Image collection, image labeling
**Isaac Eva** - Research, Image collection, image labeling

This repo contains all code necessary for custom pallet model training and inference. Please note that training was done on the Google Colab platform, 
and thus the model training python code located at "Training Files\dataset\pallete_model.py" uses the file path for recognised by Google Colab.

If wishing to perform local model training, please adjust the file path in pallete_model.py as mentioned above. A helpful comment is also written
in the script.

Feel free to run inference on the sample "Validation Video.mov" video using the Pallete_Video_Run.py script! Here's a screenshot of what inference
looks like after processing (the model can also be tested for classifying in a different manufacturing machine):

<img width="1879" height="1246" alt="image" src="https://github.com/user-attachments/assets/5fc40525-c971-49ed-b192-9acb11f20839" />

<h2>Data Acquisition</h2>

Training the model to achieve the goal of identifying the pallet on the conveyor would
require supervised datasets. The first step was to use a webcam attached to a tripod
for the setup. This is done to ensure the stability and consistency of the images. The image
collection occurs at four different distances as shown in the figure below. These distances are
categorized as Near Near range, Near Far range, Far Near range, and Far Far range.

<img width="1912" height="952" alt="image" src="https://github.com/user-attachments/assets/c3c2cc44-7ae0-41b7-b073-c2ae59e3bd00" />

The steps for taking the images are listed below:
1. Place the pallet on the conveyor in one position
2. Take pictures of the pallet on the conveyor, varying the angle at which the image is taken
3. Split these images such that 80% of images are used for training, and 20% are used for
testing, in an even spread across angles
4. Repeat steps 1 - 3 for all distances
5. Move the position of the pallet to the next position and repeat steps 1 - 4

The steps and angle change process is shown below:

<img width="2048" height="579" alt="image" src="https://github.com/user-attachments/assets/f0c46eed-2987-46f5-90d5-a0d1f6b5d2ef" />

<img width="1866" height="970" alt="image" src="https://github.com/user-attachments/assets/dc443574-d536-47d2-b445-8e0c95f71d5a" />

<h2>Image Labelling</h2>

In computer vision, labelling is an essential task in anchoring between raw visual data
and meaningful understanding. Raw images that were captured in the previous section only tell
so much about the features within it. To train the model, we need the images to have
corresponding data to show the position of the pallet on the images. Hence, we need to label the
data to its corresponding output. This creates supervised learning data for the model to train on.

For labelling, my team used an open-source tool called LabelImg annotation tool to
identify the pallet in the images. The way it works is as simple as annotating bounding boxes
around the object of interest, in our case the pallet, within the images and assigning its
corresponding label. The figure below shows a sample process of labelling a pallet on the image.

<img width="2077" height="1131" alt="image" src="https://github.com/user-attachments/assets/348ab5a4-3ce5-4b61-9460-d014bd0c2c22" />

As seen from the figure above, there may be some obscurants in the way of the pallet. In
our image collection, we identified three different scenarios; when the pallet is fully visible,
when the pallet is partly visible on one side, and when the pallet is partly visible on both sides.
For the first two cases, we will only annotate the visible pallet. Whereas for the last case, we
included the obscurant in the annotation. This is done since including as much of the pallet on
the annotation as possible would result in a higher confidence in identification, compared to only
including one visible side of the pallet. Additionally, we included slightly blurred images that
were taken. As mentioned before, the model will be used in a real-time camera feed. This is done
to increase confidence in identifying the pallet during motion. As a result, 469 images were
labelled manually to create this supervised learning dataset.

<h2>Solution Assessment</h2>

One benefit to using YOLO to train and test the model is that it provides several graphs
that represent how the model improves. The following graphs show how the mean average
precision (mAP), recall, precision and cost function loss vary with the epoch count.

<img width="1308" height="637" alt="image" src="https://github.com/user-attachments/assets/a380b7f2-dbf5-4ad0-922f-63ef6eb3dc43" />

As expected, most of these metrics significantly improved in the first few iterations,
before leveling out and improving at a slower rate. Based on these graphs, the best version was
found to occur at epoch 74 so training was ended then. This cutoff prevents overfitting, as well as
avoids diminishing results from unnecessarily long training. YOLO also provided useful graphs
for determining the ideal confidence level.

<img width="687" height="640" alt="image" src="https://github.com/user-attachments/assets/ae707ef0-4ecf-4491-bb44-7c8ebbc34aed" /> <img width="687" height="644" alt="image" src="https://github.com/user-attachments/assets/4dd45716-96bf-49ac-80df-9f05690498c0" />

The precision is the model’s ability to make a correct positive prediction. This is defined
by the number of true positives divided by the total number of positives (true and false). As the
confidence score increases, the precision understandably increases as well. Recall represents how
many of the total positive instances the model can predict, defined as the number of positive
predictions divided by the number of positive instances. As the confidence score increases, the
recall decreases due to the model not being able to make as many confident predictions.
Precision and recall are both metrics that should ideally be as high as possible. Fortunately, they
can be averaged and shown together using the F1 curve.

<img width="978" height="643" alt="image" src="https://github.com/user-attachments/assets/6017f2de-6e01-4239-b205-4e02d4067c17" />

The F1 score is the harmonic mean of the precision and recall scores, and it represents the
reliability of the model at every confidence level. For this model, the F1 score is highest at
79.9% confidence.

In the resultant inference video (Validation Video.mov is just the unlabelled sample), we observed 
that the confidence scores were very high when there was an unobstructed view of the pallet, with 
scores as high as 0.95. As the pallet moved into an obstructed view, the confidence scores decreased 
to a minimum of 0.82, which is expected but showcases the potential robustness of the model to 
accurately identify the features of the pallet in unideal conditions. The pallet was also able to 
be classified fairly quickly, with a local NVIDIA RTX 3070Ti Laptop GPU detections occurring 
within 220ms. This speed may be sufficient for production parts that move fairly slowly or have 
large inertia but may be ineffective for very rapid production cycles. For such scenarios, a more 
capable GPU (preferably an enterprise GPU such as the NVIDIA A100) may be required for faster 
image processing and I/O operations with memory.

As stated above, feel free to perform local inference on the supplied sample video "Validation Video.mov"
and watch the inference results yourself!

Thank you for your time!
