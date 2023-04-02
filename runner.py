import config
from src import app


def run():
    app.run(host=config.ADDR, port=config.PORT, debug=False)


if __name__ == '__main__':
    run()
