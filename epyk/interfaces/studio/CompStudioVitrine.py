#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from epyk.core.css import Defaults as Defaults_css
from epyk.interfaces import Arguments


class Vitrine(object):
  def __init__(self, context):
    self.parent = context

