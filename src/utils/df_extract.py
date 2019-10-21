from pandas import concat
from ocr_apis import get_ocr_sw
from utils import get_n_elements, get_where

def service_filter(media,filter=None):
    servs=get_ocr_sw(media)
    servs_filter=[]
    if not(bool(filter)): servs_filter=''
    elif isinstance(filter,list): servs_filter=tuple(filter)
    else: servs_filter=tuple(servs_filter+[filter])
    return get_where(servs,tt=[serv.startswith(servs_filter) for serv in servs])

def multi_mode(modes_files_paths):
    return {k:v for dict in list(map(single_mode,modes_files_paths)) for k,v in dict.items()}

def single_mode(file_paths,mode='ogl'):
    temp_mode=file_paths[0].split('/')[:-1][-1]
    if temp_mode in ['ogl','res','met']: mode=temp_mode
    return {mode: {k:v for dict in list(map(single_serv,file_paths,get_n_elements(mode,len(file_paths)))) for k,v in dict.items()}}

def single_serv(file_path,mode='ogl'):
    with open(file_path,'r') as f:
        serv=file_path.split('/')[-1].split('.')[0] if mode=='ogl' else file_path.split('/')[-1].split('D')[0]
        vals=[float(line.split(' ')[-1].strip()) for line in f.readlines()] if mode=='met' else [line.strip() for line in f.readlines()]
        return {serv:vals}

def get_concat_ogl_res_met_for_servs(ogl_df,res_df,met_df,media='both',servs=None,ind_arr=None,bool_arr=None):
    if not(bool(servs)): servs=get_ocr_sw(media)
    if bool(ind_arr): return concat([get_concat_ogl_res_met_for_serv(ogl_df,res_df,met_df,serv,ind_arr=ind_arr) for serv in servs],axis=1)
    if bool(bool_arr): return concat([get_concat_ogl_res_met_for_serv(ogl_df,res_df,met_df,serv,bool_arr=bool_arr) for serv in servs],axis=1)

def get_concat_ogl_res_met_for_serv(ogl_df,res_df,met_df,serv,ind_arr=None,bool_arr=None):
    if bool(ind_arr): ogl,res,met=get_concat_ogl_res_met_ind_arr(ogl_df,res_df,met_df,serv,ind_arr)
    else: ogl,res,met=get_concat_ogl_res_met_bool_arr(ogl_df,res_df,met_df,serv,bool_arr)
    df=concat([ogl,res,met],axis=1) 
    df.columns=['{0}-{1}'.format(serv,name) for name in ['ogl','res','met']]
    return df

def get_concat_ogl_res_met_ind_arr(ogl_df,res_df,met_df,serv,ind_arr):
    return (ogl_df.iloc[ind_arr][serv],res_df.iloc[ind_arr][serv],met_df.iloc[ind_arr][serv])

def get_concat_ogl_res_met_bool_arr(ogl_df,res_df,met_df,serv,bool_arr):
    return (ogl_df[serv][bool_arr],res_df[serv][bool_arr],met_df[serv][bool_arr])

def get_servs_res_transcripts_with_threshold(ogl_df,res_df,met_df,servs,threshold,exp='<'):
    return [get_serv_res_transcripts_with_threshold(ogl_df,res_df,met_df,serv,threshold,exp) for serv in servs]

def get_serv_res_transcripts_with_threshold(ogl_df,res_df,met_df,serv,threshold,exp='<'):
    bool_arr=eval('list(met_df[serv]'+''.join(list(map(str,[exp,threshold])))+')')
    return get_concat_ogl_res_met_for_serv(ogl_df,res_df,met_df,serv,bool_arr=bool_arr)