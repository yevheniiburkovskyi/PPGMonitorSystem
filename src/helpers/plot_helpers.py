import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
import numpy as np

def buildPlot (data):
    
	x_data = data['Time']
	y_data = data['Signal']

	plt.figure(figsize=(20, 10))

	plt.plot(x_data, y_data, linestyle='-')

	plt.title('Сигнали')
	plt.xlabel('Time')
	plt.ylabel('Signal')
	plt.grid(True)

	plt.show() 


# def buildParamPlot(dates: list[str], params: list[float]):
def buildParamPlot():
  
	# # Зразки даних

	# # Перетворюємо стрічки дати в об'єкти datetime
	# dates = [datetime.strptime(date_string, '%a %b %d %H:%M:%S %Y') for date_string in dates]

	# # Побудова графіку
	# plt.figure(figsize=(10, 6))
	# plt.plot(dates, params, marker='o', linestyle='-')
	# plt.title('Залежність сигналу від дати та часу вимірювання')
	# plt.xlabel('Дата і час вимірювання')
	# plt.ylabel('Виміряний сигнал')
	# plt.xticks(rotation=45)
	# plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))  # Форматування дати
	# plt.tight_layout()
	# plt.show()
# Import Library

# Define Data

	x = [1, 2, 3, 4, 5]
	y = [2, 4, 6, 8, 10]

	# Plot

	plt.plot(x, y)

	# Display

	plt.show()