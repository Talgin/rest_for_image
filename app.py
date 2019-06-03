from flask import Flask, jsonify, request, render_template, Response, redirect, url_for, flash
from werkzeug.utils import secure_filename
import subprocess
import base64
import uuid


app = Flask(__name__)

liveness = [
  {'description': 'head_liveness', 'value': 0.89, 'test_id': 1212}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        img = request.form['file']
        img = img.split(',')
        # print(img)
        img_data = img[1]
        name = uuid.uuid4().hex
        with open(r'C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\\' + name + '.ppm', "wb") as fh:
            fh.write(base64.b64decode(img_data))
            image_json = {
                "type": "image",
                "id": name
            }
            liveness.append(image_json)
        return jsonify(request.form['userID'], request.form['file'])
        # run_exe()
    return render_template('index.html')


@app.route('/liveness')
def get_liveness():
    return jsonify(liveness)


@app.route('/poster', methods=['POST'])
def poster():
    return jsonify('executed')


# delete if runs' above worked successfully
@app.route('/run')
def run_service():
    command = r'C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\test_live.exe C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\om.ppm'
    subprocess.call(command)
    return jsonify("success")


def convertTuple(tup):
    stre = ''.join(tup)
    return stre


# getting smile value - to call - localhost:5000/run_smile/<img_id> where
# img_id is the name of the image file without extension
@app.route('/run_smile/<img_id>', methods=['GET'])
def run_smile(img_id):
    command = r'C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\smile\test_live.exe C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\\' + img_id + '.ppm'
    #subprocess.call(command)
    p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
    output = p.communicate()
    output = output[0].decode('utf-8')
    output = output.split('\r\n')
    print('this is OUTPUT', output)
    return jsonify(output[1:5])


# getting head rotation value - to call - localhost:5000/run_head/<img_id> where
# img_id is the name of the image file without extension
@app.route('/run_head/<img_id>', methods=['GET'])
def run_head(img_id):
    command = r'C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\head\test_live.exe C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\\' + img_id + '.ppm'
    #subprocess.call(command)
    p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
    output = p.communicate()
    output = output[0].decode('utf-8')
    output = output.split('\r\n')
    print('this is OUTPUT', output)
    return jsonify(output[1:4])

# getting info about eyes - to call - localhost:5000/run_eye/<img_id> where
# img_id is the name of the image file without extension
@app.route('/run_eye/<img_id>', methods=['GET'])
def run_eye(img_id):
    command = r'C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\eye\test_live.exe C:\Users\TengriLab\Desktop\DOCUMENTATION\api_test\test_live_ocv34_estimates\x64\Release\\' + img_id + '.ppm'
    #subprocess.call(command)
    p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
    output = p.communicate()
    output = output[0].decode('utf-8')
    output = output.split('\r\n')
    print('this is OUTPUT', output)
    return jsonify(output[1:3])


@app.route('/liveness', methods=['POST'])
def add_liveness():
    liveness.append(request.get_json())
    return jsonify(liveness)


if __name__ == '__main__':
    app.run(threaded=True)
