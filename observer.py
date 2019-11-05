class Observer:
  def __init__(self, feedback):
    self.feedback = feedback

  def update(self, flag, data):
    print(f'updated by a {flag} with {data}')
    self.feedback(flag, data)