from subprocess import Popen, PIPE, STDOUT
import time, datetime, pathlib, re
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
        print(self.path)

    def start(self):
        
        self.process = Popen(record_cmd.format(out=pathlib.Path.cwd() / "temp.mp4").split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def stop(self):
        
        pattern = re.compile(f"{datetime.datetime.now():%Y-%m-%d}" + r'_\d+.mp4')
        file_list = [n for n in self.path.iterdir() if pattern.match(n.name)]

        name = f"{datetime.datetime.now():%Y-%m-%d}" + f"_{len(file_list)+1}" ".mp4"
        if self.process is not None:
            resp = self.process.communicate(input=b'q')
        else:
            return
        
        if not pathlib.Path(pathlib.Path.cwd() / "temp.mp4").is_file():
            print('Something went wrong - Recording failed')
            return
        l = compress_cmd.split()
        
        l.append(f'{str(self.path / name)}')
        print(f"CMD: {l}")
        p = Popen(l)
        p.wait()
        if not pathlib.Path(self.path / name).is_file():
            print("Something went wrong - Compression Failed")
            return
        t = pathlib.Path.cwd() / 'temp.mp4'
        print(f'trying to delete {t}')
        pathlib.Path.unlink(t)
        return name
            
if __name__ == "__main__":
    r = Recorder("/Users/djsur/vods")
    r.start()
    time.sleep(2)
    r.stop()

