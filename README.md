# ILapp-barebones

This project serves as an webapp back-end for online experiments, particularly those utilizing iterative learning. Its aim is to create an efficient, modular site leveraging Flask.

## Flask URL Creation

New experiments get their own url in application.py, using the following syntax (see the demo experiment as an example):

```
@app.route('/exmperimentname', methods=['GET', 'POST'])
def experimentname():
    '''Function description'''

    if request.method == 'POST':
        '''DO DATA COLLECTION'''
    
    return render_template('experimentname_page.html')
    
```

HTML templates go in the templates folder. These use Jinja2 rendering to help with security and ease of template creation (see Flask documentation for more details).

CSS and JS go in the static folder, or a subdirectory thereof. Things like images or audio samples should also go in here.

## Working in this project

Use venv when testing this code. This will allow you to avoid package conflicts.

To create a virtual environment (at least on Linux), go into your working directory and enter
`python3 -m venv venv`
Then, activate it with
`. venv/bin/activate`

Alternatively, check out virtualenvwrapper. It provides nice (but not strictly necessary) utilities for venv management.

After your venv is active, you should be able to enter `pip install -r requirements.txt` to install all the dependencies for this project. If you add new dependencies, run `pip freeze > requirements.txt` and commit the new requirements file.

To host the webapp locally for testing, enter
```
export FLASK_APP=application
flask run
```
CTRL+C exits the server.

Lastly, make sure your venv (and project, and vscode) directory is in .gitignore, to avoid conflicting venvs getting pushed to GitHub.

## Running a Demo Experiment

After the Flask server is running, the link `localhost:5000/demo` will run a demo experiment. The demo is three trials long, and demonstrates data iteration methods after the fifth time the link is accessed (split size is 2, gen size is 4). Results can be found in the `results/demo` directory.

## Deployment Checklist

1. Ensure that requirements.txt is up to date
2. Commit all relevant files
3. Sync commits to GitHub
4. Makes sure everything runs!
5. Ensure that the most recent S3 data backup is good
6. Draft a new release on GitHub; tag a new version
7. (Optional) If there were problems with the most recent S3 backup, edit as necessary, then run a manual backup
