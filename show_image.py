import tkinter as tk
import datetime
from PIL import ImageTk, Image

import sys
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

def launch(result, image, addr):

  window = tk.Tk()
  window.title("Results")
  window.geometry("800x1000")

  def quit():
    print("Close")
    window.destroy()
    exit()
  now = datetime.datetime.now()
  image.thumbnail((750,750))

  label_image = ImageTk.PhotoImage(image)

  tk.Label(image=label_image).pack()
  run_name = addr + ": MobileNetV3 @ " + now.strftime("%Y-%m-%d %H:%M:%S") + " (" + str(round(result["time"], 2)) + "s)"
  tk.Label(text=run_name).pack()

  for x in result["pds"]:
    pds_label = x["label"] + " " + str(round(x["probability"] * 100)) + "%"
    tk.Label(text=pds_label).pack()

  tk.Button(window, text="Close Window", command=quit).pack()
  
  tk.mainloop()