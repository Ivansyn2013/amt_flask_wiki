from flask_admin import static
import os
import shutil
import flask_admin

if __name__ == "__main__":

    path = os.path.dirname(flask_admin.__file__)
    src = path + '/static'
    destination = os.getcwd() + '/admin' + '/static'
    shutil.copytree(src, destination)
    #print(path)
