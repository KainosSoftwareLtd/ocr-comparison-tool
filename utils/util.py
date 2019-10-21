import ocr_settings
from ocr_apis import get_ocr_sw, get_text
from .file import handle_method_returns, join_dir_file, join_dir_files, get_files_that_exist, get_filenames_from_paths, get_dir_files, get_current_dir, get_latest_files, copy_files, read_props_file, save_to_files, overwrite_files, create_dirs, get_structure, write_to_file, overwrite_file, log
from .metric import generate_transcripts_metrics, extract_metrics
from .misc import get_timestamp, get_n_elements, are_lists_same_size

PRP_FILE='props.csv'

OGL_DIR_EXT='ogl/'
RES_DIR_EXT='res/'
MET_DIR_EXT='met/'
IMG_DIR_EXT='imgs/'

batch_cache=[]
media_cache={}

def main(base_dir=get_current_dir(),ts=get_timestamp(),gen_ogl=True,props_filename=PRP_FILE,ogl_file_paths=None,img_file_path=None,media='both'):
    props_file_path=get_files_that_exist(join_dir_file(base_dir,props_filename))
    ocr_servs=get_ocr_sw(media)
    ogl_dir,res_dir,met_dir=get_structure(base_dir,OGL_DIR_EXT,RES_DIR_EXT,MET_DIR_EXT)
    create_dirs('',ogl_dir,res_dir,met_dir)
    if base_dir!=get_current_dir():
        img_dir=join_dir_file(base_dir,IMG_DIR_EXT)
        return wrapper(ts,ocr_servs,gen_ogl,res_dir,met_dir,props_file_path,media,ogl_dir=ogl_dir,img_dir=img_dir)
    if bool(img_file_path) and not(bool(get_files_that_exist(img_file_path))): return {'The image provided is null or does not exist'}
    if gen_ogl: return wrapper(ts,ocr_servs,gen_ogl,res_dir,met_dir,props_file_path,media,ogl_dir=ogl_dir,img_file_path=img_file_path)
    if not(bool(get_files_that_exist(ogl_file_paths))): return {'The transcript file does not exist'}
    if 1==len(ogl_file_paths):
        receiving_files=join_dir_files(ogl_dir,ocr_servs,add_ext=True)
        if not(handle_method_returns(ts,copy_files(get_n_elements(ogl_file_paths[0],len(receiving_files)),receiving_files))): return {'Cannot copy the original transcript'}
        ogl_file_paths=receiving_files
    if not(sorted([filename.split('.')[0] for filename in get_filenames_from_paths(ogl_file_paths)])==sorted(get_ocr_sw(media))): return {'The original transcripts file(s) provided do not match the OCR service(s) {}'.format(', '.join(get_ocr_sw(media)))}
    return wrapper(ts,ocr_servs,gen_ogl,res_dir,met_dir,props_file_path,media,ogl_file_paths=ogl_file_paths,img_file_path=img_file_path)

def wrapper(ts,ocr_servs,gen_ogl,res_dir,met_dir,props_file_path,media,ogl_dir=None,img_dir=None,ogl_file_paths=None,img_file_path=None):
    if not(handle_method_returns(ts,parse_original_transcripts(ts,ocr_servs,gen_ogl,ogl_dir,img_dir,props_file_path,ogl_file_paths,img_file_path))): return {'Cannot parse'}
    if not(handle_method_returns(ts,save_result_transcripts_wrapper(ts,img_dir,res_dir,img_file_path,media))): return {'Cannot save OCR service(s) transcripts'}

    ogl_file_paths=join_dir_files(ogl_dir,ocr_servs,add_ext=True) if ogl_dir else ogl_file_paths
    res_file_paths=join_dir_files(res_dir,[get_latest_files(res_dir,serv) for serv in ocr_servs])
    met_file_paths=join_dir_files(met_dir,[get_latest_files(res_dir,serv) for serv in ocr_servs])
    
    if not(handle_method_returns(ts,generate_transcripts_metrics(ogl_file_paths,res_file_paths,met_file_paths))): return {'Cannot generate CharacTER metrics'}
    return [True,extract_metrics(met_file_paths)]

