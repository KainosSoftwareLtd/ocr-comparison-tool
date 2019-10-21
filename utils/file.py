from os import system, getcwd, listdir, mkdir, remove
from os.path import isfile, getctime
from pandas import read_csv
from .misc import get_timestamp, get_where, get_n_elements

def join_dir_files(dir,filenames,ts=None,ext='.txt',add_ext=False):
    return [join_dir_file(dir,filename,ts,ext,add_ext) for filename in filenames]

def join_dir_file(dir,filename,ts=None,ext='.txt',add_ext=False):
    file_path=dir+filename
    if ts: file_path=file_path+ts
    return file_path+ext if add_ext else file_path
    
def get_current_dir():
    return '{}/'.format(getcwd())

def get_dir_files(dir,ign_hidden=True):
    return sorted(get_where(listdir(dir),tt=[not(file_path.startswith('.')) for file_path in listdir(dir)])) if ign_hidden else sorted(listdir(dir))

def get_filenames_from_paths(file_paths):
    return list(map(get_filename_from_path,file_paths))

def get_filename_from_path(file_path):
    try: return file_path.split('/')[-1]
    except: return [False,'There was an issue getting the filename from {}'.format(file_path)]

def get_files_that_exist(*file_paths):
    if isinstance(file_paths[0],str): return get_where(file_paths,tt=[isfile(file_path) for file_path in file_paths]) 
    else: return get_where(file_paths[0],tt=[isfile(file) for file_path in file_paths for file in file_path])

def get_latest_files(dir,filename):
    files=get_where(get_dir_files(dir),func=lambda x: x.startswith(filename))
    return max(get_files_that_exist(join_dir_files(dir,files)),key=getctime).split('/')[-1]

def read_props_file(props_file_path):
    return read_csv(props_file_path).fillna('')

def remove_file(file_path):
    if isfile(file_path): remove(file_path)

def copy_files(recipient_file_paths,receiving_file_paths):
    if all([status[0] for status in list(map(copy_file,recipient_file_paths,receiving_file_paths))]): return [True,'All files copied']
    return [False,'There was an issue copying from files: {0} to: {1}'.format(', '.join(recipient_file_paths),', '.join(receiving_file_paths))]

def copy_file(recipient_file_path,receiving_file_path):
    if not(bool(get_files_that_exist(recipient_file_path))): return [False,'{} file does not exist'.format(recipient_file_path)]
    system('cp '+recipient_file_path+' '+receiving_file_path)
    return [True,'{0} file copied to {1}'.format(recipient_file_path,receiving_file_path)]

def overwrite_files(file_paths,recs,map_each=False):
    try:
        list(map(remove_file,file_paths))
        save_to_files(file_paths,recs,map_each=map_each)
        return[True,'All files overwritten']
    except: return [False,'There was an issue overwritting files: {}'.format(', '.join(file_paths))]

def overwrite_file(file_path,rec):
    if(isfile(file_path)): remove(file_path)
    write_to_file(file_path,rec)

def save_to_files(file_paths,recs,map_each=False):
    try: 
        [write_to_file(file_path,rec) for rec in recs for file_path in file_paths] if map_each else list(map(write_to_file,file_paths,recs))
        return [True,'All files saved down']
    except: return [False,'There was an issue saving down files: {}'.format(', '.join(file_paths))]

def write_to_file(file_path,rec,mode='a+'):
    try:
        with open(file_path,mode) as f:
            f.write(rec+'\n')
        return [True,'{0} written to {1}'.format(rec,file_path)]
    except: return [False,'There was an issue writing {0} to {1} '.format(rec,file_path)]

def create_dirs(base_dir,*dirs):
    return list(map(lambda dir: create_dir(dir),join_dir_files(base_dir,dirs)))

def create_dir(dir):
    try:
        mkdir(dir)
        return [True,'{} created'.format(dir)]
    except: return [False,'There was an issue creating {}'.format(dir)]

def get_structure(base_dir,*dirs):
    return tuple(join_dir_files(base_dir,dirs))

def handle_method_returns(ts,input,msg='',mode='debug'):
    if not(isinstance(input,list)): success=input
    else:
        success=input[0]
        try: msg=input[1]
        except: msg=''
    if mode=='debug': log(ts,success,msg,mode=mode)
    return success

def log(ts,status,msg,log_dir=get_current_dir()+'log/',log_ext=None,mode='live'):
    create_dir(log_dir)
    log_filename=mode+'-log-'
    log_file_path=join_dir_file(log_dir,log_filename+log_ext,ts=ts,add_ext=True) if log_ext else join_dir_file(log_dir,log_filename,ts=ts,add_ext=True)
    status='SUCCESS' if status else 'FAILURE'
    rec=get_timestamp()+': '+'['+status+'] | '+msg
    return write_to_file(log_file_path,rec)    