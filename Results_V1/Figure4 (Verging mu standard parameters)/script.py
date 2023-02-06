import matplotlib.pyplot as plt
import csv
from statistics import*
from math import*

## DON'T CHANGE BETWEEN THE LINE
#######################################################################################################################

name_list = ["Amdahl","Communication","General","Roofline"]
p_list = [500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
mu_list = [0.02,0.06,0.1,0.14,0.18,0.22,0.26,0.3,0.34,0.38,(3-sqrt(5))/2]
n_list = [100,200,300,400,500,600,700,800,900,1000]

for name in name_list :
    Paper = [[] for i in range(11)]
    Min_time = [[] for i in range(11)]
    f = open(name+"/all.csv",newline='')
    reader = csv.reader(f)
    for row in reader :
        if row[0] != "mu" :
            if row[0] == "0.02" :
                index = 0
            if row[0] == "0.06" :
                index = 1
            if row[0] == "0.1" :
                index = 2
            if row[0] == "0.14" :
                index = 3
            if row[0] == "0.18" :
                index = 4
            if row[0] == "0.22" :
                index = 5
            if row[0] == "0.26" :
                index = 6
            if row[0] == "0.3" :
                index = 7
            if row[0] == "0.34" :
                index = 8
            if row[0] == "0.38" :
                index = 9
            if row[0] == "0.3819660112501051":
                index = 10

            Paper[index] += [float(row[1]) / float(row[3])]
            Min_time[index] += [float(row[2]) / float(row[3])]

    f.close()
    f = open(name+"/mean.csv",'w',newline='')
    writer = csv.writer(f)
    mean_Paper = []
    mean_Time = []
    for k in mu_list :
        if k == 0.02 :
            index = 0
        if k == 0.06 :
            index = 1
        if k == 0.1 :
            index = 2
        if k == 0.14 :
            index = 3
        if k == 0.18 :
            index = 4
        if k == 0.22:
            index = 5
        if k == 0.26 :
            index = 6
        if k == 0.3 :
            index = 7
        if k == 0.34 :
            index = 8
        if k == 0.38 :
            index = 9
        if k == (3-sqrt(5))/2 :
            index = 10

        mean_Paper += [mean(Paper[index])]
        mean_Time += [mean(Min_time[index])]
        writer.writerow([k, mean(Paper[index]), mean(Min_time[index])])
    f.close()

#######################################################################################################################

    plt.plot(mu_list,mean_Paper,label='Algo Paper')
    plt.xlabel("mu")
    plt.legend()
    plt.ylabel("Normalized Makespan")
    plt.savefig("plot_4_"+name+".png")
    plt.show()