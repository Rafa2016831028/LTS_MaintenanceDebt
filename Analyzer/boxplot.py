
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
 
 
# Creating dataset
np.random.seed(10)
 
Bug = [5,4,10,3,5,7]
code_smell = [5,4,10,12,29,27,3,5,7]
vulnerability = [5,4,10,3,5,7]
# data_4 = [5,4,10,3,5,7]
data = [ Bug, code_smell, vulnerability]
 
fig = plt.figure(figsize =(8, 10))
 
# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])
 
# Creating plot
bp = plt.boxplot(data)
 
# show plot
plt.show()
plt.savefig("mygraph.png")