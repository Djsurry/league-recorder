from transfer import transfer
from record_screen import Recorder
from status import in_game, league_open
import sys, pathlib, time, threading


def parseargs(args):
	if len(args) < 1 or len(args) > 10:
		print('[0x01]: Incorrect usage. Use -h for help')
		exit(1)

	if '-h' in args:
		print('Usage: python recorder.py <path to vods foler>')
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


def handle_sync(path, dest, host, user, pswd):
	sent_files = []
	while True:
		all_files = [n for n in path.iterdir()]
		print(all_files)
		for f in all_files:
			if f in sent_files:
				continue
			if transfer(dest, f, user, pswd, host=host) == 0:
				sent_files.append(f)
		time.sleep(2)


def loop():

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
				print("LEAGUE CLOSED")
				f = r.stop()
				print("FINISHED r.stop()")
				ig = False

if __name__ == "__main__":
	args = parseargs(sys.argv[1:])
	#if args['syncing']:
	#	t = threading.Thread(target=handle_sync, args=(args['path'], args['remote'], args['host'], args['user'], args['password'],), daemon=True)
	#	t.start()
	#loop()
	handle_sync(args['path'], args['remote'], args['host'], args['user'], args['password'])



