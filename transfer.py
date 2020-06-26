from ftplib import FTP
from subprocess import Popen, PIPE, STDOUT

def transfer(dest, f, host, user, passw):
	p = Popen(f'scp {f} user@192.168.2.83:{dest}'.split() , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	data, err = p.communicate(input=b"W0rd cr1m35")
	return data, err


