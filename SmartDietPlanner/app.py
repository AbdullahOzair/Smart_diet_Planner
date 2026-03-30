import os
import sys
import subprocess

if __name__ == '__main__':
    # Convenience wrapper to run the actual application located in flask_app/
    # This prevents 'ModuleNotFoundError' when trying to run the project from the root folder.
    
    flask_app_dir = os.path.join(os.path.dirname(__file__), 'flask_app')
    
    if not os.path.exists(flask_app_dir):
        print('Error: flask_app directory not found!')
        sys.exit(1)
        
    print('======================================================')
    print('  Starting the Smart Diet Planner Application...      ')
    print('======================================================')
    
    os.chdir(flask_app_dir)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print('\nServer stopped.')
    except Exception as e:
        print(f'Error running application: {e}')
