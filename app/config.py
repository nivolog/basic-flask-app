class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 1

    REDIS_KWARGS = {
        'host': 'redis',
        'port': 6379,
        'db': 0
    }

    PLANNER_TYPE = 'astar'
