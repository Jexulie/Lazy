import subprocess
import threading
import time
# observer flags
# 6 -> spawner-init
# 7 -> spawner-process
# 8 -> spawner-killed

class Spawner(threading.Thread):
  def __init__(self, observer, cmd):
    self.cmd = cmd
    self.observer = observer
    self.sp = None

    threading.Thread.__init__(self)
    self.daemon = True

  # Observer Methods
  def notify(self, flag, msg):
    if flag == 6:
      self.observer.update(6, 'spawner-init')
    elif flag == 7:
      self.observer.update(7, 'spawner-process')

  def terminate(self):
    self.sp.terminate()
    self.sp.wait()
    print('subprocess terminated')

  def run(self):
    print('spawner has started')
    self.sp = subprocess.Popen(self.cmd)  
