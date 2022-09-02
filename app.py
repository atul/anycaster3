from flask import Flask, request, jsonify
from subprocess import check_output, getoutput
import logging
import re
import os

app = Flask(__name__)
app.config["DEBUG"]=True
logging.basicConfig(filename='error.log',level=logging.DEBUG)
hostname=check_output(['hostname']).decode('utf-8').strip()
# set lo address to service address
getoutput('ip addr add %s dev lo' %  os.environ.get('FLASK_RUN_HOST'))
# check address 221.*.*.* on physical port
op=check_output(['ip', 'addr', 'show']).decode('utf-8').strip().split('\n')

patt='221.\d+.\d+.\d+'
for ele in op:
    m=re.search(patt, ele)
    if m:
        srvip=m.group()
app.logger.info("Server ip: %s " % srvip)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'remote_ip': request.environ['REMOTE_ADDR'],
    'remote_port': request.environ['REMOTE_PORT'], 'hostname': hostname,
    'srvip': srvip}), 200

@app.route('/api/v1/srvinfo/', methods=['GET'])
def cleient_info():
    return jsonify({'ip': request.environ['REMOTE_ADDR'], 'rport': request.environ['REMOTE_PORT']}), 200

if __name__ == '__main__':
    app.run(debug=True, host=srvip)
