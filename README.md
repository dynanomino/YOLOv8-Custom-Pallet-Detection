Hello, welcome to the YOLOv8 Custom Pallet Detection model repo!

This repo contains all code necessary for custom pallet model training and inference. Please note that training was done on the Google Colab platform, 
and thus the model training python code located at "Training Files\dataset\pallete_model.py" uses the file path for recognised by Google Colab.

If wishing to perform local model training, please adjust the file path in pallete_model.py as mentioned above. A helpful comment is also written
in the script.

Feel free to run inference on the sample "Validation Video.mov" video using the Pallete_Video_Run.py script! Here's a screenshot of what inference
looks like after processing:

<img width="1879" height="1246" alt="image" src="https://github.com/user-attachments/assets/5fc40525-c971-49ed-b192-9acb11f20839" />

<h2>**Data Acquisition**</h2>

Training the model to achieve the goal of identifying the pallet on the conveyor would
require supervised datasets. The first step was to use a webcam attached to a tripod
for our setup. This is done to ensure the stability and consistency of the images. The image
collection occurs at four different distances as shown in the figure below. These distances are
categorized as Near Near range, Near Far range, Far Near range, and Far Far range.

<img width="1912" height="952" alt="image" src="https://github.com/user-attachments/assets/c3c2cc44-7ae0-41b7-b073-c2ae59e3bd00" />

The steps for taking the images are listed below:
1. Place the pallet on the conveyor in one position
2. Take pictures of the pallet on the conveyor, varying the angle at which the image is taken
3. Split these images such that 80% of images are used for training, and 20% are used for
testing
4. Repeat steps 1 - 3 for all distances
5. Move the position of the pallet to the next position and repeat steps 1 - 4

The steps and angle change process is shown below:

<img width="2048" height="579" alt="image" src="https://github.com/user-attachments/assets/f0c46eed-2987-46f5-90d5-a0d1f6b5d2ef" />

<img width="1866" height="970" alt="image" src="https://github.com/user-attachments/assets/dc443574-d536-47d2-b445-8e0c95f71d5a" />

**Image Labelling**

