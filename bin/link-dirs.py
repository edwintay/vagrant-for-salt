#!/usr/bin/env python

import argparse
import errno
import os
import sys

import json

DEFAULT_TOP = "srv"

def symlink(src, target, force=False):
  try:
    os.symlink(src, target)
  except OSError as ex:
    if ex.errno == errno.EEXIST and force:
      os.remove(target)
      os.symlink(src, target)
    else:
      raise ex

def ensure_dir_exists(path, mode=0777):
  if os.path.islink(path):
    print "Removing link %s" % path
    os.remove(path)

  if os.path.isdir(path):
    return

  print "Creating dir %s" % os.path.relpath(path)
  os.mkdir(path, mode)

def expandvars(sources):
  expanded = {}

  for name, source in sources.items():
    if isinstance(source, dict):
      # Recurse into nested dictionary
      expath = expandvars(source)
    else:
      # Otherwise, assume source is string
      expath = os.path.expanduser(source)
      expath = os.path.expandvars(expath)

    expanded[name] = expath

  return expanded

def find_sources(conf):
  raw = {}
  if conf:
    with open(conf, "r") as ff:
      raw = json.load(ff)

  # Check that minimal sources have been defined
  for name in ("salt", "secret"):
    if name not in raw:
      raise argparse.ArgumentError("--%s" % name, "must be defined")

  sources = expandvars(raw)

  return sources

def link_sources(top, sources):
  ensure_dir_exists(top)

  for tgt, src in sources.items():
    linkpath = os.path.join(top, tgt)

    # Recurse into nested dictionary
    if isinstance(src, dict):
      link_sources(linkpath, src)
      continue

    # Otherwise, assume path and try symlinking
    linkrel = os.path.relpath(linkpath)
    print "Linking %s -> %s" % (linkrel, src)
    try:
      symlink(src, linkpath, force=True)
    except OSError as ex:
      print "Failed to link %s -> %s" % (linkrel, src)

  return

def main(argv):
  cmd, args = parse_args(argv)

  sources = find_sources(args.config)

  parent = os.path.dirname(os.path.dirname(os.path.abspath(cmd)))
  top = os.path.join(parent, DEFAULT_TOP)
  link_sources(top, sources)

  return 0

def parse_args(argv):
  parser = argparse.ArgumentParser(description="Symlink host directories "
                                   " into Vagrant guest /srv folder")
  parser.add_argument("--config", help="Config file containing symlink "
                      "mappings for /srv")
  args = parser.parse_args(argv[1:])
  return argv[0], args

if __name__ == "__main__":
  sys.exit(main(sys.argv))
