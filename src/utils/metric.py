from os import system, environ
from functools import reduce

CHARACTER_SCRIPT_PATH=environ.get('CHARACTER_SCRIPT_PATH')

def generate_transcripts_metrics(ogl_file_paths,res_file_paths,met_file_paths):
    try:
        list(map(execute_CharacTER_for_file,ogl_file_paths,res_file_paths,met_file_paths))
        return [True,'CharacTER metrics generated']
    except: return [False,'There was an issue generating the CharacTER metrics']
      
def execute_CharacTER_for_file(ogl_file_path,res_file_path,met_file_path):
    try:
        py_exe='python3 '
        charTER_script=CHARACTER_SCRIPT_PATH+' '
        ref_cmd='--ref '+ogl_file_path+' '
        hyp_cmd='--hyp '+res_file_path+' '
        print_stdout_to_file='-v > '+met_file_path
        exe_cmd=reduce(lambda x,y:x+y,[py_exe,charTER_script,ref_cmd,hyp_cmd,print_stdout_to_file])

        system('touch '+met_file_path+';'+exe_cmd)
        return [True,'Metric generated and stored in {}'.format(met_file_path)]
    except: return [False,'There was an issue running command {}'.format(exe_cmd)]

def extract_metrics(met_file_paths):
    return list(map(extract_metric,met_file_paths))

def extract_metric(met_file_path):
    try:
        with open(met_file_path) as f:
            return {met_file_path.split('/')[-1].split('D')[0]:float(f.readlines()[-1].strip())}
    except: return {met_file_path.split('/')[-1].split('D')[0]:'Incorrect number of transcripts to be interpretated'}