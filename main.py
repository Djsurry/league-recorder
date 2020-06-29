from transfer import transfer
from record_screen import Recorder
from status import in_game, league_open
import sys, pathlib, time

# TODO
#     1. Check return code of scp to check sucess or not
#     2. Add second thread running to send vods


def parseargs(args):
	if len(args) < 1 or len(args) > 9:
		print('[0x01]: Incorrect usage. Use -h for help')
		exit(1)

	if '-h' in args:
		print('Usage: python recorder.py <path to vods foler>')
		print('Options:')
		print('        -r <ign>: enables recording and saving of only ranked games')
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
		except IndexError:
			print('[0x05]: Incorrect usage. Use -h for help')
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
				print('[0x06]: Incorrect usage. Use -h for help')
				exit(1)
		except IndexError:
			print('[0x07]: Incorrect usage. Use -h for help')
			exit(1)	
	
	return arg_dict

args = parseargs(sys.argv[1:])

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
			if not league:
				f = r.stop()
				if args['syncing']:
					transfer(args['remote'], f, args['host'], args['user'], args['password'])

if __name__ == "__main__":
	print(args)




