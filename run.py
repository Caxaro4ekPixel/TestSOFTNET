from app import db, create_app
from config import ProductionConfig
from flask_migrate import Migrate

app = create_app(ProductionConfig)
migrate = Migrate(app, db, compare_type=True)

if __name__ == '__main__':
    app.run()
