import numpy as np
import cv2
import os
from cv2 import dnn

def ColorizeImage(sourceImg, save):
    if(os.path.exists(sourceImg) == False):
        return
    proto_file = 'Model\colorization_deploy_v2.prototxt'
    model_file = 'Model\colorization_release_v2.caffemodel'
    hull_pts = 'Model\pts_in_hull.npy'

    # Reading the model params
    net = dnn.readNetFromCaffe(proto_file, model_file)
    kernel = np.load(hull_pts)

    # Reading and processing the image
    img = cv2.imread(sourceImg)
    imgDimensions = img.shape
    scaled = img.astype("float32") / 255.0
    lab_img = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Add the cluster centers as 1x1 convolutions to the model
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = kernel.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # Resize image
    resized = cv2.resize(lab_img, (224, 224))

    # Split the L channel
    L = cv2.split(resized)[0]

    # Mean substraction
    L -= 50

    # Predicting the ab channels from the input L channel
    net.setInput(dnn.blobFromImage(L))
    ab_channel = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # Resize the predicted ab volume to the same dimensions as the input image
    ab_channel = cv2.resize(ab_channel, (img.shape[1], img.shape[0]))

    # Take the L channel from the image
    L = cv2.split(lab_img)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab_channel), axis=2)

    # Convert image from LAB to BGR
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    # Change image to 0-255 range and convert it from float32 to int
    colorized = (255 * colorized).astype("uint8")

    # Resize the images and show them together
    img = cv2.resize(img, (640, 640))
    colorized = cv2.resize(colorized, (640, 640))

    result = cv2.hconcat([img, colorized])

    if(save == True):
        colorized = cv2.resize(colorized, (imgDimensions[1], imgDimensions[0]))
        colorizedImageName = os.path.basename(sourceImg)
        cv2.imwrite(f"ConvertedImages/Colorized-{colorizedImageName}", colorized)
    else:
        cv2.imshow("Grayscale -> Color", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()