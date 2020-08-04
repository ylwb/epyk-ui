#!/usr/bin/python
# -*- coding: utf-8 -*-


def size(value, unit="%"):
  """
  Description:
  ------------
  Wrapper to allow size arguments to be more flexible.
  By using this in the interface it is possible to then use float values instead of the usual tuples.

  Attributes:
  ----------
  :param value:
  :param unit:
  """
  if isinstance(value, tuple):
    return value

  return (value, unit)
