import matplotlib.pyplot as plt
import numpy as np

x = np.arange(250, 8001, 250)

y = []

text_box = plt.text(0.5, 0.9, "Enter decibel values:")

points = plt.ginput(6)

for point in points:
    y.append(point[1])

plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
		marker='o', markerfacecolor='blue', markersize=12)

plt.ylim(-10,100)
plt.xlim(250,8000)

plt.xlabel('Frequencies (Hz)')
plt.ylabel('Decibels (dB)')

plt.title('Audiogram')

plt.show()
