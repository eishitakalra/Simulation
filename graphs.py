from simulation import Simulation 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

def barplot(mylist , xtitle , ytitle , title):
    plt.figure(figsize=(8, 6))
    sns.histplot(mylist, discrete=True, kde=False, bins=len(set(mylist)))
    plt.ylabel(ytitle)
    plt.title(title)
    plt.savefig(title)  
    plt.close()


def cdfplot(my_list, xtitle, ytitle, title):
    # Sort the data
    sorted_data = np.sort(my_list)
    
    # Calculate the cumulative distribution
    y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    # Plot the CDF
    plt.figure(figsize=(8, 6))
    plt.plot(sorted_data, y_values, color='blue', alpha=0.7)

    # Set the labels and title
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)

    # Set both axes to start from 0 (same origin for both x and y)
    plt.xlim(left=0)  # x-axis starts at 0
    plt.ylim(bottom=0)  # y-axis starts at 0

    # Save the plot as an image or show it
    plt.savefig(title + ".png")  # Save to a file
    plt.close() 


def scatterplot(clients, profit, xtitle,ytitle,title):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=clients, y=profit, alpha=0.7, edgecolor=None)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.grid(True)
    plt.savefig(title + ".png")  # Save to a file
    plt.close() 

def histplot(my_list,xtitle,ytitle,title): 
    plt.figure(figsize=(8, 6))
    sns.histplot(my_list, bins=30, kde=True)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.savefig(title + ".png")  
    plt.close()
