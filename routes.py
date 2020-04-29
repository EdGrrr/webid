from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_cors import CORS, cross_origin
from werkzeug import FileStorage
import re
import pdb
import code
import base64
#pdb.set_trace()


app = Flask(__name__)                                                                                   #app.config['SERVER_NAME'] = 'localhost:8000'
CORS(app)

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
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
