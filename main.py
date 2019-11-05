from checker import Checker
from spawner import Spawner
from observer import Observer
from pynput.keyboard import Key, Listener
import time, threading, logging


class Lazy:

  observer = None
  checker = None
  spawner = None

  lock = threading.Lock()

  def __init__(self):
    self.args = {
      #TODO split cmd after getting CLI args
      'cmd': ['python', './test/lazyloop.test.py'],
      'path': './test',
      'options': None
    }

  def feedback(self, flag, data):
    print(f'Feedback from {flag}')
    if flag == 1 or flag == 2 or flag == 3:
      self.restartSpawner()
    # if flag == 7:
    #   self.spawnerProcess = data
    # with self.lock:
    #   print('Spawner aquired Lock')
    # if flag == 1 or flag == 2 or flag == 3:
    #   if self.spawnerProcess is not None:
    #     self.terminateSpawner()


  def handlePath(self):
    pass

  def factoryObserver(self):
    return Observer(self.feedback)

  def factorySpawner(self, observer, cmd):
    return Spawner(observer, cmd)

  def factoryChecker(self, observer, path, options):
    return Checker(observer, path, options)

  def killChecker(self):
    # self.checker.join()
    self.spawner.running = False
    print('Checker Terminated')

  def killSpawner(self):
    self.spawner.terminate()
    print('Spawner Terminated')

  def restartSpawner(self):
    self.killSpawner()
    self.spawner.run()
    print('Spawner Restarted')

  def createNewInstance(self):
    self.observer = self.factoryObserver()
    self.spawner = self.factorySpawner(self.observer, self.args['cmd'])
    self.checker = self.factoryChecker(self.observer, self.args['path'], self.args['options'])

  def pressEvent(self, key):
    print(key)
    if key == 'r':
      print('pressed reset')
      self.restartSpawner()

  def releaseEvent(self, key):
    print(key)
    if key == 'r':
      print('released reset')
      self.restartSpawner()


  def startEventLoop(self):
    with Listener(on_press=self.pressEvent, on_release=self.releaseEvent) as listener:
      listener.join()


  def start(self):
    self.createNewInstance()
    self.checker.start()
    self.spawner.start()
    print('Process Started...')
    self.startEventLoop()

if __name__ == "__main__":
  # Parse CLI ARGs
  # start checker thread
  # start spawner thread
  # listen for keyboard presses & execute

  # get relative path or ...
  newInstance = Lazy()

  newInstance.start()