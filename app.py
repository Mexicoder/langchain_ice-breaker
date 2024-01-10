from flask import Flask, render_template, request, jsonify

from ice_breaker import ice_break

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    person_info, profile_pic_url = ice_break(name=name)

    return jsonify(
        {
            "summary": person_info.summary,
            "facts": person_info.facts,
            "topics_of_interest": person_info.topics_of_interest,
            "ice_breakers": person_info.ice_breakers,
            "profile_pic_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
