import pandas as pd

def getParsedSignal(file_path: str) -> pd.DataFrame:
  parsed_df = pd.read_excel(file_path)
  ppg_signal_df = parsed_df.iloc[:, 0:2]

  ppg_signal_df=ppg_signal_df.drop(ppg_signal_df.index[0])
  ppg_signal_df.reset_index(drop=True, inplace=True)
  ppg_signal_df.columns = ['Time', 'Signal']

  return ppg_signal_df