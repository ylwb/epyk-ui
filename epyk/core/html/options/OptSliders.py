
from epyk.core.html.options import Options


class OptionsSlider(Options):

  @property
  def animate(self):
    """
    Description:
    ------------
    Whether to slide the handle smoothly when the user clicks on the slider track. Also accepts any valid animation

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-animate
    """
    return self._report._jsStyles('animate', False)

  @animate.setter
  def animate(self, value):
    self._report._jsStyles["animate"] = value
    return self

  @property
  def classes(self):
    """
    Description:
    ------------
    Specify additional classes to add to the widget's elements.
    Any of classes specified in the Theming section can be used as keys to override their value.
    To learn more about this option, check out the learn article about the classes option.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-classes
    """
    return self._report._jsStyles('classes')

  @classes.setter
  def classes(self, value):
    self._report._jsStyles["classes"] = value
    return self

  @property
  def disabled(self):
    """
    Description:
    ------------
    Disables the slider if set to true.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-disabled
    """
    return self._report._jsStyles('disabled', False)

  @disabled.setter
  def disabled(self, value):
    self._report._jsStyles["disabled"] = value
    return self

  @property
  def max(self):
    """
    Description:
    ------------
    The maximum value of the slider.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-max
    """
    return self._report._jsStyles('max', 100)

  @max.setter
  def max(self, value):
    self._report._jsStyles["max"] = value
    return self

  @property
  def min(self):
    """
    Description:
    ------------
    The minimum value of the slider.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-min
    """
    return self._report._jsStyles('min', 0)

  @min.setter
  def min(self, value):
    self._report._jsStyles["min"] = value
    return self

  @property
  def orientation(self):
    """
    Description:
    ------------
    Determines whether the slider handles move horizontally (min on left, max on right) or vertically (min on bottom, max on top).
    Possible values: "horizontal", "vertical".

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-orientation
    """
    return self._report._jsStyles('orientation', "horizontal")

  @orientation.setter
  def orientation(self, value):
    self._report._jsStyles["orientation"] = value
    return self

  @property
  def range(self):
    """
    Description:
    ------------
    Whether the slider represents a range.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-range
    """
    return self._report._jsStyles('range', False)

  @range.setter
  def range(self, value):
    self._report._jsStyles["range"] = value
    return self

  @property
  def step(self):
    """
    Description:
    ------------
    Determines the size or amount of each interval or step the slider takes between the min and max.
    The full specified value range of the slider (max - min) should be evenly divisible by the step.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-step
    """
    return self._report._jsStyles('step', 1)

  @step.setter
  def step(self, value):
    self._report._jsStyles["step"] = value
    return self

  @property
  def value(self):
    """
    Description:
    ------------
    Determines the value of the slider, if there's only one handle.
    If there is more than one handle, determines the value of the first handle.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-value
    """
    return self._report._jsStyles('value', 0)

  @value.setter
  def value(self, value):
    self._report._jsStyles["value"] = value
    return self

  @property
  def values(self):
    """
    Description:
    ------------
    This option can be used to specify multiple handles.
    If the range option is set to true, the length of values should be 2.

    Related Pages:
    --------------
    https://api.jqueryui.com/slider/#option-values
    """
    return self._report._jsStyles('values', 0)

  @values.setter
  def values(self, value):
    self._report._jsStyles["values"] = value
    return self


