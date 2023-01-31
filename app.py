from flask import render_template
from flask import Flask
from api_teplica import api

# main Flask app
app = Flask(__name__)


@app.route('/')  # route in the / address
def main():
    # TODO: watch gb course and create structure of the app
    tepl_api = api.TeplicaApi("")
    print(tepl_api.patch_watering(1, 1))


if __name__ == '__main__':
    app.run()
