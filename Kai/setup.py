import os
import shutil

import chromadb
from setting import PERSISTANT_PATH


def setup_application():
    if not os.path.exists(PERSISTANT_PATH):
        os.makedirs(PERSISTANT_PATH)
    chromadb.PersistentClient(path=PERSISTANT_PATH)

def reset_application():
    if os.path.exists(PERSISTANT_PATH):
        shutil.rmtree(PERSISTANT_PATH)
    setup_application()
