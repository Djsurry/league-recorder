from subprocess import Popen, PIPE, STDOUT
import time, datetime, pathlib
'''
#########

RUNNING FTP SERVICE. brew services stop pure-ftpd

#########
'''



record_cmd = 'ffmpeg -y -rtbufsize 100M -f gdigrab -framerate 30 -probesize 10M -draw_mouse 1 -i desktop -c:v libx264 -r 30 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p {out}'
compress_cmd = 'ffmpeg -i temp.mp4 -vcodec libx265 -crf 28'



class Recorder:
    def __init__(self, folder):
        self.process = None
        self.path = pathlib.Path(folder)
        

    def start(self):
        
        self.process = Popen(record_cmd.format(out=pathlib.Path.cwd() / "temp.mp4").split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def stop(self):
        name = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}.mp4"
        if self.process is not None:
            resp = self.process.communicate(input=b'q')
        else:
            return
        
        if not pathlib.Path(pathlib.Path.cwd() / "temp.mp4").is_file():
            print('Something went wrong - Recording failed')
            return
        l = compress_cmd.split()

        l.append(f'"{str(self.path / name)}"')
        
        p = Popen(l)
        p.communicate()
        if not pathlib.Path(self.path / name).is_file():
            print("Something went wrong - Compression Failed")
            return
        p = Popen(['del', 'temp.mp4'])
        return name
            


