import os
# I know os.system() is worse than Popen(), but Popen() wasn't working (something with the path to the windows file)
def transfer(dest, f, user, passw, host):
	cmd = f'pscp -pw "{passw}" {f} {user}@{host}:{dest}'
	return os.system(cmd)

