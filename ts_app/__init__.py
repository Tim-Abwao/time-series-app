from ts_app.flask_app import server
import os
import subprocess


app = server


def run_app():
    """Launch the app using gunicorn's command line script."""
    try:
        print('Launching Time Series App using gunicorn...')
        subprocess.run(['gunicorn', '-w', '3', 'ts_app:app'])
    except KeyboardInterrupt:
        print('Time Series App stopped!')
        
        # Remove the cached sample file 
        if os.path.exists('sample.pkl'):
            os.remove('sample.pkl')
