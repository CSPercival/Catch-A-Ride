# from .app.init import create_app
from Components.Visualizer.app.init import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=False)