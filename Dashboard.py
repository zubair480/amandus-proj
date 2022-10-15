import string

from flask import Flask, render_template, request, redirect, flash, jsonify

import helper
from dashboard.EtihadDb import EtihadDb
from parser.Parser import Parser
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
    parser = Parser()
    result = parser.parse_file("temp_file.CMP")

    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class Etihadly():
    def suggestion(self, partDict):
        pass

    def decorate(self, partDict):
        if "allwrong" in partDict:
            return f"<span class='allwrong'>{partDict['part']}</span>"

        if "possible" in partDict:
            posibilities = "Suggestions: " + str(", ".join(partDict["possible"]))

            return f"<div class='justdiv'><span class='error' " \
                   f"  onClick='alert(\"{posibilities}\")'>{partDict['part']}" \
                   f"<span>" \
                   f"<p class='myTooltip'>{posibilities}</p>" \
                   f"</div>"

        return partDict["part"]


    def build(self, backmatch):
        res = ""
        for line in backmatch:
            for part in line:
                res += self.decorate(part)
            res += "\n"


        return res


@app.route('/show_file', methods=['GET'])
def show_file():
    filename = request.args.get('file', default = None, type = str)
    content = EtihadDb().get_file(filename)
    if content:
        print(content)
        p = Parser()
        res = p.parse_text(content)

        return render_template("index.html",
            header=res.get("header"),
            carrier=res.get("carrier"),
            ULDs=res.get("ULDs"),
            etihadly=Etihadly().build(p.backmatches),
            dbfiles=EtihadDb("db.db").get_file_list())



    return render_template("index.html",
                           header=None,
                           carrier=None,
                           ULDs=None,
                           etihadly=None,
                           dbfiles=EtihadDb("db.db").get_file_list())



@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("file")
        db = EtihadDb()
        for file in files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            print("adding file", filename)
            db.add_file(file.filename, helper.load_file_simple(filename))

    return redirect("show_file")



@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            p = Parser()
            res = p.parse_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            f = open(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            file_contents = f.read()
            f.close()


            return render_template("index.html",
                                   header=res.get("header"),
                                   carrier=res.get("carrier"),
                                   ULDs=res.get("ULDs"),
                                   etihadly=Etihadly().build(p.backmatches),
                                   dbfiles=EtihadDb("db.db").get_file_list())



    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

