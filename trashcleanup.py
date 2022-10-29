#!/usr/bin/python3

# Trash Cleanup - Maintains a list of files in a "temporary" folder and autodeletes them after 2 months.

import os, shelve, datetime, logging
from pathlib import Path

stats = {'num files deleted': 0, 'empty directories removed': 0, 'files modified': 0 }
temp_dir = Path.home() / 'Downloads/2 months to live/'
lifespan = datetime.timedelta(days=60)
cleanup_data = temp_dir / 'logs/'
shelf_file = shelve.open(os.path.join(cleanup_data, 'cleanup_shelf'))
logfpath = cleanup_data / datetime.datetime.now().strftime('%Y_%m%d_trashcollector.log')

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s -  %(message)s', filename=logfpath)

assert temp_dir.is_dir(), 'Missing temporary directory. Expected to find a directory at ' + str(temp_dir)
assert cleanup_data.is_dir(), 'Missing logfile directory. Expected at ' + str(cleanup_data)

def remove_garbage(fpath): # deletes old files and updates changelog
    global temp_dir
    global cleanup_data

    now = datetime.datetime.now().strftime('%b %d, %y') # e.g. Nov 13, 22
    fsize = os.path.getsize(fpath)
    
    # print('Dry run deletion: %s' % fpath)
    os.unlink(fpath)
    logging.info(os.path.relpath(fpath, temp_dir) + ' ### GONE! ###')
    changelog = open(cleanup_data / 'deletions.txt', 'a')
    changelog.write(f'{now.ljust(10)} - {round(fsize / 1_000_000, 1):,} MB saved. {os.path.relpath(fpath, temp_dir)}\n')
    changelog.close()

try:
    hitdict = shelf_file['hitdict']
    missing_files = []
    for fpath in hitdict.keys(): # remove files from dictionary that no longer exist
        if not os.path.exists(fpath):
            missing_files.append(fpath)
    for goner in missing_files:
        hitdict.pop(goner)
        logging.info('Removed %s from dictionary directory.' % os.path.relpath(goner, temp_dir))

except KeyError:
    logging.info('No shelf file found. Creating a new one.')
    hitdict = {}
    shelf_file['total deletions'] = 0

logging.info("Shelf loaded. %s items on the chopping block today." % len(hitdict))

for folder_name, sub_folders, filenames in os.walk(temp_dir):
    for sub_folder in sub_folders:
        sub_folder = Path(folder_name) / sub_folder
        try:
            os.rmdir(sub_folder)
            logging.info('Removed empty directory %s' % os.path.relpath(sub_folder, temp_dir))
            stats['empty directories removed'] += 1            
        except OSError:
            continue

    for filename in filenames:
        k = Path(folder_name) / filename # dictionary keys are the path to the file
        
        birthday = hitdict.setdefault(k, datetime.datetime.now()) # adds file birthday with current time if it doesn't already exist
        modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(k))
        if modify_time > birthday:
            birthday = modify_time # modifying file "resets the clock" on when it will get deleted
            hitdict[k] = birthday
            logging.info('File modified. Updating TTL: %s' % os.path.relpath(k, temp_dir))
            stats['files modified'] += 1
        elif birthday + lifespan < datetime.datetime.now():
            remove_garbage(k)
            hitdict.pop(k)
            stats['num files deleted'] += 1

logging.info('%s empty directories removed.' % stats['empty directories removed'])
logging.info('%s total files changed.' % stats['files modified'])
logging.info('%s files deleted today.' % stats['num files deleted'])
logging.info('%s files deleted all-time.' % (shelf_file['total deletions'] + stats['num files deleted']))
shelf_file['hitdict'] = hitdict
shelf_file['total deletions'] += stats['num files deleted']
shelf_file.close()