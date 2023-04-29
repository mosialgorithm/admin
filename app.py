import os
from flask import Flask, render_template





base_dir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('admin/index.html')




if __name__ == '__main__':
    app.run(debug=True)