import config
from app import api


def run():
    api.run(host=config.ADDR, port=config.PORT, debug=False)


if __name__ == '__main__':
    run()
