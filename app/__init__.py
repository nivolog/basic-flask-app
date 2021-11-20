from flask import Flask
from app.AStar import Solver, Map
from app.tools import euclideanDistance, storePath
from app.config import Config
from redis import Redis

app = Flask(__name__)
app.config.from_object(Config)
app.db = Redis(**app.config['REDIS_KWARGS'])
app.db.flushdb()
grid = Map()
grid.ReadFromPNG('./app/static/images/map1.png')
solver = Solver(app.config['PLANNER_TYPE'], grid, euclideanDistance)

from app import routes
