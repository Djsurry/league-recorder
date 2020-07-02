from transfer import transfer
from record_screen import Recorder
from status import in_game, league_open
import sys, pathlib, time, threading

log = ".vodlogger"
def parseargs(args):
	if len(args) < 1 or len(args) > 10:
		print('[0x01]: Incorrect usage. Use -h for help')
		exit(1)

	if '-h' in args:
		print('Usage: python main.py <path to vods foler>')
		print('Options:')
		print('        -r <ign> <region>: enables recording and saving of only ranked games')
		print('        -s <host> <user> <pswd> <path to remote folder>: enables syncing')
		exit(0)

	if '-' in args[0]:
		print('[0x02]: Incorrect usage. Use -h for help')
		exit(1)

	arg_dict = {'path': pathlib.Path(args[0])}

	if len(args) > 1:
		if '-' not in args[1]:
			 print('[0x03]: Incorrect usage. Use -h for help')
			 exit(1)

	arg_dict['ranked'] = '-r' in args
	if arg_dict['ranked']:
		index = args.index('-r')
		try:
			if '-' not in args[index+1]:
				arg_dict['ign'] = args[index+1]
			else:
				print('[0x04]: Incorrect usage. Use -h for help')
				exit(1)
			if '-' not in args[index+2]:
				arg_dict['region'] = args[index+2]
			else:
				print('[0x05]: Incorrect usage. Use -h for help')
				exit(1)
		except IndexError:
			print('[0x06]: Incorrect usage. Use -h for help')
			exit(1)

	arg_dict['syncing'] = '-s' in args
	if '-s' in args:
		index = args.index('-s')
		try:
			arg_dict['host'] = args[index + 1]
			arg_dict['user'] = args[index + 2]
			arg_dict['password'] = args[index + 3]
			arg_dict['remote'] = args[index + 4]
			if '-' in args[index + 1] or '-' in args[index + 2] or '-' in args[index + 3] or '-' in args[index + 4]:
				print('[0x07]: Incorrect usage. Use -h for help')
				exit(1)
		except IndexError:
			print('[0x08]: Incorrect usage. Use -h for help')
			exit(1)	
	
	return arg_dict


class Syncer(threading.Thread):
	def __init__(self, path, dest, host, user, pswd, s):
		super().__init__()
		self.path = path
		self.dest = dest
		self.host = host
		self.user = user
		self.pswd = pswd
		self.sent_files = s
		print(s)
		self.running = True
	def run(self):
		while self.running:
			all_files = [n for n in self.path.iterdir() if n.name != log]
			print(f"all: {all_files}")
			for f in all_files:
				if f in self.sent_files:
					continue
				print(f"sending {f}")
				if transfer(self.dest, f,  self.user, self.pswd, self.host) == 0:
					self.sent_files.append(f)
			time.sleep(2)
		print(self.sent_files)
		with open(self.path / log, 'w') as f:
			f.write('\n'.join([str(n) for n in self.sent_files if n != '']))

	def stop(self):
		self.running = False


def init(path):
	if path.exists() and not path.is_dir():
		print(f"[0x09]: {f} is not a directory")
		exit(1)
	elif not path.exists():
		if input(f"Do you want to create {path}? (y or n)").lower() == "y":
			path.mkdir(parents=True)
	log_file = path / log
	if log_file.exists():
		with open(log_file) as f:
			lines = f.read()
			return [pathlib.Path(n) for n in lines.split('\n')]
	else:
		log_file.touch()
		return []
	


def loop(args):
	r = Recorder(args['path'])
	ig = False
	while True:
		time.sleep(2)
		if not ig:		
			if not league_open():
				continue
			if args['ranked']:
				if in_game(args['ign']):
					r.start()
					ig = True
			r.start()
			ig = True
		else:
			if not league_open():
				f = r.stop()
				ig = False

if __name__ == "__main__":

	args = parseargs(sys.argv[1:])
	s = init(args['path'])
	f = None
	if args['syncing']:
		f = Syncer(args['path'], args['remote'], args['host'], args['user'], args['password'],s)
		f.start()

	try:
		loop(args)
	except KeyboardInterrupt:
		if f is not None:
			f.stop()
			f.join()
	


