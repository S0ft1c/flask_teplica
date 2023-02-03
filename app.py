from flask import render_template
from flask import Flask
from database import db_sqlite as db
from flask import request
from flask import redirect
from api_teplica import api

# main Flask app
app = Flask(__name__)


@app.route('/drop')  # if we want drop all tables, just go on this page
def drop_tables():
    database = db.DataBase(True)
    return redirect("/")


@app.route('/')  # route in the / address
def index():
    database = db.DataBase(False)
    user_params = database.get_user_params()  # get all user_params
    context = {
        "user_temperature": user_params[1],
        "user_humanity": user_params[2],
        "user_hb_persent": user_params[3],
        "fork_state": database.get_fork()[0],  # get fork state
        "humanity_state": database.get_humanity()[0]  # get humanity state
    }
    for i in range(1, 7):  # it's for good adding data about hb_devices
        context[f"hb_{i}"] = database.get_hb_device(i)[0]

    return render_template("site/index.html", **context)


@app.route('/user_params_update/', methods=['GET', 'POST'])
def user_params_update():
    database = db.DataBase(False)
    if request.method == "POST":
        response = 1
        t = request.form.get("t")
        h = request.form.get("h")
        hb = request.form.get("hb")
        t = float(t) if t.isdigit() else -1
        h = float(h) if h.isdigit() else -1
        hb = float(hb) if hb.isdigit() else -1
        if -1 not in (t, h, hb):
            database.update_user_params(t, h, hb)
        return redirect("/")
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run()
