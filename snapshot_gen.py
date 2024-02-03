import os
from datetime import datetime

source_dir = 'bitcoin'
snapshot_file = 'snapshot1.txt'

def create_snapshot(source, snapshot):
    with open(snapshot, 'w') as f:
        for root, dirs, files in os.walk(source):
            for name in files:
                file_path = os.path.join(root, name)
                file_mtime = str(os.path.getmtime(file_path))
                f.write(f"{file_path}|{file_mtime}\n")

create_snapshot(source_dir, snapshot_file)
