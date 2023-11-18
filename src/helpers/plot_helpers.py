import matplotlib.pyplot as plt

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