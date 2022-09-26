import pandas as pd
import openpyxl
from flask import Flask, redirect, url_for, request, render_template, send_from_directory
import os
import shutil
import dbtjumpstart

input_file_path = "./dbt_jumpstart/config"
output_file_path = "./dbt_jumpstart/output"

# Set flask app name
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'config'

# Default hello world output
@app.route('/')
def hello_world():
    # return "Hello there!"
    return render_template('start.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    shutil.make_archive("delivery\\output", 'zip', r"C:\Code repositories\dbt-jumpstart-docker\output")
    # uploads = os.path.join(r"C:\Code repositories\dbt-jumpstart-docker", "delivery")
    return send_from_directory(".\\delivery", "output.zip")


@app.route('/jumpstart')
def upload_file():
   return render_template('jumpstart.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_uploader():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file.save("./dbt_jumpstart/config/{}".format(file.filename))
        dbtjumpstart.make_models(input_file_path, output_file_path)
        shutil.make_archive("./dbt_jumpstart/delivery/output", 'zip', r"./dbt_jumpstart/output")

        # delete the generated files except the output
        folders_to_clear = ['./dbt_jumpstart/config', './dbt_jumpstart/output']
        for folder in folders_to_clear:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        return send_from_directory("/usr/src/app/dbt_jumpstart/delivery", "output.zip")
    return 'Nothing has happened. Go back.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 9000)