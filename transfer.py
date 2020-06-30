
from subprocess import Popen, PIPE, STDOUT
def transfer(dest, f, user, passw, host='192.168.2.83'):
	p = Popen(f'scp {f} {user}@{host}:{dest}'.split() , stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	data, err = p.communicate(input=f"{passw}".encode('utf-8'))
	p.wait()
	return p.returncode


