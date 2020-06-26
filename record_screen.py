from subprocess import Popen, PIPE, STDOUT
from os import path
import time
'''
#########

RUNNING FTP SERVICE. brew services stop pure-ftpd

#########
'''



record_cmd = 'ffmpeg -f gdigrab -framerate 10 -i desktop {out}'
compress_cmd = 'ffmpeg -i {inp} -vcodec libx265 -crf 28 {out}'



class Recorder:
    def __init__(self, folder):
        self.process = None
        self.path = folder

    def start(self, out):
        self.out = out
        self.process = Popen(record_cmd.format(out="temp.mp4").split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def stop(self):
        if self.process is not None:
            resp = self.process.communicate(input=b'q')
        else
            return
        
        if not path.exists("temp.mp4"):
            print('Something went wrong - Recording failed')
            return
        p = Popen(compress_cmd.format(out=folder + self.out, inp="temp.mp4").split())
        p.communicate()
        if not path.exists(folder + self.out):
            print("Something went wrong - Compression Failed")
            return

        return self.out
            


