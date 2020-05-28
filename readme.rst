************************************
A web-based image feature identifier
************************************

The aim of this project is to facilitate the identification of features in images. It was originally designed for use with images from the MODIS instrument, but should work with any set of images.

There are two method for marking out features:

- Object based, where a set of points marking out the feature are recorded by the database. This is based around a simplified version of the identifier used in Gryspeerdt et al. (2019).
- Mask based, where a mask of features is saved and the features are identified with simple drawing tools. Based on the identifier used for contrails in upcoming work.

Thanks to Charles Harvey and Michael Richardson for their contributions.


General usage
#############

Create a conda environment using the environment.yml file. Alternatively, make sure you have the main requirements installed:
- flask
- numpy
- pillow (PIL)

Create some experiments (see below), then start the server (on localhost) by running 'make' in the project root directory. The webpage should then be at 'localhost:8000/index'.

For each experiment on the index page, there are two links. Clicking on the number of images will take you to a list of all available images. Clicking on the number in the 'checked' column will take you to a list of only the unchecked images. When going through the list of images, this should be the list of images used by the server.


Mask identifier
###############

Setup
*****

Once you have created a set of images, place them in a folder in the 'static' directory. If using an mask-based identifier, run 'util/create_mask_imagedb.py' from within the directory containing the images, where the following arguments are the names of the files to add to the database. This will create blank masks for images that don't already have them. A single folder of images is known as an 'experiment'.

Note that this script can be run in the future to add new images to a database without overwriting the results for previous images. You can try this in the example folder 'contrail_masks'. The current images.db does not include all of the images yet. These lines will add the new image.

``cd static/contrail_masks``
``python ../../util/create_mask_imagedb.py *.v1.png``

Add the experiment details to tasic_cfg in 'routes.py'. Note that you can have many different experiments in a single identifier setup. All that is required here is the location of the experiment folder and the name of the experiment.

Workflow (mask-mode)
********************

Enter the experiment (using either of the links in the index) and then click on a file. Use the mouse to draw out your mask, along with the line drawing function and erase function as necessary. The 'undo' and 'redo' function are unreliable, so use the 'save mask' button to save your progress.

When you have finished, use the 'Image Complete' button to record your mask information in the database. Note that you can add a note with the image and also mark it as unchecked (useful if you want to move on but may need to come back to this image later).

The 'Next Image' link takes you to the next image in the experiment, or back to the experiment info page if you have finished all the images.

Keyboard shortcuts (mask mode)
******************************

Within the identifier screen for each image, there are some keyboard shortcuts to make life easier

- d - switch to free-draw mode (default)
- Numbers 1-5 - change the stroke width
- t - toggle the visibility of the mask
- e - switch to erase mode (draw a rectangle and the contents are erased)
- l - switch to line drawing mode (click and hold)
- p - polygon drawing mode (not yet implemented)


Object identifier
*****************

Not yet copied over from old code...


