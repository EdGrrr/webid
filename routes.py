from flask import Flask, request, render_template, redirect, url_for, make_response
import re
import pdb
import code
import base64
import json
from util import imagedb
from PIL import Image

class DataIndex(object):
    '''Stores a list and the position in it'''
    def __init__(self, newlist=None, missing=-1):
        if not newlist:
            self.data = []
        self.current_index = 0
        self.missing = missing

    def current(self):
        return self.data[self.current_index]
        
    def next(self):
        try:
            self.current_index += 1
            return self.data[self.current_index]
        except:
            return self.missing

    def replace(self, newlist):
        self.data = newlist
        self.current_index = 0

    def visiting(self, visit_number):
        self.current_index = self.data.index(int(visit_number))


class ExpInfo(object):
    '''Stores info about an experiment'''
    def __init__(self, folder, etype, composites=None):
        self.folder = folder
        self.etype = etype
        if composites:
            self.composites = composites
        else:
            self.composites = []

        if self.etype == 'mask':
            self.image_db = imagedb.ImageDatabase(app.root_path+'/static/'+self.folder+'images.db')
            self.image_list = DataIndex([a[1] for a in self.image_db.dump()], 'None')
            self.item_list = DataIndex(missing=-1)
        else:
            raise NotImplementedError('Object detector not yet implmented')
            # tasic_cfg[exp]['track_db'] = TrackDatabase(app.root_path+'/static/'+tasic_cfg[exp]['folder']+'tracks.db')
            # tasic_cfg[exp]['image_db'] = GranuleDatabase(app.root_path+'/static/'+tasic_cfg[exp]['folder']+'granules.db')
            # tasic_cfg[exp]['image_list'] = DataIndex([a[1] for a in tasic_cfg[exp]['gran_db'].dump()], 'None')
            # tasic_cfg[exp]['tr_list'] = DataIndex(missing=-1)


class Expts(object):
    '''Stores information about all experiments'''
    def __init__(self):
        self.expts = {}

    def add_expt(self, name, expt):
        self.expts[name] = expt

    def get_info(self):
        return [[exp, self.expts[exp].etype, *self.expts[exp].image_db.info()] for exp in self.expts.keys()]


app = Flask(__name__)

tasic_cfg = Expts()
tasic_cfg.add_expt('contrails',
                   ExpInfo(
                       folder='contrail_masks/',
                       etype='mask'))
tasic_cfg.add_expt('contrails_goes',
                   ExpInfo(folder='contrail_mask_train/',
                           composites=['CON'],
                           etype='mask'))


@app.route('/submit_mask/<exp>/<image_name>', methods=['POST'])
def submit_mask(exp, image_name):
    '''Save the mask to the server. Done without updating the database as a temporary thing'''
    if request.method == 'POST':
        data = request.form['img64']
        image_data = base64.b64decode(re.sub('^data:image/.+;base64,', '', data))
        mask_name = imagedb.get_maskname('static/'+tasic_cfg.expts[exp].folder+'/'+image_name)
        #Todo here - apply a threshold to the mask
        print(mask_name)
        with open(mask_name, 'wb') as f:
            f.write(image_data)
        return redirect(url_for('index'), code=303)
    else:
        print('Requires POST')


@app.route('/exp/<exp>/image_complete/<image_name>', methods=['POST'])
def image_complete(image_name=None, exp=None):
    '''Store the results from the image in the database'''
    image_data = json.loads(request.form['image_data'])
    try:
        pmask = imagedb.mask_percentage('static/'+tasic_cfg.expts[exp].folder+'/'+image_name)
    except:
        pmask = imagedb.mask_percentage('static/'+tasic_cfg.expts[exp].folder+'/'+image_name, fix=True)
    image_update = {
        'checked': image_data['checked'],
        'notes': image_data['notes'],
        'percentage_mask': pmask
    }
    print(image_name)
    tasic_cfg.expts[exp].image_db.update(image_name,
                                         image_update)
    new_data = tasic_cfg.expts[exp].image_db.check(image_name)
    print('Image: {} Tracks: {} Notes: {}'.format(
        image_name, new_data['percentage_mask'], new_data['notes']))
    return redirect(url_for('index'), code=303)


@app.route('/exp/<exp>/image/<res>/<image_name>')
def image(exp, image_name=None, res='hr'):
    '''Display an image'''
    if (not image_name) or (image_name == 'None'):
        return redirect(url_for('exp_info', exp=exp))
    image_notes = tasic_cfg.expts[exp].image_db.check(image_name)['notes']

    if res == 'hr':
        img_rgb = '{folder}{image_name}'.format(
            folder=tasic_cfg.expts[exp].folder,
            image_name=image_name)
        with Image.open('static/'+img_rgb) as img:
            width, height = img.size[0], img.size[1]
        scale = 1 # Image scaling, not used here
        
        return render_template(
            'image.html',
            img_rgb=img_rgb,
            width=width, height=height,
            exp=exp,
            image_name=image_name,
            mask_name=imagedb.get_maskname(img_rgb),
            image_notes=image_notes, res=res,
            composites=[imagedb.get_compositename(img_rgb, comp) for comp in tasic_cfg.expts[exp].composites],
            next_image=tasic_cfg.expts[exp].image_list.next())

@app.route('/')
@app.route('/index')
def index():
    '''A starting page with list of all the experiments'''
    cfinfo = tasic_cfg.get_info()
    return render_template('index.html', data=cfinfo)

@app.route('/exp/<exp>')
def exp_info(exp):
    '''Provide a single page with links to all the granules
    and track statistics for each'''
    print(exp)
    granules = tasic_cfg.expts[exp].image_db.dump()
    tasic_cfg.expts[exp].image_list.replace([a[1] for a in granules])
    return render_template('exp.html', exp=exp, data=granules)

@app.route('/exp/<exp>-unchecked')
def unchkexp_info(exp):
    '''Provide a single page with links to all the granules
    and track statistics for each'''
    print(exp)
    granules = tasic_cfg.expts[exp].image_db.dump()
    granules = [g for g in granules if g[2] == 0]
    tasic_cfg.expts[exp].image_list.replace([a[1] for a in granules])
    return render_template('exp.html', exp=exp, data=granules)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
