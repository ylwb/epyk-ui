"""
Module dedicated to create CSS Styles

https://www.w3schools.com/Jsref/dom_obj_style.asp
"""

import os

from epyk.core.css.styles import CssStyle
from epyk.core.css import Color
from epyk.core.css import CssInternal
from epyk.core.css import Defaults


class CssDefaults(object):
  font = Defaults.Font


class Css(object):
  """
  CSS Object is the main Python wrapper used to create the on the fly CSS files
  The idea will be to use this as the bespoke CSS file in a report. There will be nothing done outside of python in this
  framework. Everything like CSS or Javascript will be automatically generated and defined from the components used in the reports.

  https://www.w3schools.com/Jsref/dom_obj_style.asp
  https://en.wikipedia.org/wiki/Minification_(programming)
  """

  class __internal(object):
    """
    Internal context for all the object created not in the framework context.
    This will ensure the process will still work.
    """
    _props = {}

  def __init__(self, report=None):
    self.rptObj = report if report is not None else self.__internal()
    if not 'css' in self.rptObj._props:
      self.rptObj._props['css'] = {}
    self.cssStyles, self._cssOvr, self._cssEventOvr, self.cssAttrs, self._cssCls = {}, {}, {}, {}, []
    self._colors = None

  @property
  def colors(self):
    """
    CSS Colors category

    This will provide an interface to deal with colors in Python and Javascript in a simple manner.
    This will provide an object with different methods to play with colors.

    Colors and themes can be changed directly in the report run time

    For changing the colors you can use the below function

    for adding a bespoke theme to the framework you can use the CLI command:

    Example
    >>> Css().colors.get('success', 0)
    '#e8f2ef'

    :return: A Python ColorMaker object
    :rtype: epyk.Lib.css.Color.ColorMaker
    """
    if self._colors is None:
      self._colors = Color.ColorMaker(self.rptObj)
    return self._colors

  @property
  def defaults(self):
    return CssDefaults

  def append(self, clsNames):
    """
    Add CSS Class Names to the CSS Object attached to a component.

    Example
    cssObj.append(['class2', 'class1'])

    :param clsNames: The Python list of classNames

    :rtype: Css
    :return: The Python CSS Object
    """
    if not isinstance(clsNames, list):
      clsNames = [clsNames]
    for cls in clsNames:
      clsObj = CssStyle.getCssObj(cls, theme=self.colors._themeObj.name)
      if clsObj is not None:
        self.cssStyles[clsObj.classname] = clsObj
      else:
        self._cssCls.append(cls)
    return self

  @property
  def internal(self):
    """
    CSS System Definition

    THis property will return the pre defined CSS Style and Themes in the framework.
    This will return the classes themselves to any changes there will impact the entire framework.

    This is a simple and quick hook to apply override and make the environment very specific

    :return:
    """
    return CssInternal

  def cssCls(self, clsName, attrs=None, event_attrs=None, global_scope=False):
    """
    Add a bespoke class to the CSS Style Factory. This class is added on the fly and it cannot override an existing one.

    Example
    cssObj.cssCls("CssDivChart", {"color": 'yellow'})
    cssObj.cssCls('css-class') # add a valid CSS class from the external packages
    self.style.cssCls('CssButtonBasic', {'color': color}, {"hover": {"background-color": 'None', "color": "None"}})

    :param clsName: A Python Class or a String with a className
    :param attrs: The Python definition of the CSS Class (a dictionary)
    :param event_attrs: The Python definition of the CSS Class (a dictionary of dictionary)
    :param global_scope:

    :return: The Python Class definition in the factory
    """
    if isinstance(clsName, str):
      fCls = CssStyle.getCssObj(clsName, theme=self.colors._themeObj.name)
      if fCls is not None:
        if global_scope:
          fCls.css(attrs, eventAttrs=event_attrs)
        else:
          self._cssOvr[clsName] = attrs
          if event_attrs is not None:
            self._cssEventOvr.setdefault(clsName, {}).update(event_attrs)
        # Add the class to the list of defined classes in the final CSS section in the page
        self.add(clsName)
      elif fCls is None and (attrs is not None or event_attrs is not None):
        cls_virtual = type(clsName, (CssStyle.CssCls,), {})()
        cls_virtual.style.update(attrs)
        cls_virtual.name = CssStyle.cssName(clsName)
        if event_attrs is not None:
          for k, v in event_attrs.items():
            cls_virtual.eventsStyles[k] = event_attrs[k]
        if global_scope:
          CssStyle.setCssObj(CssStyle.cssName(clsName), cls_virtual, self.rptObj, theme=self.colors._themeObj.selected)
        else:
          self.cssStyles[clsName] = cls_virtual
      else:
        self._cssCls.append(clsName)
    else:
      cssCls = type(clsName.__name__, (clsName, CssStyle.CssCls), {})
      if not clsName.__name__ in CssStyle.load():
        CssStyle.load()[clsName.__name__] = {'class': cssCls, 'file': 'external (%s)' % self.rptObj.user}
      self.add(clsName.__name__)
    return self

  def cssDerivCls(self, htmlId, clsName, attrs=None, event_attrs=None, force_reload=False):
    """
    CSS Functions

    Create a new CSS definition based on an existing one.

    Examples
    textObj.style.cssCls("CssText", {"text-decoration": 'underlying'}, eventAttrs={"hover": {"color": "black !important", "cursor": "pointer"}})

    :param htmlId: The htmlCode of this event
    :param clsName: The original classname
    :param attrs: Optional, The CSS attributes
    :param event_attrs: Optional, The event CSS attributes
    :param force_reload: Optional, Force the CSS factory to attached this object

    :return: The CSS Class
    :rtype: epyk.Lib.css.styles.CssStyle.CssCls
    """
    fCls = CssStyle.getCssObj(clsName, theme=self.colors._themeObj.name)
    derv_cls_name = CssStyle.cssName("%s_%s" % (clsName, htmlId))
    if fCls is not None:
      dervfCls = fCls.clone(derv_cls_name)
    else:
      dervfCls = type(derv_cls_name, (CssStyle.CssCls,), {})
    drvClsObj = dervfCls(theme=self.colors._themeObj.name)
    drvClsObj.style.update(attrs)
    if fCls is not None:
      for k, v in fCls.eventsStyles.items():
        drvClsObj.eventsStyles[k] = dict(fCls.eventsStyles[k])
    if event_attrs is not None:
      for k, v in event_attrs.items():
        if k in drvClsObj.eventsStyles:
          drvClsObj.eventsStyles[k].update(event_attrs[k])
        else:
          drvClsObj.eventsStyles[k] = event_attrs[k]
    CssStyle.setCssObj(derv_cls_name, drvClsObj, self.rptObj, theme=self.colors._themeObj.selected, force_reload=force_reload)
    return drvClsObj

  def custom(self, clsName, attrs, event_attrs=None):
    """
    Bespoke CSS Definition

    This will allow you to create your own CSS classes from Python dictionaries and they
    to use it in the different HTML object.

    More details on the CSS
    https://www.w3schools.com/css/

    :param clsName: A CSS Python class Name as a String
    :param attrs: A dictionary with the CSS parameters to be overridden
    :param event_attrs: A python dictionary with the event types and the attributes to be set / overriddenn

    :return: The Python CSS Object
    """
    self.cssStyles[clsName] = type(clsName, (CssStyle.CssCls,), {})
    self.cssStyles[clsName].attrs = attrs
    self.cssStyles[clsName].name = clsName
    self.cssStyles[clsName].eventAttrs = event_attrs
    for cssId, cssDef in self.cssStyles[clsName]().getStyles().items():
      self.rptObj._props['css'][cssId] = cssDef
    return self

  def reload(self):
    """
    Force the CSS Classes cache to be refreshed.
    This should never be used locally as a simple change in the code will refresh all the caches as Flask / Django will automatically restart

    :return: The Python CSS Object
    """
    CssStyle.load(reset=True)
    return self

  def get(self, clsName):
    """
    Get from the factory an object defining a CSS class

    :param clsName: A CSS Python class Name as a String

    :return: A CSS Class Python object
    :rtype: CssStyle.CssCls
    """
    return CssStyle.getCssObj(clsName, self.rptObj, theme=self.colors._themeObj.name)

  def add(self, className, cssRef=None, htmlId=None):
    """

    :param className:
    :param cssRef:
    :param htmlId:

    :return:
    """
    clsObj = self.get(className)
    if cssRef is not None:
      clsObj.setId({'reference': cssRef})
    elif htmlId is not None:
      clsObj.setId({'reference': "#%s" % htmlId})
    self.cssStyles[clsObj.classname] = clsObj
    return clsObj

  def css(self, key, value=None):
    """
    Set the CSS Attributes to a HTML component.
    This function is similar to the Jquery css function and it will accept any CSS Style defined by W3C.

    Documentation
    https://www.w3schools.com/css/

    Example
    cssObj.css('color', 'red')
    cssObj.css({'color': 'red'})

    #TODO: Add the CSS attributes to the component

    :param key: The CSS Key definition or a dictionary with all the CSS definition
    :param value: The CSS Value defined for a given attribute key (optional if key is a dictionary)
    :rtype: Css

    :return: The Python CSS Object
    """
    pixelCats = set(['font-size', 'width', 'height'])
    cssVals = key if value is None and isinstance(key, dict) else {key: value}
    for k, v in cssVals.items():
      if isinstance(v, str):
        self.cssAttrs[k] = v
      elif v is not None:
        if k in pixelCats and isinstance(v, int):
          v = "%spx" % v
        self.cssAttrs[k] = v
    return self

  def clear(self, clsNames=None):
    """
    Remove from the object a list (or all) the predefined styles

    Example
    cssObj.clear(['class2'])
    cssObj.clear()

    :param clsNames: The Python CSS class Name

    :return: The CSS Python Object
    """
    if clsNames is None: # Remove all the styles for the object
      self.cssStyles, self._cssOvr, self._cssEventOvr, self._cssCls = {}, {}, {}, []
      return self

    if not isinstance(clsNames, list):
      clsNames = [clsNames]
    for clsName in clsNames:
      if clsName in self.cssStyles:
        del self.cssStyles[clsName]
      if clsName in self._cssOvr:
        del self._cssOvr[clsName]
      if clsName in self._cssEventOvr:
        del self._cssEventOvr[clsName]
      if clsName in self._cssCls:
        self._cssCls.remove(clsName)
    return self

  def cssName(self, name):
    """
    CSS Class name

    This will return the translated CSS classname used in the framework.
    In order to avoid conflicts classnames are prefixed with a py_ and they are put in lower cases.

    :param name: The original classname

    :return: A String with the internal classname used
    """
    return CssStyle.cssName(name)

  def getClsTag(self, clsNames=None):
    """
    HTML tags

    Create the CSS Tag to be added to the HTML Element to consider the different classes.
    This will only add a class tag with the list of class names defined.

    Example
    >>> Css().css('color', 'red').getClsTag()
    'style="color:red"'

    >>> Css().getClsTag(['class1'])
    'class="py_class1"'

    :param clsNames: Optional. A list of classNames

    :return: A string with the HTML Class information to add to the element
    """
    if len(self.cssAttrs) > 0 and clsNames is None:
      return 'style="%s"' % ";".join(["%s:%s" % (k, v) for k, v in self.cssAttrs.items()])

    return 'class="%s"' % " ".join([CssStyle.cssName(clsName) for clsName in clsNames])

  def toHtml(self, clsNames=None):
    """
    HTML tags

    Create the CSS Tag to be added to the HTML Element to consider the different classes.
    This will only add a class tag with the list of class names defined.

    Example:
    cssObj.toHtml("CssBillboardTitle")

    :param clsNames: A list or a String for the scope of CSS classname to use

    :return: A String used to add the references to the CSS classnames
    """
    html_tags = {'class': '', 'style': ''}
    if clsNames is not None and not isinstance(clsNames, list):
      clsNames = [clsNames]
    if clsNames is None:
      html_tags['class'] = " ".join([clsObj.classname for clsObj in self.cssStyles.values()])
    else:
      html_tags['class'] = " ".join([clsObj.classname for clsObj in self.cssStyles.values() if clsObj.__class__.__name__ in clsNames])
    if len(self._cssCls) > 0:
      html_tags['class'] = " ".join([" ".join(self._cssCls), html_tags['class']]).strip()
    html_tags['style'] = ";".join(["%s:%s" % (k, v) for k, v in self.cssAttrs.items()])
    for clsName, clsObj in self.cssStyles.items():
      if clsObj.__class__.__name__ in self._cssOvr:
        clsObj.css(self._cssOvr[clsObj.__class__.__name__], eventAttrs=self._cssEventOvr.get(clsObj.__class__.__name__, {}))
      for cssId, cssDef in clsObj.getStyles().items():
        self.rptObj._props['css'][cssId] = cssDef
    return html_tags

  def getStyles(self, to_str=False):
    """
    CSS Style Builder.

    This will take into account all the overrides.

    :param to_str: Optional. Flag to convert the CSS style to a valid CSS string object. Default False

    :return: A python dictionary with all the styles
    """
    style = {}
    for clsName, cls_obj in self.cssStyles.items():
      if not hasattr(cls_obj, "classname"):
        style[clsName] = cls_obj
        continue

      if cls_obj.__class__.__name__ in self._cssOvr:
        cls_obj.css(self._cssOvr[cls_obj.__class__.__name__], event_attrs=self._cssEventOvr.get(cls_obj.__class__.__name__, {}))
      for css_id, css_def in cls_obj.getStyles(to_str=to_str).items():
        style[css_id] = css_def
    return style



  def toCss(self, file_name=None, path=None):
    """
    This function will be in charge of producing the best CSS content according to the need.
    If minify is set to true it will have to try to create groups and to aggregate the data before writing a one liner

    Example
    >>> Css().append(["CssBillboardTitle"]).toCss()
    '.py_cssbillboardtitle .bb-title { fill: #000000 !IMPORTANT; }'

    :param file_name:
    :param path:

    :return: The String with all the CSS classes and definition
    """
    css_str = []
    for clsName, cls_obj in self.cssStyles.items():
      if not hasattr(cls_obj, "classname"):
        css_str.append("%s %s" % (clsName, cls_obj))
        continue

      if cls_obj.__class__.__name__ in self._cssOvr:
        cls_obj.css(self._cssOvr[cls_obj.__class__.__name__], event_attrs=self._cssEventOvr.get(cls_obj.__class__.__name__, {}))
      for css_id, css_def in cls_obj.getStyles().items():
        css_str.append("%s %s" % (css_id, css_def))

    if file_name is not None and path is not None:
      filename = os.path.join(path, "%s.css" % file_name)
      if not os.path.exists(path):
        os.makedirs(path)
      with open(filename, "w") as f:
        f.write("\n".join(css_str))

    if self.rptObj._props.get('_system', {}).get('minify', False):
      return "".join(css_str)

    return "\n".join(css_str)