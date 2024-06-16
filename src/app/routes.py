from flask import render_template
import pandas as pd
from . import create_app

app = create_app()

def configure_routes(app):
    @app.route('/')
    def home():
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [24, 27, 22],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        df = pd.DataFrame(data)
        html_table = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', table=html_table)