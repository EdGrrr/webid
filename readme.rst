************************************
A web-based image feature identifier
************************************

The aim of this project is to facilitate the identification of features in images. It was originally designed for use with images from the MODIS instrument, but should work with any set of images.

There are two method for marking out features:

- Object based, where a set of points marking out the feature are recorded by the database. This is based around a simplified version of the identifier used in Gryspeerdt et al. (2019).
- Mask based, where a mask of features is saved and the features are identified with simple drawing tools. Based on the identifier used for contrails in upcoming work.

Thanks to Charles Harvey and Michael Richardson for their contributions.


Usage
#####

Create a conda environment using the environment.yml file. Alternatively, make sure you have the main requirements installed:
- flask
- numpy
- pillow (PIL)


Mask-identifier
***************

Once you have created a set of images, place them in a folder in the 'static' directory. If using an mask-based identifier, run 'util/create_mask_imagedb.py' from within the directory containing the images, where the following arguments are the names of the files to add to the database. This will create blank masks for images that don't already have them.

Add the project details to tasic_cfg in 'routes.py'. Note that you can have many different projects in a single identifier setup.

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

Not yet copied over from old code 


