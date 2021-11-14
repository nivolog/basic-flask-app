import json
from flask import render_template, request
from app import app
from app import solver

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Home')


@app.route('/planning.html', methods=['GET', 'POST'])
def planning():
    return render_template('planning.html', title='Planning')


@app.route('/add_point', methods=["POST"])
def add_point():
    data = request.get_json()
    pathFound = solver.plan(100, 100, int(round(data['click']['y'])), int(round(data['click']['x'])))

    path = solver.MakePathRaw()

    result = {
        "Start":
            {"x": 100,
             "y": 100},
        "Goal":
            {"x": int(round(data['click']['x'])),
             "y": int(round(data['click']['y']))},
        "pathFound": pathFound,
        "path": path[0],
        "pathLength": f'{path[1]:.3f}'}

    rsp = json.dumps(result)
    print(rsp)
    # db.set('test', 3)
    print('Success')
    response = app.response_class(
        response=rsp,
        status=200,
        mimetype='application/json'
    )
    return response


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response
