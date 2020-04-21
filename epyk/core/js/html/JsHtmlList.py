
from epyk.core.js.html import JsHtml
from epyk.core.js import JsUtils

from epyk.core.js.primitives import JsObjects
from epyk.core.js.objects.JsNodeDom import JsDoms


class Tags(JsHtml.JsHtmlRich):

  @property
  def content(self):
    """
    Description:
    -----------
    Returns the list of data available on the filters panel
    """
    return JsHtml.ContentFormatters(self._report, '''
      (function(dom){var content = []; dom.childNodes.forEach(function(rec){content.push(rec.textContent)}); return content})(%s)
      ''' % self.querySelector("div[name=panel]"))

  def is_duplicated(self, text):
    """
    Description:
    ------------
    Check the duplicates in the filter panel
    """
    text = JsUtils.jsConvertData(text, None)
    return JsObjects.JsObjects.get(''' 
      (function(dom){var index = -1; var children = dom.childNodes; var count = 0;
        for(child in children){if(children[child].textContent == %s){
            index = count; break; }; count++; }; return index})(%s)''' % (text, self.querySelector("div[name=panel]")))

  def hide(self):
    """
    Description:
    ------------
    Hide the filters panel
    """
    return self.querySelector("div[name=panel]").show()

  def show(self):
    """
    Description:
    ------------
    Show the filters panel
    """
    return self.querySelector("div[name=panel]").show()

  def toggle(self):
    """
    Description:
    ------------
    Toggle the display of the filters panel
    """
    return self.querySelector("div[name=panel]").toggle()

  def add(self, text, no_duplicte=True):
    """
    Description:
    ------------
    Add item on the filters panel

    Attributes:
    ----------
    :param text: String. The value to be added on the filter panel
    """
    text = JsUtils.jsConvertData(text, None)
    if no_duplicte:
      return JsObjects.JsObjects.get(''' 
      if (%(duplicated)s == -1){
      var div = document.createElement("div"); div.innerHTML = %(text)s; div.style.width = 'auto'; div.style.display = 'inline'; %(css)s;
      var icon = document.createElement("i"); icon.classList.add('fas'); icon.classList.add('fa-times'); 
      icon.addEventListener('click', function(event) {div.remove()}) ;div.appendChild(icon); %(icon_css)s;
      %(panel)s.appendChild(div); }
      ''' % {'duplicated': self.is_duplicated(text),
        'panel': self.querySelector("div[name=panel]"), 'text': text, 'css': JsDoms.get(varName="div").css(self._src.options.item_css).r,
        'icon_css': JsDoms.get(varName="icon").css({"vertical-align": "middle", "display": "inline-block",
                              "margin": "auto 0", "padding": "auto 0", "margin-left": "2px", "cursor": "pointer"}).r})

    return JsObjects.JsObjects.get(''' 
      var div = document.createElement("div"); div.innerHTML = %(text)s; div.style.width = 'auto'; div.style.display = 'inline'; %(css)s;
      var icon = document.createElement("i"); icon.classList.add('fas'); icon.classList.add('fa-times'); 
      icon.addEventListener('click', function(event) {div.remove()}) ;div.appendChild(icon); %(icon_css)s;
      %(panel)s.appendChild(div);
      ''' % {'panel': self.querySelector("div[name=panel]"), 'text': text, 'css': JsDoms.get(varName="div").css(self._src.options.item_css).r,
             'icon_css': JsDoms.get(varName="icon").css({"vertical-align": "middle", "display": "inline-block",
                              "margin": "auto 0", "padding": "auto 0", "margin-left": "2px", "cursor": "pointer"}).r})

  def clear(self):
    """
    Description:
    ------------
    Clear the content of the fitlers panel
    """
    return self.querySelector("div[name=panel]").empty()

  def remove(self, text):
    """
    Description:
    ------------
    Remove an item from the filters panel

    Attributes:
    ----------
    :param name: String. The test of the items to be removed
    """
    return JsObjects.JsObjects.get('''var itemPos = %(duplicated)s; if (itemPos >= 0){ %(panel)s.childNodes[itemPos].remove()}
      ''' % {'duplicated': self.is_duplicated(text), 'panel': self.querySelector("div[name=panel]")})