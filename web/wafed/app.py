from flask import Flask, render_template, request, redirect, make_response
import base64, glob, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@app.route("/")
@app.route("/index.html")
def index_view():
    return render_template("index.html")

@app.route("/changeFeed/<feed>")
def switch_view(feed):
    
    resp = make_response(redirect("/trade"))
    resp.set_cookie("price_feed", base64.b64encode((feed).encode()))
    
    return resp

@app.route("/trade")
def read_view():

    raw_path = "./PriceFeeds/DAI"

    if request.cookies.get("price_feed"):

        raw_path = "./PriceFeeds/" + base64.b64decode(request.cookies.get("price_feed")).decode()
    
    blocked = ["/etc/passwd", "/flag.txt"]
        
    if raw_path in blocked:
        return "<h1>you just got WAFFED</h1>"
    try:
        print(raw_path)
        path = glob.glob(raw_path)[0]
    except:
        return "<h1>WOOPS</h1>"
    data = open(path, "r").read()


    data = data.split(",")

    if is_number(data[0]):
        data = [int(x) for x in data]

    return render_template("chart.html", array=data)


if __name__ == "__main__":
    app.run(debug=True)