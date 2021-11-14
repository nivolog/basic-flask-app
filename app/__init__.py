from flask import Flask
from app.AStar import Solver, Map
from app.tools import EuclideanDistance

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

grid = Map()
grid.ReadFromPNG('./app/static/images/map1.png')
solver = Solver('astar', grid, EuclideanDistance)

from app import routes