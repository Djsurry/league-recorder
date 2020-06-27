from subprocess import Popen, PIPE, STDOUT
from os import path, getcwd
import time, datetime
'''
#########

RUNNING FTP SERVICE. brew services stop pure-ftpd

#########
'''



record_cmd = 'ffmpeg -y -rtbufsize 100M -f gdigrab -framerate 30 -probesize 10M -draw_mouse 1 -i desktop -c:v libx264 -r 30 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p {out}'
compress_cmd = 'ffmpeg -i temp.mp4 -vcodec libx265 -crf 28 '



class Recorder:
    def __init__(self, folder):
        self.process = None
        self.path = folder

    def start(self):
        
        self.process = Popen(record_cmd.format(out=path.abspath(getcwd()) + "\\temp.mp4").split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def stop(self):
        name = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}.mp4"
        if self.process is not None:
            resp = self.process.communicate(input=b'q')
        else:
            return
        
        if not path.exists("temp.mp4"):
            print('Something went wrong - Recording failed')
            return
        p = Popen(compress_cmd.split().append('"' + self.path + '\\' + name + ".mp4" + '"'))
        p.communicate()
        if not path.exists(self.path + '\\' + name + '.mp4'):
            print("Something went wrong - Compression Failed")
            return
        p = Popen(['del', 'temp.mp4'])
        return self.out
            


