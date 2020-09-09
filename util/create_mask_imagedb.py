from imagedb import ImageDatabase, get_maskname, mask_percentage, mask_create_blank, mask_data_fix
import sys
from PIL import Image
import os.path
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', "--fixmasks", help="fix supplied masks so the alpha channel matches the red channel",
                    action="store_true")
parser.add_argument('file', nargs='+')
args = parser.parse_args()

imgdb = ImageDatabase('images.db')

for img in args.file:
    print(f'Adding {img}')
    #Check for existing mask
    maskname = get_maskname(img)
    if os.path.exists(maskname):
        if args.fixmasks:
            mask_data_fix(img)
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
