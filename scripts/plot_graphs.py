import os.path
import subprocess

gnuplot_cmd = '''
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xtics rotate out
set xlabel "Trackers"

#set size 1.0, 0.6
set terminal png

set title "Average Temperatures Recorded at Each Tracker"
set ylabel "Avg Temperature (degrees)"
set output "{avg_out}.png"
plot    "{trackers_on}" using 2:xticlabels(1) title 'Cool Scheduling ON' with linespoints, \
        "{trackers_off}" using 2 title 'Cool Scheduling Off' with linespoints

set title "Std Deviation of Temperatures Recorded at Each Tracker"
set ylabel "Std Dev Temperature (degrees)"
set output "{std_out}.png"
plot    "{trackers_on}" using 3:xticlabels(1) title 'Cool Scheduling ON' with linespoints, \
        "{trackers_off}" using 3 title 'Cool Scheduling Off' with linespoints

set title "Maximum Temperatures Recorded at Each Tracker"
set ylabel "Max Temperature (degrees)"
set output "{max_out}.png"
plot    "{trackers_on}" using 4:xticlabels(1) title 'Cool Scheduling ON' with linespoints, \
        "{trackers_off}" using 4 title 'Cool Scheduling Off' with linespoints
'''

def plot():
    curdir = os.path.abspath(os.curdir)
    ondir = os.path.join(curdir, 'on')
    offdir = os.path.join(curdir, 'off')
    plotsdir = os.path.join(curdir, 'plots')
    plotf = open('gnuplot.in', "w")
    for size in ('200', '100', '50', '25', '10', '5'):
        plotf.truncate()
        cmdstring = gnuplot_cmd.format(avg_out=os.path.join(plotsdir, 'trackers_avg_%s' % size),
                                    std_out=os.path.join(plotsdir, 'trackers_std_%s' % size),
                                    max_out=os.path.join(plotsdir, 'trackers_max_%s' % size),
                                    trackers_on=os.path.join(ondir, 'terasort_%sgb.on.out.trackers' % size),
                                    trackers_off=os.path.join(offdir, 'terasort_%sgb.off.out.trackers' % size))
        plotf.write(cmdstring)
        plotf.flush()
        if subprocess.call(['gnuplot','-e', 'load "gnuplot.in"']) != 0:
            print "ERROR on: %s" % cmdstring

if __name__ == '__main__':
    plot()