class OptionsProgBar(Options):

  @property
  def classes(self):
    """
    Description:
    ------------
    Initialize the progressbar with the classes option specified, changing the theming for the ui-progressbar

    Related Pages:
    --------------
    https://api.jqueryui.com/progressbar/#option-classes
    """
    return self._report._jsStyles('classes')

  @classes.setter
  def classes(self, value):
    self._report._jsStyles["classes"] = value
    return self

  @property
  def background(self):
    """
    Description:
    ------------

    """
    return self._report._jsStyles['css'].get('background')

  @background.setter
  def background(self, value):
    self._report._jsStyles['css']["background"] = value
    return self

  def css(self, attrs):
    """
    Description:
    ------------

    :param attrs:
    """
    self._report._jsStyles['css'].update(attrs)
    return self

  @property
  def disabled(self):
    """
    Description:
    ------------
    Disables the progressbar if set to true.

    Related Pages:
    --------------
    https://api.jqueryui.com/progressbar/#option-disabled
    """
    return self._report._jsStyles('disabled', False)

  @disabled.setter
  def disabled(self, bool):
    self._report._jsStyles["disabled"] = bool
    return self

  @property
  def max(self):
    """
    Description:
    ------------
    The maximum value of the progressbar.

    Related Pages:
    --------------
    https://api.jqueryui.com/progressbar/#option-max
    """
    return self._report._jsStyles('max', 100)

  @max.setter
  def max(self, bool):
    self._report._jsStyles["max"] = bool
    return self

  @property
  def value(self):
    """
    Description:
    ------------
    The value of the progressbar.

    Related Pages:
    --------------
    https://api.jqueryui.com/progressbar/#option-value
    """
    return self._report._jsStyles('value', False)

  @value.setter
  def value(self, bool):
    self._report._jsStyles["value"] = bool
    return self


class OptionsMenu(Options):
  @property
  def classes(self):
    """
    Description:
    ------------
    Specify additional classes to add to the widget's elements.
    Any of classes specified in the Theming section can be used as keys to override their value.
    To learn more about this option, check out the learn article about the

    Related Pages:
    --------------
    https://api.jqueryui.com/menu/#option-classes
    """
    return self._report._jsStyles('classes', {})

  @classes.setter
  def classes(self, value):
    self._report._jsStyles["classes"] = value
    return self

  @property
  def disabled(self):
    """
    Description:
    ------------
    Disables the menu if set to true

    Related Pages:
    --------------
    https://api.jqueryui.com/menu/#option-disabled
    """
    return self._report._jsStyles('disabled', False)

  @disabled.setter
  def disabled(self, bool):
    self._report._jsStyles["disabled"] = bool
    return self

  @property
  def icons(self):
    """
    Description:
    ------------
    Icons to use for submenus, matching an icon provided by the jQuery UI CSS Framework.

    Related Pages:
    --------------
    https://api.jqueryui.com/menu/#option-icons
    """
    return self._report._jsStyles('icons')

  @icons.setter
  def icons(self, bool):
    self._report._jsStyles["icons"] = bool
    return self

  @property
  def position(self):
    """
    Description:
    ------------
    Identifies the position of submenus in relation to the associated parent menu item.
    The of option defaults to the parent menu item, but you can specify another element to position against.
    You can refer to the jQuery UI Position utility for more details about the various options.

    Related Pages:
    --------------
    https://api.jqueryui.com/menu/#option-position
    """
    return self._report._jsStyles('position')

  @position.setter
  def position(self, bool):
    self._report._jsStyles["position"] = bool
    return self


