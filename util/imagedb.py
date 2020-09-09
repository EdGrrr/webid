import sqlite3
from datetime import datetime, timedelta
import numpy as np
from PIL import Image

def get_maskname(image_name):
    fname_parts = image_name.split('.')
    if len(fname_parts) == 2:
        return '.'.join([fname_parts[:-1]]+['mask']+[fname_parts[-1]])
    else:
        return '.'.join(fname_parts[:-1]+['mask']+[fname_parts[-1]])

def mask_data_validator(data):
    totals = (data>0).sum(axis=(0, 1))
    if totals[0]==totals[3] and totals[1]==0 and totals[2]==0:
        return True
    else:
        return False
    
def mask_validator(image_name):
    with Image.open(get_maskname(image_name)) as img:
        data = np.array(img)
        return mask_data_validator(data)
    
def mask_percentage(image_name):
    with Image.open(get_maskname(image_name)) as img:
        data = np.array(img)
        if mask_data_validator(data):
            return (100*(data[:, :, 0]>1).sum())/float(data.shape[0]*data.shape[1])
        else:
            raise ValueError('Mask is not valid (either red or black transparent)')

def mask_data_fix(image_name):
    '''If the alpha and red channels don't align, fix the alpha channels to match the red channel'''
    with Image.open(get_maskname(image_name)) as img:
        data = np.array(img)
    # Fix the alpha channel
    data[:, :, -1] = data[:, :, 0]
    # Zero out other channels
    data[:, :, [1, 2]] = 0
    imgmask = Image.fromarray(data)
    imgmask.save(get_maskname(image_name))

def mask_create_blank(image_name):
    with Image.open(image_name) as img:
        maskdata = np.zeros((img.size[1], img.size[0], 4)).astype('uint8')
    imgmask = Image.fromarray(maskdata)
    imgmask.save(get_maskname(image_name))
        
class ImageDatabase:
    def __init__(self, databasefile):
        # Connects to a new database if none existing
        self._dbase = sqlite3.connect(databasefile, check_same_thread=False)
        self._cursor = self._dbase.cursor()
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS
        images(
            id INT PRIMARY KEY,
            image_name TEXT,
            checked BOOL,
            number_overlay INT,
            number_tracks INT,
            percentage_mask INT,
            notes TEXT)''')
        # Schema
        # image_name - duh
        # checked - has image been assesed
        # number_overlay - number of overlay points (e.g. ships, aircraft)
        # number_tracks - how many tracks have been identified (track type)
        # percentage_mask - how much data is masked (mask type)
        # notes - any notes about the image

    def check(self, image_name):
        self._cursor.execute('''SELECT checked, number_overlay, number_tracks, percentage_mask, notes, id
        FROM images WHERE image_name=?''', (image_name,))
        outdata = list(self._cursor)
        if len(outdata) == 0:
            raise ValueError('Image does not exist')
        retdata = {'checked': outdata[0][0],
                   'number_overlay': outdata[0][1],
                   'number_tracks': outdata[0][2],
                   'percentage_mask': outdata[0][3]/100,
                   'notes': outdata[0][5]}
        return retdata

    def update(self, image_name, info):
        try:
            _ = self.check(image_name)
            for name in info.keys():
                # print(name, info[name], type(info[name]))
                self._cursor.execute("UPDATE images SET {} = ? WHERE image_name= ?".format(name),
                                     (info[name], image_name))
        except ValueError:
            self._cursor.execute("""INSERT INTO images(
            image_name, checked, number_overlay, number_tracks, percentage_mask, notes)
            VALUES (?,?,?,?,?,?)""",
                                 [image_name,
                                  info.get('checked', False),
                                  info.get('number_overlay', -1),
                                  info.get('number_tracks', -1),
                                  100*info.get('percentage_mask', -1),
                                  info.get('notes', '')])
        self._dbase.commit()

    def dump(self):
        self._cursor.execute("SELECT * FROM images")
        images = self._cursor.fetchall()
        images.sort(key=lambda x: x[1])
        return images

    def list_imagess(self):
        self._cursor.execute("SELECT image_name FROM images")
        return [g[0] for g in self._cursor]

    def info(self):
        self._cursor.execute("SELECT * FROM images")
        info_array = np.array(self._cursor.fetchall())
        return [
            len(info_array),
            info_array[:, 2].sum(),
            info_array[:, 3][info_array[:, 3]>0].sum(),
            info_array[:, 4][info_array[:, 4]>0].sum(),
            info_array[:, 5][info_array[:, 5]>0].sum()/(100*len(info_array))]
