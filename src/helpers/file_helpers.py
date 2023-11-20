import os
import pandas as pd
import random
import string
import time

def getParsedSignal(file_path: str) -> pd.DataFrame:
  parsed_df = pd.read_excel(file_path)
  ppg_signal_df = parsed_df.iloc[:, 0:2]

  ppg_signal_df=ppg_signal_df.drop(ppg_signal_df.index[0])
  ppg_signal_df.reset_index(drop=True, inplace=True)
  ppg_signal_df.columns = ['Time', 'Signal']

  return ppg_signal_df

def getFileNames(path) -> list[str]:
  files = os.listdir(path)
  file_names = []
  
  for file_name in files:
      file_names.append(file_name)
      
  return file_names

def generateUniqueFileName(file_names: list[str]) -> str:
    while True:
        unique_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Генерація випадкового імені з 8 символів
        
        if unique_name not in file_names:
            return unique_name
          
def getParsedAverageParamsDict(path: str) -> dict:

  data = pd.read_excel(path, header=None, index_col=0)

  data_dict = data.squeeze().to_dict()
  
  del(data_dict['Parameter'])

  return data_dict

def getCreationFilesTime(paths: str) -> list[str]:
  data_list: list[str] = []
  
  for path in paths:
    creation_time = os.path.getctime(path)
    creation_datetime = time.ctime(creation_time)
    data_list.append(creation_datetime)
  
  return data_list