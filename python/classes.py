class MyClass:
  def __init__(self):
    return
  def set_verbose(self,bool):
    if bool:
        def default_callback(data):
            print data
        self.callback = default_callback
    return
  def set_callback(self,callback):
    self.callback = str
    return
  def run(self,str):
    if hasattr(self, 'callback') and self.callback is not None:
        self.callback(str)
    return
  @staticmethod
  def staticm():
    print "static method!"
c = MyClass()
c.run('hi')
c.set_verbose(True)
c.run('verbosed')
c.callback = None
c.run('deleted')
MyClass.staticm()
