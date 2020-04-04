
from epyk.core.css.styles import GrpCls
from epyk.core.css import Classes


class ClassSelect(GrpCls.ClassHtml):

  def __init__(self, htmlObj):
    super(ClassSelect, self).__init__(htmlObj)
    self._css_class_dt, self._css_class_dt_ui, self._css_select = None, None, None
    self.classList['main'].add(self.cls_select)
    self.classList['main'].add(self.cls_datepicker)
    self.classList['main'].add(self.cls_datepicker_ui)

  @property
  def cls_select(self):
    """

    :rtype: Classes.CatalogInput.CatalogDate
    """
    if self._css_select is None:
      self._css_select = Classes.CatalogSelect.CatalogSelect(self.htmlObj._report, self.classList['main']).base()
    return self._css_select

  @property
  def cls_datepicker(self):
    """

    :rtype: Classes.CatalogInput.CatalogDate
    """
    if self._css_class_dt is None:
      self._css_class_dt = Classes.CatalogSelect.CatalogSelect(self.htmlObj._report, self.classList['main']).button()
    return self._css_class_dt

  @property
  def cls_datepicker_ui(self):
    """

    :rtype: Classes.CatalogInput.CatalogDate
    """
    if self._css_class_dt_ui is None:
      self._css_class_dt_ui = Classes.CatalogSelect.CatalogSelect(self.htmlObj._report, self.classList['main']).outline()
    return self._css_class_dt_ui


class ClassDropDown(GrpCls.ClassHtml):

  def __init__(self, htmlObj):
    super(ClassDropDown, self).__init__(htmlObj)
    self._css_base, self._css_menu, self._css_menu_after, self._css_menu_link = None, None, None, None
    self._css_menu_hover, self._css_menu_pull_left, self._css_menu_li = None, None, None
    self.classList['main'].add(self.cls_base)
    self.classList['main'].add(self.cls_menu)
    self.classList['main'].add(self.cls_menu_li)
    self.classList['main'].add(self.cls_menu_after)
    self.classList['main'].add(self.cls_menu_hover)
    self.classList['main'].add(self.cls_menu_pull_left)

  @property
  def cls_base(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_base is None:
      self._css_base = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).base()
    return self._css_base

  @property
  def cls_menu(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_menu is None:
      self._css_menu = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).menu()
    return self._css_menu

  @property
  def cls_menu_li(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_menu_li is None:
      self._css_menu_li = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).menu_li()
    return self._css_menu_li

  @property
  def cls_menu_after(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_menu_after is None:
      self._css_menu_after = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).menu_after()
    return self._css_menu_after

  @property
  def cls_menu_hover(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_menu_hover is None:
      self._css_menu_hover = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).menu_hover()
    return self._css_menu_hover

  @property
  def cls_menu_pull_left(self):
    """

    :rtype: Classes.CatalogTree.CatalogDropDown
    """
    if self._css_menu_pull_left is None:
      self._css_menu_pull_left = Classes.CatalogTree.CatalogDropDown(self.htmlObj._report, self.classList['main']).menu_pull_left()
    return self._css_menu_pull_left

