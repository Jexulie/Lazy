import os, time, threading, re
from pprint import pprint as pp

# Observer Flags
#TODO Enum this
# 1 -> file-changed
# 2 -> file-created
# 3 -> file-removed

class Checker(threading.Thread):
  status = True
  filesToWatch = []

  def __init__(self, observer, watch, exclude):
    # self.path = path
    # self.options = options
    self.watch = watch
    self.exclude = exclude
    self.observer = observer
    
    threading.Thread.__init__(self)
    self.daemon = True

  # Observer Methods
  def notify(self, flag, msg):
    if flag == 1:
      self.observer.update(1, 'file-changed')
    elif flag == 2:
      self.observer.update(2, 'file-created')
    elif flag == 3:
      self.observer.update(3, 'file-removed')

  def extractExtension(self, path):
    matched = re.match(r'^(.*)\.(.*)$', path)
    ext = matched.group(2)
    if ext is None:
      raise Exception
    else:
      return ext

  def checkFileExtException(self, path):
    ext = self.extractExtension(path)
    if ext in self.exclude['ext']:
      return True

    return False

  def checkDirExeption(self, directory):
    if directory in self.exclude['dir']:
      return True

    return False

  def checkFileRemoval(self, nameList):
    temp = []
    for file in self.filesToWatch:
      if file['name'] in nameList:
        temp.append(file)
      else:
        name = file['name']
        self.notify(3, f'{name} file has removed.')
    
    self.filesToWatch = temp
      

  def checkFileCreated(self, name, size):
    if name not in [file['name'] for file in self.filesToWatch]:
      f = {'name': name, 'size': size}
      self.notify(2, f'{name} file has created.')
      self.filesToWatch.append(f)

  def checkFileChanged(self, name, size):
    # check File Size
    for file in self.filesToWatch:
      if file['name'] == name:
        if file['size'] != size:
          self.notify(1, f'{name} file has changed.')
          file['size'] = size

  def walkFiles(self):
    filesToCheck = []
    for root, dirs, files in os.walk(self.watch['dir'], topdown=True):
      # print(root, dirs, files)

      if self.checkDirExeption(dirs):
        continue

      for name in files:
        filePath = root + '/' + name
        fileSize = os.stat(filePath).st_size

        if self.checkFileExtException(filePath):
          continue

        filesToCheck.append(filePath)
        
        # Check if a file created
        self.checkFileCreated(filePath, fileSize)
        # Check if a file changed
        self.checkFileChanged(filePath, fileSize)
    
    if len(filesToCheck) != len(self.filesToWatch):
      # Check if a file removed
      self.checkFileRemoval(filesToCheck)
        


  def stopChecker(self):
    self.status = False

  def run(self):
    print('checker has started')

    while self.status:
      time.sleep(.25)
      self.walkFiles()

      # pp(self.filesToWatch)
      # print('\n')