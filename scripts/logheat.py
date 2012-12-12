import sys
import os
import os.path
import subprocess
import getopt
import datetime
import time
import pdb

def usage():
    print "Usage: python logheat.py -m <hostsfile> -l <logfile>"

def parse_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hm:l:e:u:', ['help', 'machines=', 'log=', 'err=', 'user='])
    except getopt.GetoptError, err:
        dprintln(str(err))
        usage()
        sys.exit()

    options = {'machines': None, 'log': None, 'err': None, 'help': False, 'user': 'skhurasani'}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            options['help'] = True
        elif o in ('-l', '--logfile'):
            options['log'] = a
        elif o in ('-e', '--errfile'):
            options['err'] = a
        elif o in ('-m', '--machines'):
            options['machines'] = a
        elif o in ('-u', '--user'):
            options['user'] = a

    return options

def get_hosts(hosts_fpath):
    f = open(hosts_fpath)
    hosts = [h.strip() for h in f.readlines()]
    f.close()
    return hosts

def parse_temperatures(ipmi_output):
    temps = []
    for line in ipmi_output.split('\n'):
        if line.startswith('Temp'):
            temps.append(line.split('|')[1].strip().split()[0])
    return temps

def remote_command(cmdn, user, hosts, logpath, errpath, append=False):
    outf = open(logpath, 'w+')
    errf = open(errpath, 'w+')
    hostsline = ' ' * len(str(datetime.datetime.now())) + '  ' + ''.join([' %s' % h[:13] for h in hosts]) + '\n'
    outf.write(hostsline)
    while True:
        ts = datetime.datetime.now()
        outline = '%s: ' % ts
        for host in hosts:
            p = subprocess.Popen(['ssh', '-t', '-t',
                        '%s@%s' % (user, host), 'sudo',
                        '/usr/bin/ipmitool', 'sdr', 'list'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            temps = parse_temperatures(out)
            outline += '[%12s]' % ','.join(temps)
            if err:
                errf.write(err)
        outline += '\n'
        outf.write(outline)
        outf.flush()
        errf.flush()
        time.sleep(30)

def main():
    options = parse_args()
    if options['help']:
        sys.exit()
    print 'Options: ', str(options)
    hosts = get_hosts(options['machines'])
    print 'Hosts: ', str(hosts)
    cmd = 'sudo /usr/bin/ipmitool sdr list'
    remote_command(cmd, options['user'], hosts, options['log'], options['err'])

if __name__ == '__main__':
    main()
