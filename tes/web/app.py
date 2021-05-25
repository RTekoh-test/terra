#!/usr/local/bin/python3

# import the Flask class from the flask module
import flask
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import subprocess

# create the application object
app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods = ['POST', 'GET'])
def home():
    def getjson(form_data_org):
        form_env = os.environ.copy()
        form_env['ORG'] = form_data_org
        return subprocess.Popen(
            ['python ../terratattle.py --output=json'],
            shell=True,
            stdout=subprocess.PIPE,
            env=form_env
        )

    if request.method == "GET":
      return render_template('index.html')
    if request.method == 'POST':
      form_data_org = request.form['org'].lower().strip()
      response = getjson(form_data_org).communicate()

    return render_template('results.html', response = json.loads(response[0]))

@app.route('/api', methods = ['GET'])
def api():
    def data(req_org, req_repo):
        form_env = os.environ.copy()
        form_env['ORG'] = req_org.lower()

        py_cmd = 'python ../terratattle.py --output=json'

        if req_repo != None:
            py_cmd += ' --repo'
            form_env['REPONAME'] = req_repo.lower()

        return subprocess.Popen(
            [py_cmd],
            shell = True,
            stdout = subprocess.PIPE,
            env = form_env
        )

    req_org = request.args.get('org')
    if req_org == None:
      return flask.Response(json.dumps({'message': 'Please provide an org argument.'}), status = 422, mimetype = 'application/json')

    req_repo = request.args.get('repo')

    response = data(req_org, req_repo).communicate()

    return flask.Response(response[0], mimetype = 'application/json')

# start the server with the 'run()' method
if __name__ == '__main__':
#  app.run(debug=True)
  app.run(threaded=True, debug=True)
#  app.jinja_env.auto_reload = True
#  app.config['TEMPLATES_AUTO_RELOAD'] = True
