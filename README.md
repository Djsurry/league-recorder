# league-recorder
Records league and synchs files with a remote machine, so I can watch vods in bed on my laptop

usage:

python main.py </path/to/vods_folder>

Options:
- `-s <host> <user> <password> <destination path>`: Enable synching with remote `user@host`, saving files to the destination path with scp.
- `-n`: By default, this only saves ranked games, this flag enables recording norms games.
