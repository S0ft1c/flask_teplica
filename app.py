from flask import render_template
from flask import Flask
from database import db_sqlite as db
from flask import request
from flask import redirect
from api_teplica import api
from help import help

# main Flask app
app = Flask(__name__)


@app.route('/drop')  # if we want drop all tables, just go on this page
def drop_tables():
    database = db.DataBase(True)
    return redirect("/")


@app.route('/')
@app.route('/index/')  # route in the / address
def index():
    database = db.DataBase(False)
    user_params = database.get_user_params()  # get all user_params
    context = {
        "user_temperature": user_params[1],
        "user_humanity": user_params[2],
        "user_hb_persent": user_params[3],
        "fork_state": database.get_fork()[0],  # get fork state
        "fork_can": help.average_temp(),
        "humanity_state": database.get_humanity()[0],  # get humanity state
        "humanity_can": help.average_hum(),
        "hb_1_can": help.average_hb(1),     # not from 0, yes?
        "hb_2_can": help.average_hb(2),
        "hb_3_can": help.average_hb(3),
        "hb_4_can": help.average_hb(4),
        "hb_5_can": help.average_hb(5),
        "hb_6_can": help.average_hb(6),
    }
    for i in range(1, 7):  # it's for good adding data about hb_devices
        context[f"hb_{i}"] = database.get_hb_device(i)[0]
        # context[f"hb_can_{i}"] = help.average_hb(i) looks like its useless...

    return render_template("site/index.html", **context)


# ЗДЕСЬ ВСЕ МЕНЯТЬ НАДО !!!
@app.route('/graphs/')  # route in the / address
def graphs():
    database = db.DataBase(False)
    graphs_params = database.get_user_params()  # get all graphs_params
    context = {
        "temperature": graphs_params[1],
        "humanity": graphs_params[2],
        "hb_persent": graphs_params[3],
        "humanity_state": database.get_humanity()[0]  # get humanity state
    }
    return render_template("site/graphs.html", **context)

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


@app.route('/get_all_data/')
def get_all_data():
    page = request.args.get("page")
    api_sys = api.TeplicaApi("")
    database = db.DataBase(False)
    for i in range(1, 5):
        data = api_sys.get_temp_hum(i)
        database.insert_temp_hum(data["id"], data["temperature"], data["humidity"])
    for i in range(1, 7):
        data = api_sys.get_ground_hum(i)
        database.insert_ground_hum(data["id"], data["humidity"])
    return redirect(f'/{page}/')

@app.route('/get_graphs_data/')
def get_graphs_data():
    page = request.args.get("page")
    api_sys = api.TeplicaApi("")
    database = db.DataBase(False)
    for i in range(1, 5):
        data = api_sys.get_temp_hum(i)
        database.insert_temp_hum(data["id"], data["temperature"], data["humidity"])
    for i in range(1, 7):
        data = api_sys.get_ground_hum(i)
        database.insert_ground_hum(data["id"], data["humidity"])
    return redirect(f'/{page}/')

@app.route('/fork_open/')
def fork_open():
    state = request.args.get("state")  # get an arg from address
    api_sys = api.TeplicaApi("")
    database = db.DataBase(False)

    can = help.average_temp()

    if can:
        state = 1 if state == "on" else 0  # what we want to do with fork
        response = api_sys.patch_fork(status=state)  # patch fork via api
        print(response)
        database.update_fork(bool(state))
    return redirect("/")


@app.route('/humanity_open/')
def humanity_open():
    state = request.args.get("state")
    api_sys = api.TeplicaApi("")
    database = db.DataBase(False)

    can = help.average_hum()

    if can:
        state = 1 if state == "on" else 0  # what we want to do with hum
        response = api_sys.patch_total_hum(state)
        print(response)
        database.update_humanity(bool(state))
    return redirect("/")


@app.route('/hb_open/')
def hb_open():
    num = request.args.get("num")
    state = request.args.get("state")
    api_sys = api.TeplicaApi("")
    database = db.DataBase(False)
    num = int(num)

    can = help.average_hb(num)
    if can:
        state = 1 if state == "on" else 0
        response = api_sys.patch_watering(num=num, status=state)
        print(response)
        database.update_hb_device(num, state)
    return redirect("/")


if __name__ == '__main__':
    app.run()
