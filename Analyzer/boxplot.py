
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
 
 
# Creating dataset
np.random.seed(10)
 
data_1 = [5,4,10,3,5,7]
data_2 = [5,4,10,12,29,27,3,5,7]
data_3 = [5,4,10,3,5,7]
data_4 = [5,4,10,3,5,7]
data = [data_1, data_2, data_3, data_4]
 
fig = plt.figure(figsize =(5, 7))
 
# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])
 
# Creating plot
bp = ax.boxplot(data)
 
# show plot
plt.show()
plt.savefig("mygraph.png")