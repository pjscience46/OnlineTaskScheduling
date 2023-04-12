# The title of this doc is rather self-explanatory

_I will not explain the details of how these algorithms work, but will only cover their
usage. If you have any further questions, please feel free to contact me at 
thomas.verrecchia@outlook.com._

- All the tasks graph you may need are precomputed and stored in the directory "DAGGEN",
the task list are in the directory "TASKS". 
- You will only need two functions wich are written in the "utils.py" files :
compute_and_save() and display_results(). 
  - The compute_and_save() function takes three arguments: the parameter you want to 
  vary (can be fat, density, regular, p, or n), the path to the directory where it will
  save the results, and the number of instances you want to run for each set of 
  parameters. The result directory must contain four subdirectories named 
  "Amdahl", "Communication", "General", and "Roofline". An example can be 
  found in the "Results_V1" directory. The number of instances must be between 
  1 and 30. This function will save the results in files called "all.csv" in the 
  subdirectories, containing all the results for each instance and each set of 
  parameters.
  - The display_results() function takes two arguments: 
  the parameter you want to vary and the path to the directory where the results 
  of compute_and_save() were saved. It will compute the mean value for each speedup 
  model and each set of parameters in four files called "mean.csv". It will then 
  display and save the figures.

The process is straightforward: you only need to copy and adapt these two lines 
of code in the main:

    compute_and_save('jump','Results_DAGGEN/WEEK 7/test/',1)

    display_results('jump','Results_DAGGEN/WEEK 7/test/')

if you want to modify the figures, you can either build a code from the ground up using
the "mean.csv" files previously saved or modify the last part of the
"display_results()" code. 