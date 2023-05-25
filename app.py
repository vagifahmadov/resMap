from setting.config import apps
from services.services import index, search, listing

apps.register_blueprint(index)
apps.register_blueprint(search)
apps.register_blueprint(listing)

if __name__ == '__main__':
    apps.run(debug=True, port=1985, host='localhost')


