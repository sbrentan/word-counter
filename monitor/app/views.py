from app import app
from flask import render_template
from flask import send_file
from multiprocessing import Process
import glob
import os

import sys
sys.path.insert(1, '/master')
import monitor as monitor


@app.route('/')
def home():
   return "hello world!"

@app.route('/top_words')
def template():

   f = open("/save/accept_mode.txt", "r")
   accept_mode = f.readline().strip()
   f.close()
   os.environ['ACCEPT_MODE'] = accept_mode
   print("accept_mode is " + accept_mode)
   if(accept_mode == "active"):
      monitor.send_command("send_data")
      p = Process(target=monitor.receive)
      p.start()
      p.join()

   sc = monitor.read_counters()
   occ = monitor.read_occurrences()
   return render_template('top_words.html', counter=sc, occurrences=occ)


@app.route('/download/<path:filename>')
def download(filename):
   monitor.send_command("send_file " + filename)
   p = Process(target=monitor.receive_document, args=(filename,))
   p.start()
   p.join()

   docs_folder = "/uploads/"
   file_found = ""
   files = glob.glob(docs_folder + '*')
   for f in files:
      doc = os.path.splitext(f)[0]
      if(docs_folder+filename == doc):
         file_found = f
         break

   if(file_found):
      print(file_found)
      return send_file(file_found, as_attachment=True, attachment_filename=file_found.split("_")[-1])
   else:
      return "not found"



@app.route('/accept_mode/active')
def change_mode():
   p = Process(target=monitor.update_accept_mode, args=("active",))
   p.start()
   os.environ['ACCEPT_MODE'] = "active"
   return "accept_mode changed to active"


@app.route('/accept_mode/passive')
def change_mode2():
   p = Process(target=monitor.update_accept_mode, args=("passive",))
   p.start()
   os.environ['ACCEPT_MODE'] = "passive"
   return "accept_mode changed to passive"


@app.route('/generate/on')
def generate_on():
   monitor.send_command("generate on")
   return "Generate is now on"

@app.route('/generate/off')
def generate_off():
   monitor.send_command("generate off")
   return "Generate is now off"



@app.route("/command/reset")
def reset():

   f = open("/save/nodes.txt", "w")
   f.close()
   f = open("/save/command.txt", "w")
   f.write("0 none")
   f.close()
   f = open("/save/counters.txt", "w")
   f.close()
   f = open("/save/occurrences.txt", "w")
   f.close()

   return "Monitor reset"

p = Process(target=monitor.main, args=(os.environ['ACCEPT_MODE'],))
p.start()