
import matplotlib.pyplot as plt
import csv

## DON'T CHANGE BETWEEN THE LINE
#######################################################################################################################

name_list = ["Amdahl","Communication","General","Roofline"]
p_list = [500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
mu_list = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36,0.38]
n_list = [100,200,300,400,500,600,700,800,900,1000]

for name in name_list :
    Paper = []
    Min_time = []
    f = open(name + "/all.csv",newline='')
    reader = csv.reader(f)
    for row in reader :
        if row[0] != "i" :

            Paper += [float(row[1]) / float(row[3])]
            Min_time += [float(row[2]) / float(row[3])]
    f.close()

#######################################################################################################################

    plt.boxplot([Paper,Min_time])
    plt.xlabel("Algorithm")
    plt.xticks([1,2],["Paper","Min Time"])
    plt.ylabel("Normalized Makespan")
    plt.savefig("Plot_1_"+name+".png")
    plt.show()