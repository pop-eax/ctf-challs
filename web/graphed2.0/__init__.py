from app import app
from flask import render_template
from graph import schema
from flask_graphql import GraphQLView

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

@app.route("/")
def index_view():
    return render_template("index.html")

@app.route("/cool")
def cool_view():
    return render_template("cool.html")

if __name__ == "__main__":
    app.run(debug=True)