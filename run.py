from src.app import create_app
from src.app.routes import configure_routes

app = create_app()

if __name__ == '__main__':
    configure_routes(app)
    app.run(debug=True)
