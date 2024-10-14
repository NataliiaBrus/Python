import os
import shutil

def clean_raw_dir(raw_dir):
  
    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
    os.makedirs(raw_dir)