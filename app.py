from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/shares")
def shares():
    return "Shares page"

@app.route("/profile")
def profile():
    return {"id":1, "name": "Serhat", "age":22, "following":15, "followers":50, "followersList":["Yagiz","Kaan", "Melih", "Bartu"]}

if __name__ == "__main__":
    app.run(debug=True)