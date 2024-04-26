from flask import Flask, render_template

app = Flask(__name__, static_folder='fitnesstracker/static', template_folder='fitnesstracker/templates')

@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