def parse_original_transcripts(ts,ocr_servs,gen_ogl,ogl_dir,img_dir,props_file_path,ogl_file_paths,img_file_path):
    if gen_ogl:
        if not(bool(props_file_path)): return [False,'The properties file {} does not exist'.format(props_file_path)]
        props_file_path=props_file_path[0]
        ogl_file_paths=join_dir_files(ogl_dir,ocr_servs,add_ext=True)
        if not(handle_method_returns(ts,generate_original_transcripts(ogl_file_paths,props_file_path))): return [False,'There is an issue generating the original transcripts']
    img_file_paths=img_file_path.split(' ') if img_file_path else get_dir_files(img_dir)
    return check_original_transcripts(gen_ogl,ogl_file_paths,img_file_paths,props_file_path)

def check_original_transcripts(gen_ogl,ogl_file_paths,img_file_paths,props_file_path):
    if(not(bool(get_files_that_exist(ogl_file_paths)))): return [False,'The original transcripts file(s) {} does not exist'.format(', '.join(ogl_file_paths))]
    num_ogl_file_lines=list(map(lambda file: len(['' for line in open(file)]),get_files_that_exist(ogl_file_paths)))
    if not(are_lists_same_size(num_ogl_file_lines)): return [False,'The original transcripts length(s) are different {}'.format(', '.join(list(map(lambda file_path,line_count: '{0} has {1} line(s)'.format(file_path,line_count),ogl_file_paths,num_ogl_file_lines))))]
    if len(img_file_paths)!=num_ogl_file_lines[0]: return [False,'There are {0} images to process which is different to the {1} transcript(s) provided'.format(len(img_file_paths),num_ogl_file_lines[0])]
    if not(gen_ogl): return [True,'All original transcript checks passed but cannot check the order of transcripts to image files']
    df=read_props_file(props_file_path)
    filenames=[filename.strip() for filename in list(df.filename)]
    if filenames!=get_filenames_from_paths(img_file_paths): return [False,'records in: '+props_file_path+' don\'t match the order of the sorted images: '+', '.join(img_file_paths)]
    return [True,'All original transcript checks passed']

def generate_original_transcripts(ogl_file_paths,props_file_path):
    try:
        df=read_props_file(props_file_path)
        overwrite_files(ogl_file_paths,df.text,map_each=True)
        return [True,'Original transcripts generated']
    except: return [False,'There is an issue when attempting to generate the original transcript(s)']

def save_result_transcripts_wrapper(ts,img_dir,res_dir,img_file_path,media):
    if bool(img_file_path): return save_result_transcripts(ts,res_dir,img_file_path,media)
    img_file_paths=join_dir_files(img_dir,get_dir_files(img_dir))  
    num_imgs=len(img_file_paths)
    ts_arr=get_n_elements(ts,num_imgs)
    res_dir_arr=get_n_elements(res_dir,num_imgs)
    if not(isinstance(media,list)): save_res=list(map(save_result_transcripts,ts_arr,res_dir_arr,img_file_paths,get_n_elements(media,num_imgs)))
    elif are_lists_same_size(img_file_paths,media): save_res=list(map(save_result_transcripts,ts_arr,res_dir_arr,img_file_paths,media))
    else: return [False,'There are {0} images to be processed which is different to the {1} media definitons'.format(num_imgs,len(media))]
    
    if 1==len(set(tuple(res) for res in save_res)): return save_res[0]
    return get_where(save_res,tt=[not(res[0]) for res in save_res])[0]

def save_result_transcripts(ts,res_dir,img_file_path,media):
    global media_cache 
    media_cache=get_text(img_file_path,media)
    batch_cache.append(media_cache)
    return save_to_files(join_dir_files(res_dir,media_cache.keys(),ts=ts,add_ext=True),media_cache.values())