class OptionDialog(Options):
  @property
  def appendTo(self):
    """
    Description:
    ------------
    Which element the dialog (and overlay, if modal) should be appended to

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-appendTo
    """
    return self._report._jsStyles('appendTo', 'body')

  @appendTo.setter
  def appendTo(self, bool):
    self._report._jsStyles["appendTo"] = bool
    return self

  @property
  def autoOpen(self):
    """
    Description:
    ------------
    If set to true, the dialog will automatically open upon initialization.
    If false, the dialog will stay hidden until the open() method is called.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-autoOpen
    """
    return self._report._jsStyles('autoOpen', True)

  @autoOpen.setter
  def autoOpen(self, bool):
    self._report._jsStyles["autoOpen"] = bool
    return self

  @property
  def classes(self):
    """
    Description:
    ------------
    Specify additional classes to add to the widget's elements.
    Any of classes specified in the Theming section can be used as keys to override their value.
    To learn more about this option, check out the learn article about the

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-classes
    """
    return self._report._jsStyles('classes', {})

  @classes.setter
  def classes(self, value):
    self._report._jsStyles["classes"] = value
    return self

  @property
  def closeOnEscape(self):
    """
    Description:
    ------------
    Specifies whether the dialog should close when it has focus and the user presses the escape (ESC) key.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-closeOnEscape
    """
    return self._report._jsStyles('closeOnEscape', True)

  @closeOnEscape.setter
  def closeOnEscape(self, value):
    self._report._jsStyles["closeOnEscape"] = value
    return self

  @property
  def closeText(self):
    """
    Description:
    ------------
    Specifies the text for the close button. Note that the close text is visibly hidden when using a standard theme.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-closeText
    """
    return self._report._jsStyles('closeText', True)

  @closeText.setter
  def closeText(self, value):
    self._report._jsStyles["closeText"] = value
    return self

  @property
  def draggable(self):
    """
    Description:
    ------------
    If set to true, the dialog will be draggable by the title bar. Requires the jQuery UI Draggable widget to be included.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-draggable
    """
    return self._report._jsStyles('draggable', True)

  @draggable.setter
  def draggable(self, value):
    self._report._jsStyles["draggable"] = value
    return self

  @property
  def height(self):
    """
    Description:
    ------------
    The height of the dialog.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-height
    """
    return self._report._jsStyles('draggable', 'auto')

  @height.setter
  def height(self, value):
    self._report._jsStyles["height"] = value
    return self

  @property
  def hide(self):
    """
    Description:
    ------------
    If and how to animate the hiding of the dialog.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-hide
    """
    return self._report._jsStyles('draggable', None)

  @hide.setter
  def hide(self, value):
    self._report._jsStyles["hide"] = value
    return self

  @property
  def maxHeight(self):
    """
    Description:
    ------------
    The maximum height to which the dialog can be resized, in pixels.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-maxHeight
    """
    return self._report._jsStyles('maxHeight', None)

  @maxHeight.setter
  def maxHeight(self, value):
    self._report._jsStyles["maxHeight"] = value
    return self

  @property
  def maxWidth(self):
    """
    Description:
    ------------
    The maximum width to which the dialog can be resized, in pixels.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-maxWidth
    """
    return self._report._jsStyles.get("option", {})('maxWidth', None)

  @maxWidth.setter
  def maxWidth(self, value):
    self._report._jsStyles.setdefault("option", {})["maxWidth"] = value
    return self

  @property
  def minHeight(self):
    """
    Description:
    ------------
    The minimum height to which the dialog can be resized, in pixels.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-minHeight
    """
    return self._report._jsStyles.get("option", {})('minHeight', None)

  @minHeight.setter
  def minHeight(self, value):
    self._report._jsStyles.setdefault("option", {})["minHeight"] = value
    return self

  @property
  def minWidth(self):
    """
    Description:
    ------------
    The minimum width to which the dialog can be resized, in pixels.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-minWidth
    """
    return self._report._jsStyles.get("option", {})('minWidth', None)

  @minWidth.setter
  def minWidth(self, value):
    self._report._jsStyles.setdefault("option", {})["minWidth"] = value
    return self

  @property
  def modal(self):
    """
    Description:
    ------------
    If set to true, the dialog will have modal behavior; other items on the page will be disabled, i.e., cannot be interacted with.
    Modal dialogs create an overlay below the dialog but above other page elements.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-modal
    """
    return self._report._jsStyles.get("option", {})('modal', True)

  def position(self, my="center", at="center", of="window"):
    """
    Description:
    ------------
    Specifies where the dialog should be displayed when opened. The dialog will handle collisions such that as much of the dialog is visible as possible.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-position
    """
    self._report._jsStyles['position'] = {"my": "center", "at": "center", "of": "window"}
    return self

  @modal.setter
  def modal(self, value):
    self._report._jsStyles.setdefault("option", {})["modal"] = value
    return self

  @property
  def resizable(self):
    """
    Description:
    ------------
    If set to true, the dialog will be resizable. Requires the jQuery UI Resizable widget to be included.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-resizable
    """
    return self._report._jsStyles.get("option", {})('resizable', True)

  @resizable.setter
  def resizable(self, value):
    self._report._jsStyles.setdefault("option", {})["resizable"] = value
    return self

  @property
  def title(self):
    """
    Description:
    ------------
    Specifies the title of the dialog. If the value is null, the title attribute on the dialog source element will be used.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-title
    """
    return self._report._jsStyles.get('title', None)

  @title.setter
  def title(self, value):
    self._report._jsStyles["title"] = value
    return self

  @property
  def width(self):
    """
    Description:
    ------------
    The width of the dialog, in pixels.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-title
    """
    return self._report._jsStyles.get('width', 300)

  @width.setter
  def width(self, value):
    self._report._jsStyles["width"] = value
    return self


