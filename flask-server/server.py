from flask import Flask, redirect, url_for, render_template, request
import recommend
import synopsis


app = Flask(__name__)


@app.route('/PostForm', methods=['POST', 'GET'])
def PostForm():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("usr", usr=user))
    else:
        return redirect(url_for("PostForm"))


@app.route("/usr")
def usr():
    return f"<H1>{usr} sadasd</H1>"

# members Api route


@app.route("/members")
def members():
    return{"members": ["Member1", "Member2", "Member3"]}


@app.route('/title')
def get_recommend_title():
    json2 = request.args.get('title')
    recommender = recommend.content_recommendations(json2)
    return {'name': recommender}


@app.route('/synopsis')
def get_recommend_synopsis():
    json2 = request.args.get('title')
    recommender = synopsis.content_synopsis(json2)
    return {'name': recommender}


if __name__ == "__main__":
    app.run(debug=True)
