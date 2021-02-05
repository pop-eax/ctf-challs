from flask import Flask,request
import hashlib
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def index_view():
    sandbox_dir = int(hashlib.sha256(request.remote_addr.encode('utf-8')).hexdigest(), 16) % 10**8
    if not os.path.isdir(f"sandbox/{sandbox_dir}"):
        os.system(f"mkdir \"sandbox/{sandbox_dir}\"")
        
    cmd = request.args.get("cmd")
    if cmd:
        if len(cmd) <= 5:
            return subprocess.check_output(f"cd 'sandbox/{sandbox_dir}';{cmd}", shell=True)
        else:
            return "input shouldn't exceed length of 5"
    return "arg cmd is missing"


if __name__ == "__main__":
    app.run(debug=True)