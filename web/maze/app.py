from flask import Flask, render_template, request, render_template_string, session, redirect, make_response
import sqlite3
import graphene
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

app = Flask(__name__)
app.secret_key = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coins.db'
db = SQLAlchemy(app)

@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "GET" and session.get('logged_in') != True:
        return render_template("login.html")
    
    elif session.get('logged_in') == True:
        return redirect("/")

    else:
    
        if request.method == "POST" and request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            if  username == "XFT" and password == "iigvj3xMVuSI9GzXhJJWNeI":
                session['logged_in'] = True
                return redirect("/")
            else:
                return redirect("/login")

@app.route("/")
def index_view():
    if session.get('logged_in'):
        return render_template("index.html")
    else :
        return redirect("/login")

@app.route("/trade")
def trade_view():
    if session.get('logged_in'):
        coin = request.args.get("coin")
        conn = sqlite3.connect('coins.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM coin_data where coin_name='{coin}'")
        query = c.fetchall()
        if len(query) > 0:
            return render_template("trade.html", coin=query[0][0], desc=query[0][1])
        else :
            return render_template("trade.html", coin="invalid coin", desc="nothing in here")
    else :
        return redirect("/login")

@app.route("/admin", methods=["GET", "POST"])
def admin_route():
    if request.method == "GET" and session.get('admin') != True:
        return render_template("login.html")
    
    elif session.get('admin') == True and request.method == "GET":
        if request.cookies.get("name"):
            name_input = request.cookies.get("name")
        else:
            name_input = "skid"
        resp = make_response(render_template("admin.html", name=render_template_string(name_input)))
        resp.set_cookie("name", name_input)
        
        return resp

    else:
    
        if request.method == "POST" and request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            if  username == "admin" and password == "p0To3zTQuvFDzjhO9":
                session['admin'] = True
                return redirect("/admin")
            else:
                return redirect("/admin")

@app.route("/robots.txt")
def robots_view():
    return "/sup3r_secr37_@p1"

class Trader(db.Model):
    __tablename__  = 'traders'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    coins = db.relationship('Coin', backref='owned_coins')

    def __repr__(self):
        return '<Trader %r>' % self.username

class Coin(db.Model):
    __tablename__ = 'coins'

    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    password = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('traders.uuid'))

    def __repr__(self):
        return '<Coin %r>' % self.title

class CoinObject(SQLAlchemyObjectType):
    class Meta:
        model = Coin
        interfaces = (graphene.relay.Node, )

class TraderObject(SQLAlchemyObjectType):
    class Meta:
        model = Trader
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_traders = SQLAlchemyConnectionField(TraderObject)


schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/sup3r_secr37_@p1',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)

if __name__ == "__main__":
    app.run(debug=True)