import enum


class ApiConsts(object):

    HOST = 'http://0.0.0.0:8091'
    GET_ALL_BEARS = '/bear'
    GET_BEAR = '/bear/{id}'
    CREATE_NEW_BEAR = '/bear'
    DELETE_BEAR = '/bear/{id}'
    DELETE_ALL_BEARS = '/bear'
    UPDATE_BEAR = '/bear/{id}'


class ResultMsgs(object):

    EMPTY = 'EMPTY'
    INTERNAL_SERVER_ERROR = '500 Internal Server Error'
    OK = 'OK'


class BearType(enum.Enum):

    POLAR = 'POLAR'
    BROWN = 'BROWN'
    BLACK = 'BLACK'
    GUMMY = 'GUMMY'
