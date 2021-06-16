import itertools
import matplotlib.pyplot as plt
from boltons import iterutils
from statistics import mean
import numpy as np

def remove_space(i):
    d = i.split(' ')
    dat1 = d[:len(d)-2]
    return dat1

def calc_time(frec):
    time = [i/frec for i in range(180)]
    return time

def read_data(filename):
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    return lines

def get_data(filename):
    lines = read_data(filename)
    data = lines[5:]

    f = list(map(lambda x:remove_space(x),data))
    final_data = list(itertools.chain(*f))

    f = list(map(lambda x:float(x),final_data))
    set_info = iterutils.chunked(f, int(lines[0])*int(lines[1]))
    final_info = []
    for i in set_info:
        set_inf = iterutils.chunked(i, lines[1])
        final_info.append(set_inf)
    return final_info

def baseline_correction(final_info):
    baseline_correction = []
    for can in final_info:
        av = round(mean(can[0][:26]),4)
        baseline_correction.append(av)
    return baseline_correction

def media_per_canal(filename,final_info):
    lines = read_data(filename)
    result = np.zeros((8, 180))
    for i in final_info:
        result = [map(sum, zip(*t)) for t in zip(result, i)]

    ma = list(map(lambda x : list(map(lambda y: round(y/int(lines[2]),4) ,list(x))), result ))
    return ma

def create_trigger():
    time_triggerX = list(map(lambda x: x + 0.1, np.zeros(180)))
    time_triggerY = list(map(lambda x: x + 10, np.zeros(180)))
    time_triggerY[0] = -10
    return time_triggerX, time_triggerY


filename_Targets  = 'ep8chTargets.dat'
filename_NONTargets = 'ep8chNONTargets.dat'

final_info_Targets = get_data(filename_Targets)
final_info_NONTargets = get_data(filename_NONTargets)

print(final_info_NONTargets[415][7][179])
baseline_correction_Targets = baseline_correction(final_info_Targets)
baseline_correction_NONTargets = baseline_correction(final_info_NONTargets)

print('baseline_correction_Targets:' + str(baseline_correction_Targets))
print('baseline_correction_NONTargets:' + str(baseline_correction_NONTargets))


ma_Targets = media_per_canal(filename_Targets,final_info_Targets)
ma_NONTargets = media_per_canal(filename_NONTargets,final_info_NONTargets)

# scale x
frecventa = read_data('ep8chTargets.dat')[4]
time = calc_time(int(frecventa))

# create trigger
time_triggerX, time_triggerY = create_trigger()

figure, axes = plt.subplots(nrows=2, ncols=3,figsize = (14,8))
canal = 0
for i in range(2):
    for y in range(3):
        canal += 1
        axes[i][y].plot(time,ma_Targets[canal-1],color='blue')
        axes[i][y].plot(time,ma_NONTargets[canal-1], color='green')
        axes[i][y].plot(time_triggerX, time_triggerY, color='red')

        axes[i][y].set_xlabel('time[s]')
        axes[i][y].set_ylabel('[V]')
        axes[i][y].set_title('Canal' + str(canal))
        axes[i][y].set_ylim([-10,10])
        plt.figlegend(['ep8chTargets', 'ep8chNONTargets', 'trigger' ], loc='lower right', ncol=1, labelspacing=0.)
plt.show()