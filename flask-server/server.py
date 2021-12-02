from flask import Flask, redirect, url_for, render_template, request


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


@app.route("/recommendations", methods=['POST'])
def content_recommendations(title):
    return{"members": ["Member1", "Member2", "Member3"]}


if __name__ == "__main__":
    app.run(debug=True)
