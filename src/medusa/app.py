from flask import Flask, render_template
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weather import get_Weather, session

app = Flask(__name__)

@app.route('/')
def index():
    try:
        weather_data = get_Weather(session)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        weather_data = None

    return render_template('base.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
