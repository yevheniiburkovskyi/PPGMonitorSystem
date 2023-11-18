import heartpy as hp
import numpy as np

def getMesures(signal_df):
  signal = signal_df['Signal'].values
  hp.process(signal, sample_rate = 100.0)
  return hp.process(signal, sample_rate = 100.0)

def getAverageParams(data):

  keys = data[0].keys()

  average_values = {}
  
  for key in keys:
      values = [item[key] for item in data]
      average_values[key] = np.mean(values)

  return average_values