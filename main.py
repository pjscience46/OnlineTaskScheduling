# main
from processors import*
from utils import*
from statistics import*
import matplotlib.pyplot as plt


# compute_and_save('regular','Results_V3/Regular/',1)
# compute_and_save('density','Results_V3/Density/',1)
# compute_and_save('Fat','Results_V3/Fat/',1)
# compute_and_save('jump','Results_V3/Jump/',1)
# compute_and_save('n','Results_V3/n/',1)
# compute_and_save('p','Results_V3/P/',1)

# display_results('regular','Results_V3/Regular/')
# display_results('density','Results_V3/Density/')
# display_results('Fat','Results_V3/Fat/')
# display_results('jump','Results_V3/Jump/')
# display_results('n','Results_V3/n/')
# display_results('p','Results_V3/P/')


#display_multiple_results("V2","V3","Density","Merging_V2_and_V3")
#display_multiple_results("V2","V3","Fat","Merging_V2_and_V3")
#display_multiple_results("V2","V3","Jump","Merging_V2_and_V3")
#display_multiple_results("V2","V3","n","Merging_V2_and_V3")
#display_multiple_results("V2","V3","p","Merging_V2_and_V3")
#display_multiple_results("V2","V3","Regular","Merging_V2_and_V3")

display_results_boxplot("V2","V3","Merging_V2_and_V3")
