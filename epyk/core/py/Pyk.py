import importlib, subprocess, sys, os, inspect

class EpykMissingPykException(Exception):
  pass

class EpykBoundRptObj(Exception):
  pass


def requires(pyk_file, components=None, autoinstall=False):
  """
  Description:
    ------------

      This function will allow you to import components from another pyk file.
      The pyk file can be located on your file system, or it can be on pypi or even github
      if it's the latter options (pypi or github) you will need to use autoinstall=True

  Usage:
  -----------
    requires(pyk_name, autoinstall=True)

    requires('/usr/local/my_pyk_file.py', components=['obj1', 'obj2'])

  :param pyk_file: the pyk to be imported into your project, this will be a name if installing from pypi or github or just a path if it's a local pyk)
  :param components: list of objects to import, if None all the objects declared in the pyk file will be available
  :param autoinstall: specify whether we need to check github or pypi
  :return: a pyk object
  """

  pyk_obj = _Pyk.instance()
  pyk_obj._requires(pyk_file, components, autoinstall)

def exports(obj_dict):
  """
  Description:
  ------------

    This function requries you to pass a dictionary with the object alias as key and the object as value
    for as many objects as you wish
    This will then be used by users who need to require your particular pyk file
    You can pass epyk object in that dictionary as well as function if you need to

  Usage:
  ------

    exports({'my_obj1': my_obj1, 'my_obj1': my_obj2})

  :param obj__dict: dictionary with object name as key and object as value
  """
  pyk_obj = _Pyk.instance()
  pyk_obj._exports(obj_dict)

class _Pyk(object):
  """

  """
  __instance = None
  __pyk_dict = {}

  @staticmethod
  def instance():
    if _Pyk.__instance is None:
      _Pyk()
    return _Pyk.__instance

  def __init__(self):
    if _Pyk.__instance is not None:
      raise Exception("You need to call this object with the instance() method: _Pyk.instance()")

    _Pyk.__instance = self

  def register(self, rpt_obj):
    for obj_name, obj in inspect.getmembers(self):
      if obj_name.startswith('pyk_'):
        rpt_obj.context.register(obj)

  def _requires(self, pyk_file, components=None, autoinstall=False):
    """
    Description:
    ------------

      This function will allow you to import components from another pyk file.
      The pyk file can be located on your file system, or it can be on pypi or even github
      if it's the latter options (pypi or github) you will need to use autoinstall=True

    Usage:
    -----------
      requires(pyk_name, autoinstall=True)

      requires('/usr/local/my_pyk_file.py', components=['obj1', 'obj2'])

    :param pyk_file: the pyk to be imported into your project, this will be a name if installing from pypi or github or just a path if it's a local pyk)
    :param components: list of objects to import, if None all the objects declared in the pyk file will be available
    :param autoinstall: specify whether we need to check github or pypi
    :return: a pyk object
    """
    pyk_dict = _Pyk.__pyk_dict
    if pyk_file.endswith('.py'):
      path_split = pyk_file.split(os.sep)
      sys.path.append(os.sep.join(path_split[:-1]))
      importlib.import_module(path_split[-1].replace('.py', ''))
    else:
      try:
        importlib.import_module(pyk_file)
      except (ModuleNotFoundError, ImportError):
        if not autoinstall:
          print("The package is not found on your environment, you will need to install it manually or use the autoinstall argument")
          raise

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pyk_file])
        importlib.import_module((pyk_file))

    if pyk_file not in pyk_dict:
      raise EpykMissingPykException('The specified pyk file: %s does not call the exports function, if this is your file make sure to call this!' % pyk_file)

    if components:
      for component in components:
        comp_obj = pyk_dict[pyk_file][component]
        setattr(self, 'pyk_%s' % component, comp_obj)
    else:
      for obj_name, comp_obj in pyk_dict[pyk_file].items():
        setattr(self, 'pyk_%s' % obj_name, comp_obj)
    return self

  def _exports(self, obj_dict):
    """
    Description:
    ------------

      This function requries you to pass a dictionary with the object alias as key and the object as value
      for as many objects as you wish
      This will then be used by users who need to require your particular pyk file
      You can pass epyk object in that dictionary as well as function if you need to

    Usage:
    ------

        exports({'my_obj1': my_obj1, 'my_obj1': my_obj2})

    :param obj__dict: dictionary with object name as key and object as value
    """
    pyk_dict = _Pyk.__pyk_dict
    frame_found = False
    for frame in inspect.stack():
      if frame_found:
        filename = frame.filename
        break

      if frame.function == 'exports':
        frame_found = True
    pyk_dict[filename] = {}
    for obj_name, obj in obj_dict.items():
      pyk_dict[filename][obj_name] = obj

