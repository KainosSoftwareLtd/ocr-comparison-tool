import argparse
from utils import main

parser=argparse.ArgumentParser(description='Generate OCR performance')

parser.add_argument('-d','--dir',dest='DIR',help='Directory of OCR as described *')
parser.add_argument('-i','--img',dest='IMG',help='Path to image directory or file')
parser.add_argument('-o','--ogl',dest='OGL',nargs='+',help='Path to original transcript directory or file')
parser.add_argument('-p','--prp',dest='PRP',help='Filename for property .csv file')
parser.add_argument('-m','--med',dest='MED',help='Media mode for the OCR services')

args=parser.parse_args()

media=args.MED if args.MED in ('both','document','image') else 'both'

if args.DIR: print(main(base_dir=args.DIR,media='both'))
else: print(main(gen_ogl=not(bool(args.OGL)),props_filename=args.PRP,ogl_file_paths=args.OGL,img_file_path=args.IMG,media=media)) if args.PRP else print(main(gen_ogl=not(bool(args.OGL)),ogl_file_paths=args.OGL,img_file_path=args.IMG,media=media))