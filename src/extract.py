from pandas import DataFrame
from ocr_apis import get_ocr_sw
from utils import join_dir_files, get_latest_files, get_where_index, read_props_file, service_filter, multi_mode, get_serv_res_transcripts_with_threshold, get_concat_ogl_res_met_for_servs

ogl_df,res_df,met_df=['','','']

def get_failed_transcripts(ogl_df,res_df,met_df,services=None,media='both'):
        return [get_serv_res_transcripts_with_threshold(ogl_df,res_df,met_df,serv,1.0,exp='==') for serv in service_filter(media,filter=servs)]

def get_perfect_transcripts(ogl_df,res_df,met_df,services=None,media='both'):
        return [get_serv_res_transcripts_with_threshold(ogl_df,res_df,met_df,serv,0.0,exp='==') for serv in service_filter(media,filter=servs)]

def get_by_file_name(ogl_df,res_df,met_df,file_name,service=None,media='both'):
        if not(file_name in list(ogl_df.index)): return [False,'{} image file not found'.format(file_name)]
        where_true=get_where_index(ogl_df,tt=[file_name==rec for rec in list(ogl_df.index)])
        return get_concat_ogl_res_met_for_servs(ogl_df,res_df,met_df,servs=service_filter(media,filter=service),ind_arr=where_true)

def setup(prps_file_path,ogl_dir,res_dir,met_dir,media='both'):
        file_paths=[join_dir_files(dir,list(map(lambda serv:get_latest_files(dir,serv),get_ocr_sw(media)))) for dir in [ogl_dir,res_dir,met_dir]]
        file_names=list(read_props_file(prps_file_path).filename)
        global ogl_df
        ogl_df=DataFrame.from_dict(multi_mode(file_paths)['ogl'])
        ogl_df.index=file_names
        global res_df
        res_df=DataFrame.from_dict(multi_mode(file_paths)['res'])
        res_df.index=file_names
        global met_df
        met_df=DataFrame.from_dict(multi_mode(file_paths)['met'])[:-1]
        met_df.index=file_names