from utils import make_dir
import pandas as pd
import os

folders = ['gravity',
  'parameters',
  'total_effects_vzp_without_rec',
  'total_effects_vzp_with_rec',
  'total_effects_vz_without_rec',
  'total_effects_vz_with_rec',
  'total_winds_without_rec',
  'total_winds_with_rec',
  'vertical_drift',
  'winds_and_vzp_without_rec',
  'winds_and_vzp_with_rec',
  'winds_and_vz_without_rec',
  'winds_and_vz_with_rec',
  'winds_without_rec',
  'winds_with_rec']

root = "D:\\plots\\parameters"

def create_dirs(folders, root):
   
    for folder in folders:
        
        path = make_dir(os.path.join(root, folder))
        
        create_months_folders(path)
        
def create_months_folders(infile):

    ts = pd.date_range("2013-1-1", "2013-12-31", freq = "1M")
      
    for dn in ts:
        month_name = dn.strftime("%m")
        
        make_dir(
            os.path.join(infile, month_name)
            )
        
def add_month_folder():
    root = "D:\\plots\\vertical_drift"
    
    #for folder in os.listdir(root):
    create_months_folders(root)
        
        
add_month_folder()