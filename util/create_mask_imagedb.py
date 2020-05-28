from imagedb import ImageDatabase, get_maskname, mask_percentage, mask_create_blank
import sys
from PIL import Image
import os.path

images = sys.argv[1:]

imgdb = ImageDatabase('images.db')

for img in images:
    print(f'Adding {img}')
    #Check for existing mask
    maskname = get_maskname(img)
    if os.path.exists(maskname):
        mask_percent = mask_percentage(img)
        print(mask_percent)
    else:
        mask_create_blank(img)
        mask_percent = 0
    imgdb.update(img, {'percentage_mask': mask_percent})

print('Database creation complete')
print('''
Images:         {}
Checked:        {}
Total overlays: {}
Total tracks:   {}
Percent masks:  {}'''.format(*imgdb.info()))
