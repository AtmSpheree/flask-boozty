# flask-boozty
A parody of the Boosty service, developed on the Flask micro framework of the Python programming language.
### Written in Python 3.10.9!!!
#### !!!
This version is already partially completed, and will be further developed later. The ability to restore your account by email, the ability to edit your profile and records will be added.
## Installation
1. Create and activate [venv](https://docs.python.org/3/library/venv.html)
2. Using [pip](https://pip.pypa.io/en/stable/) install packages from **requirements.txt**.
```bash
pip install -r requirements.txt
```
# Warning
### The flask-uploads module uses the werkzeug library is currently not supported. To run the code after installing requirements, you need to change the line in the file import block Lib/site-packages/flask_uploads.py
```bash
from werkzeug import secure_filename, FileStorage
```
replace with:
```bash
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
```
## Using
1. Run main.py file from project directory.
2. Enjoy!
