#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.js import JsUtils
from epyk.core.js.objects import JsNodeDom
from epyk.core.js.primitives import JsObject


class Msg(object):

  def __init__(self, page=None):
    self._src = page

  def status(self, timer=3000, cssAttrs=None):
    """
    Description:
    ------------
    This function will display a popup message using the key status from the service return

    Attributes:
    ----------
    :param timer: Number. The time the popup will be displayed
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "absolute", "padding": "5px 10px", 'border-radius': "5px",
                  "bottom": "10px", 'right': "10px"}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
      if 'left' in cssAttrs:
        del dflt_attrs["right"]
    return '''
      (function(event, content, response){
        var popup = document.createElement("div"); 
        if (typeof content.background === 'undefined'){
          if (response.status == 200){
            popup.style.background = 'green'; popup.style.color = 'white';}
          else {popup.style.background = 'white'}
        }
        if (typeof content.css !== 'undefined'){
          for (var key in content.css) {popup.style[key] = content.css[key]}}
        %s
        popup.innerHTML = content.status; document.body.appendChild(popup);
        setTimeout(function(){ document.body.removeChild(popup); }, %s);
      })(event, data, response)''' % (JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, timer)

  def mouse(self, content, timer=3000, cssAttrs=None):
    """
    Description:
    ------------
    Display a popup message close to the mouse.

    Attributes:
    ----------
    :param content: String. The content of the popup
    :param timer: Number. The time the popup will be displayed
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "absolute", "background": "white", "padding": "5px 10px", 'border-radius': "5px",
                  "top": JsObject.JsObject.get('event.clientY + "px"'), 'left': JsObject.JsObject.get('event.clientX + "px"')}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'bottom' in cssAttrs:
        del dflt_attrs["top"]
      if 'right' in cssAttrs:
        del dflt_attrs["left"]
    return '''
      (function(event, content){
        var popup = document.createElement("div"); %s
        popup.innerHTML = content; document.body.appendChild(popup);
        setTimeout(function(){ document.body.removeChild(popup); }, %s);
      })(event, %s)''' % (JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, timer, JsUtils.jsConvertData(content, None))

  def text(self, content, timer=3000, fixed=True, cssAttrs=None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param content: String. The content of the popup
    :param timer: Number. The time the popup will be displayed
    :param fixed:
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "fixed" if fixed else "absolute", "background": "white", "padding": "5px 10px", 'border-radius': "5px",
                  "bottom": "10px", 'right': "10px"}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
      if 'left' in cssAttrs:
        del dflt_attrs["right"]
    return '''
      (function(event, content){
        var popup = document.createElement("div"); %s
        popup.innerHTML = content; document.body.appendChild(popup);
        setTimeout(function(){ document.body.removeChild(popup); }, %s);
      })(event, %s)''' % (JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, timer, JsUtils.jsConvertData(content, None))

  def count(self, value, content=None, cssAttrs=None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param value: Integer
    :param content: String. The content of the popup
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "absolute", "background": "white", "padding": "5px 10px", 'border-radius': "5px",
                  "bottom": "40px", 'right': "10px"}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
      if 'left' in cssAttrs:
        del dflt_attrs["right"]
    return '''
      (function(event, inc, content){
        var currentVal;
        if(content == null){
          var currentVal = parseFloat(window['globalPoopup'].querySelector('div').innerHTML) + inc;
          window['globalPoopup'].querySelector('div').innerHTML = currentVal;
        } else{
          if(typeof window['globalPoopup'] === 'undefined'){
            window['globalPoopup'] = document.createElement("div");
            var globalValue = document.createElement("div");
            globalValue.innerHTML = inc; 
            globalValue.style.marginRight = '5px';
            globalValue.style.display = 'inline-block';
            var globalContent = document.createElement("div");
            globalContent.innerHTML = inc; globalContent.style.display = 'inline-block';
            globalContent.innerHTML = content;
            window['globalPoopup'].appendChild(globalValue);
            window['globalPoopup'].appendChild(globalContent);
            document.body.appendChild(window['globalPoopup']);
          } else {
            var currentVal = parseFloat(window['globalPoopup'].querySelector('div').innerHTML) + inc;
            window['globalPoopup'].querySelector('div').innerHTML = currentVal;
          } 
        }
      %s
      if(currentVal == 0){
        document.body.removeChild(window['globalPoopup']);
        window['globalPoopup'] = undefined;
      }
      })(event, %s, %s)''' % (JsNodeDom.JsDoms.get("window['globalPoopup']").css(dflt_attrs).r, value, JsUtils.jsConvertData(content, None))

  def fixed(self, content, fixed=True, cssAttrs=None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param content: String. The content of the popup
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "fixed" if fixed else "absolute", "background": "white", "padding": "10px 20px", 'border-radius': "5px",
                  "bottom": "10px", 'right': "10px"}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
      if 'left' in cssAttrs:
        del dflt_attrs["right"]
    return '''
      (function(event, content){
        var popup = document.createElement("div"); %s 
        var popupSpan = document.createElement("span");
        popupSpan.innerHTML = "&times;";
        popupSpan.style.position = 'absolute';
        popupSpan.style.top = 0;
        popupSpan.style.cursor = 'pointer';
        popupSpan.addEventListener('click', function(){ document.body.removeChild(popup) });
        popupSpan.style.right = '5px';
        popup.appendChild(popupSpan);
        var popupContent = document.createElement("div");
        popupContent.innerHTML = content;
        popup.appendChild(popupContent); document.body.appendChild(popup);
      })(event, %s)''' % (JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, JsUtils.jsConvertData(content, None))

  def center(self, content, timer=None, cssAttrs=None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param content: String. The content of the popup
    :param timer: Number. The time the popup will be displayed
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "absolute", "background": "white", "padding": "10px 20px", 'border-radius': "5px",
                  "top": "50%", 'left': "50%", 'zIndex': 110, 'border': '1px solid black'}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
      if 'left' in cssAttrs:
        del dflt_attrs["right"]
    return '''
      (function(event, content){
        var popup = document.createElement("div"); %(dom)s
        var popupSpan = document.createElement("span");
        popupSpan.innerHTML = "&times;";
        popupSpan.style.position = 'absolute';
        popupSpan.style.top = 0;
        popupSpan.style.cursor = 'pointer';
        popupSpan.addEventListener('click', function(){ document.body.removeChild(popup) });
        popupSpan.style.right = '5px';
        popup.appendChild(popupSpan);
        var popupContent = document.createElement("div");
        popupContent.innerHTML = content;
        popup.appendChild(popupContent); document.body.appendChild(popup);
        if(%(timer)s != null){
          setTimeout(function(){ document.body.removeChild(popup); }, %(timer)s);
        }
      })(event, %(content)s)''' % {'dom': JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, 'timer': timer,
                                   'content': JsUtils.jsConvertData(content, None)}

  def banner(self, content, timer=None, cssAttrs=None):
    """
    Description:
    ------------


    Attributes:
    ----------
    :param content: String. The content of the popup
    :param timer: Number. The time the popup will be displayed
    :param cssAttrs: Dictionary. The CSS attributes for the popup
    """
    dflt_attrs = {"position": "absolute", "padding": "10px", "bottom": "0", "width": '100%', 'background': 'pink'}
    if cssAttrs is not None:
      dflt_attrs.update(cssAttrs)
      if 'top' in cssAttrs:
        del dflt_attrs["bottom"]
    return '''
      (function(event, content){
        var popup = document.createElement("div"); %(dom)s
        var popupSpan = document.createElement("span");
        popupSpan.innerHTML = "&times;";
        popupSpan.style.position = 'absolute';
        popupSpan.style.top = 0;
        popupSpan.style.cursor = 'pointer';
        popupSpan.addEventListener('click', function(){ document.body.removeChild(popup) });
        popupSpan.style.right = '5px';
        popup.appendChild(popupSpan);
        var popupContent = document.createElement("div");
        popupContent.innerHTML = content;
        popup.appendChild(popupContent); document.body.appendChild(popup);
        if(%(timer)s != null){
          setTimeout(function(){ document.body.removeChild(popup); }, %(timer)s);
        }
      })(event, %(content)s)''' % {'dom': JsNodeDom.JsDoms.get("popup").css(dflt_attrs).r, 'timer': timer,
                                   'content': JsUtils.jsConvertData(content, None)}
