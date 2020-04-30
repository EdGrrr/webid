from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_cors import CORS, cross_origin
from werkzeug import FileStorage
import re
import pdb
import code
import base64
from util import imagedb
#pdb.set_trace()

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

def get_info(tasic_cfg):
    return [[a, tasic_cfg[a]['type'], *tasic_cfg[a]['image_db'].info()] for a in tasic_cfg.keys()]

tasic_cfg = {'contrails': {'folder': 'contrail_masks/',
                           'composite': 'CON',
                           'type': 'region'},}

app = Flask(__name__)                                                                                   #app.config['SERVER_NAME'] = 'localhost:8000'
CORS(app)

for exp in tasic_cfg.keys():
    if tasic_cfg[exp]['type'] == 'region':
        tasic_cfg[exp]['image_db'] = imagedb.ImageDatabase(app.root_path+'/static/'+tasic_cfg[exp]['folder']+'images.db')
        tasic_cfg[exp]['image_list'] = DataIndex([a[1] for a in tasic_cfg[exp]['image_db'].dump()], 'None')
        tasic_cfg[exp]['item_list'] = DataIndex(missing=-1)
    else:
        tasic_cfg[exp]['track_db'] = TrackDatabase(app.root_path+'/static/'+tasic_cfg[exp]['folder']+'tracks.db')
        tasic_cfg[exp]['image_db'] = GranuleDatabase(app.root_path+'/static/'+tasic_cfg[exp]['folder']+'granules.db')
        tasic_cfg[exp]['image_list'] = DataIndex([a[1] for a in tasic_cfg[exp]['gran_db'].dump()], 'None')
        tasic_cfg[exp]['tr_list'] = DataIndex(missing=-1)



@app.route('/submit_mask', methods=['POST'])
#@cross_origin()
def submit_mask():
    if request.method == 'POST':
        data = request.form['img64']
        #print(data)
        image_data = base64.b64decode(re.sub('^data:image/.+;base64,', '', data))
        with open('test.png', 'wb') as f:
            f.write(image_data)
        return 
    else:
        print('Requires POST')
        
@app.route('/')
@app.route('/index')
def index():
    cfinfo = get_info(tasic_cfg)
    return render_template('index.html', data=cfinfo)

@app.route('/exp/<exp>')
def exp(exp=exp):
    '''Provide a single page with links to all the granules
    and track statistics for each'''
    print(exp)
    granules = tasic_cfg[exp]['image_db'].dump()
    tasic_cfg[exp]['image_list'].replace([a[1] for a in granules])
    return render_template('exp.html', exp=exp, data=granules)

@app.route('/exp/<exp>-unchecked')
def unchkexp(exp=exp):
    '''Provide a single page with links to all the granules
    and track statistics for each'''
    print(exp)
    granules = tasic_cfg[exp]['image_db'].dump()
    granules = [g for g in granules if g[2] == 0]
    tasic_cfg[exp]['image_list'].replace([a[1] for a in granules])
    return render_template('exp.html', exp=exp, data=granules)

# def test():
#     return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
