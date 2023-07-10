from create_app import create_app
import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

application = create_app(False)

application.route('/')(lambda: 'API da Rio Service!')

if __name__ == "__main__":
    application.run()