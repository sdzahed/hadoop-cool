import sys
import math
import re
import os.path


mean = lambda a: sum(a) * 1.0/len(a)

def std_dev(data, mean_of_data):
     return math.sqrt(sum((x - mean_of_data) ** 2 for x in data) / len(data))

def parse_heat_readings(line):
    temps = []
    for t in re.findall('\d+,\d+', line):
        temps.append(int(t.split(',')[0]))
    return temps

def printlastline(trackers, outf):
    print '\n ############ Summary #############\n'
    for i in range(len(tracker_temps)):
        max_temp = max(tracker_temps[i])
        mean_temp = mean(tracker_temps[i])
        sdev_temp = std_dev(tracker_temps[i], mean_temp)
        print "%s ---> mean: %.2f, std dev: %.2f, max: %.2f" % (trackers[i], mean_temp, sdev_temp, max_temp)
        print >>outf, "%s %.2f %.2f %.2f" % (trackers[i], mean_temp, sdev_temp, max_temp)

def main():
    numlines = 0
    global tracker_temps
    dirname = os.path.split(sys.argv[1])[0]
    fname = os.path.split(sys.argv[1])[1]
    fin = open(sys.argv[1])
    fcluster = open(os.path.join(dirname, fname + '.cluster'), "w")
    ftrackers = open(os.path.join(dirname, fname + '.trackers'), "w")
    tracker_temps = {}
    trackers = [t.strip() for t in fin.readline().split()]
    for line in fin.readlines():
        numlines += 1
        temps = parse_heat_readings(line)
        if not temps:
            continue
        mean_temp = mean(temps)
        std_dev_temp = std_dev(temps, mean_temp)
        for idx, t in enumerate(temps):
            t = float(t)
            tracker_temps.setdefault(idx, []).append(t)
        print line + '  ----> [%.2f, %.2f]' % (mean_temp, std_dev_temp)
        print >>fcluster, '%.2f %.2f' % (mean_temp, std_dev_temp)
    printlastline(trackers, ftrackers)

if __name__ == '__main__':
    main()
