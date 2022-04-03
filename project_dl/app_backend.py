import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from skimage.transform import resize

model = load_model("model.h5")

def reco_funk():
    reco_photo = input()
    reco_photo = str(reco_photo + ".jpg")
    my_image = plt.imread(reco_photo)
    my_image_resized = resize(my_image, (384, 512,3))
    img = plt.imshow(my_image_resized)
    probabilities = model.predict(np.array( [my_image_resized,] ))

    number_to_class = ['cardboard', 'glass', 'metal', 'paper', 'plastic']
    index = np.argsort(probabilities[0,:])
    print("Most likely class:", number_to_class[index[4]])
    print("Second most likely class:", number_to_class[index[3]])
    print("Third most likely class:", number_to_class[index[2]])
