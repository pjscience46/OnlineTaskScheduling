import matplotlib.pyplot as plt
import csv
from statistics import*

## DON'T CHANGE BETWEEN THE LINE
#######################################################################################################################

name_list = ["Amdahl","Communication","General","Roofline"]
p_list = [500,1000,1500,2000,2500,3000,3500,4000,4500,5000]
mu_list = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28,0.3,0.32,0.34,0.36,0.38]
n_list = [100,200,300,400,500,600,700,800,900,1000]

for name in name_list :
    Paper = [[] for i in range(19)]
    Min_time = [[] for i in range(19)]
    f = open(name+"/all.csv",newline='')
    reader = csv.reader(f)
    for row in reader :
        if row[0] != "mu" :
            if row[0] == "0.02" :
                index = 0
            if row[0] == "0.04" :
                index = 1
            if row[0] == "0.06" :
                index = 2
            if row[0] == "0.08" :
                index = 3
            if row[0] == "0.1" :
                index = 4
            if row[0] == "0.12" :
                index = 5
            if row[0] == "0.14" :
                index = 6
            if row[0] == "0.16" :
                index = 7
            if row[0] == "0.18" :
                index = 8
            if row[0] == "0.2" :
                index = 9
            if row[0] == "0.22" :
                index = 10
            if row[0] == "0.24" :
                index = 11
            if row[0] == "0.26" :
                index = 12
            if row[0] == "0.28" :
                index = 13
            if row[0] == "0.3" :
                index = 14
            if row[0] == "0.32" :
                index = 15
            if row[0] == "0.34" :
                index = 16
            if row[0] == "0.36" :
                index = 17
            if row[0] == "0.38" :
                index = 18

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
        if k == 0.04 :
            index = 1
        if k == 0.06 :
            index = 2
        if k == 0.08 :
            index = 3
        if k == 0.1 :
            index = 4
        if k == 0.12 :
            index = 5
        if k == 0.14 :
            index = 6
        if k == 0.16 :
            index = 7
        if k == 0.18 :
            index = 8
        if k == 0.2 :
            index = 9
        if k == 0.22:
            index = 10
        if k == 0.24 :
            index = 11
        if k == 0.26 :
            index = 12
        if k == 0.28 :
            index = 13
        if k == 0.3 :
            index = 14
        if k == 0.32 :
            index = 15
        if k == 0.34 :
            index = 16
        if k == 0.36 :
            index = 17
        if k == 0.28 :
            index = 18

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