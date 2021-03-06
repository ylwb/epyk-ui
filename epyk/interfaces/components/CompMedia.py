#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core import html
from epyk.interfaces import Arguments


class Media(object):
  def __init__(self, context):
    self.context = context

  def video(self, value, align="center", path=None, width=(100, '%'), height=(None, 'px'), htmlCode=None, profile=None, options=None):
    """
    Add a video from the server to the page.
    The format for the video must be MP4

    Usage::

      rptObj.ui.media.video("CWWB3673.MP4")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlMedia.Media`

    Related Pages:

      https://www.w3schools.com/html/html5_video.asp

    Attributes:
    ----------
    :param value: The name of the video
    :param path: Optional. THe path to the video
    :param align: String. Optional. A string with the horizontal position of the component
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: Optional. The component identifier code (for both Python and Javascript)
    :param profile: Boolean or Dictionary. Optional. A flag to set the component performance storage
    :param options: Dictionary. Optional. Specific Python options available for this component
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dft_options = {"autoplay": True}
    if options is not None:
      dft_options.update(options)
    html_media = html.HtmlMedia.Media(self.context.rptObj, value, path, width, height, htmlCode, profile, dft_options)
    if align == "center":
      html_media.style.css.margin = "auto"
      html_media.style.css.display = "block"
    return html_media

  def audio(self, value, path=None, width=(100, '%'), height=(None, 'px'), htmlCode=None, profile=None, options=None):
    """
    Add a audio track from the server to the page.
    The format for the video must be mpeg

    Usage::

      rptObj.ui.media.video("CWWB3673.mpeg")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlMedia.Audio`

    Related Pages

    https://www.w3schools.com/html/html5_video.asp

    Attributes:
    ----------
    :param value: The name of the audio object
    :param path: String. Optional. THe path to the audio object
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: String. Optional. An identifier for this component (on both Python and Javascript side)
    :param profile: Boolean or Dictionary. Optional. A flag to set the component performance storage
    :param options: Dictionary. Optional. Specific Python options available for this component
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dft_options = {"autoplay": True}
    if options is not None:
      dft_options.update(options)
    html_audio = html.HtmlMedia.Audio(self.context.rptObj, value, path, width, height, htmlCode, profile, dft_options)
    return html_audio

  def youtube(self, link, align="center", width=(100, '%'), height=(None, 'px'), htmlCode=None, profile=None, options=None):
    """
    This will add a youtube video using the shared line to embedded to a website.

    Usage::

      rptObj.ui.media.youtube("https://www.youtube.com/embed/dfiHMtih5Ac")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlMedia.Youtube`

    Related Pages

    https://www.w3schools.com/html/html5_video.asp

    Attributes:
    ----------
    :param link: String. The youtube link
    :param align: String. Optional. A string with the horizontal position of the component
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param htmlCode: Optional. The component identifier code (for both Python and Javascript)
    :param profile: Optional. A flag to set the component performance storage
    :param options: Optional. A dictionary with the components properties
    """
    width = Arguments.size(width, unit="%")
    height = Arguments.size(height, unit="px")
    dflt_options = {"width": "420", "height": "315", "type": "text/html"}
    if '/embed/' not in link:
      link = html.HtmlMedia.Youtube.get_embed_link(link)
    if options is not None:
      dflt_options.update(options)
    html_youtube = html.HtmlMedia.Youtube(self.context.rptObj, link, width, height, htmlCode, profile, dflt_options)
    html_youtube.style.css.text_align = align
    return html_youtube