class OptionAutoComplete(Options):

  @property
  def appendTo(self):
    """
    Description:
    ------------
    Which element the menu should be appended to.
    When the value is null, the parents of the input field will be checked for a class of ui-front.
    If an element with the ui-front class is found, the menu will be appended to that element.
    Regardless of the value, if no element is found, the menu will be appended to the body.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-appendTo
    """
    return self._report._jsStyles('appendTo', None)

  @appendTo.setter
  def appendTo(self, value):
    self._report._jsStyles["appendTo"] = value
    return self

  @property
  def autoFocus(self):
    """
    Description:
    ------------
    If set to true the first item will automatically be focused when the menu is shown.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-autoFocus
    """
    return self._report._jsStyles('autoFocus', False)

  @autoFocus.setter
  def autoFocus(self, value):
    self._report._jsStyles["autoFocus"] = value
    return self

  @property
  def classes(self):
    """
    Description:
    ------------
    Specify additional classes to add to the widget's elements.
    Any of classes specified in the Theming section can be used as keys to override their value.
    To learn more about this option, check out the learn article about the classes option.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-classes
    """
    return self._report._jsStyles('classes', {})

  @classes.setter
  def classes(self, value):
    self._report._jsStyles["classes"] = value
    return self

  @property
  def delay(self):
    """
    Description:
    ------------
    The delay in milliseconds between when a keystroke occurs and when a search is performed.
    A zero-delay makes sense for local data (more responsive), but can produce a lot of load for remote data, while being less responsive.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-delay
    """
    return self._report._jsStyles('delay', 300)

  @delay.setter
  def delay(self, value):
    self._report._jsStyles["delay"] = value
    return self

  @property
  def disabled(self):
    """
    Description:
    ------------
    Disables the autocomplete if set to true.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-delay
    """
    return self._report._jsStyles('disabled', True)

  @disabled.setter
  def disabled(self, value):
    self._report._jsStyles["disabled"] = value
    return self

  @property
  def minLength(self):
    """
    Description:
    ------------
    The minimum number of characters a user must type before a search is performed.
    Zero is useful for local data with just a few items, but a higher value should be used when a single character search could match a few thousand items.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-minLength
    """
    return self._report._jsStyles('minLength', 0)

  @minLength.setter
  def minLength(self, value):
    self._report._jsStyles["minLength"] = value
    return self

  def position(self, my="center", at="center", of="window"):
    """
    Description:
    ------------
    Specifies where the dialog should be displayed when opened. The dialog will handle collisions such that as much of the dialog is visible as possible.

    Related Pages:
    --------------
    https://api.jqueryui.com/dialog/#option-position
    """
    self._report._jsStyles['position'] = {"my": "center", "at": "center", "of": "window"}
    return self

  @property
  def source(self):
    """
    Description:
    ------------
    Defines the data to use, must be specified.

    Related Pages:
    --------------
    https://api.jqueryui.com/autocomplete/#option-source
    """
    return self._report._jsStyles('source', [])

  @source.setter
  def source(self, value):
    self._report._jsStyles["source"] = value
    return self
