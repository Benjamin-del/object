# Import all Modules
import timm
import torch
import time
import show_image
import threading
import tkinter as tk
import datetime
from PIL import ImageTk, Image
import json
import multiprocessing

# Import extra modules (TIMM)
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

# Import extra modules (PIL)
from PIL import Image

# Import extra modules (Flask)
from flask import Flask, request, render_template
from flask_basicauth import BasicAuth
# Open Files 
label_file = open("model_data/classes.txt", "r")
labels = label_file.read().split("\n")
label_file.close()

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()
# Configure Flask
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = config["username"]
app.config['BASIC_AUTH_PASSWORD'] = config["password"]

basic_auth = BasicAuth(app)



def getLabel(index):
    return labels[index]

def runModel(img):
    model = timm.create_model('tf_mobilenetv3_large_075', checkpoint_path='model_data/mobilenetv3.pth')
    model.eval()

    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)

    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(tensor)

    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    #print(probabilities.shape)

    top5_prob, top5_catid = torch.topk(probabilities, 5)
    results = []

    for i in range(top5_prob.size(0)):
        #print(labels[top5_catid[i]], top5_prob[i].item())
        results.append({"label": getLabel(top5_catid[i]), "probability": top5_prob[i].item()})

    return results
    
@app.route("/upload", methods = ['POST'])
@basic_auth.required
def upload():
    print("Loading...")
    file = request.files['file']

    time_indiv_start = time.time()
    img = Image.open(file).convert('RGB')
    model_data = runModel(img)
        
    time_indiv_end = time.time()
    processThread = multiprocessing.Process(target=show_image.launch, args=({
        "file": file.filename,
        "pds": model_data,
        "time": time_indiv_end-time_indiv_start,
    }, img,request.remote_addr,)) 
    processThread.start()


    return {
        "message":"Your File has been sent to the Server! Return to see the results.",
    }

@app.route("/")
@basic_auth.required
def index():
    return render_template('index.html')

@app.route("/dlg")
@basic_auth.required
def dlg():
    return render_template('dlg.html')

@app.route("/demo")
@basic_auth.required
def demo():
    return render_template('demo.html')

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
