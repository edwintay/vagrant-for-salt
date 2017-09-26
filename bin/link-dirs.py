#!/usr/bin/env python

import argparse
import errno
import json
import logging
import os
import sys

DEFAULT_TOP = "srv"

LOG_FORMAT="%(levelname)s :: %(message)s"
logger = logging.getLogger(__name__)

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
    logger.info("Removing link %s", path)
    os.remove(path)

  if os.path.isdir(path):
    return

  logger.info("Creating dir %s", os.path.relpath(path))
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
  with open(conf, "r") as ff:
    raw = json.load(ff)

  # Check that minimal sources have been defined
  for name in ("salt",):
    if name not in raw:
      raise argparse.ArgumentTypeError("key '%s' missing in "
                                       "%s" % (name, conf))

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
    logger.info("Linking %s -> %s", linkrel, src)
    try:
      symlink(src, linkpath, force=True)
    except OSError as ex:
      logger.error("Failed to link %s -> %s", linkrel, src)

  return

def main(argv):
  cmd, args = parse_args(argv)

  logging.basicConfig(level=args.loglevel, format=LOG_FORMAT)

  sources = find_sources(args.config)

  parent = os.path.dirname(os.path.dirname(os.path.abspath(cmd)))
  top = os.path.join(parent, DEFAULT_TOP)
  link_sources(top, sources)

  return 0

def parse_args(argv):
  parser = argparse.ArgumentParser(description="Symlink host directories "
                                   " into Vagrant guest /srv folder")
  parser.add_argument("--config", help="config file containing symlink "
                      "mappings for /srv", required=True)
  parser.add_argument("-s", "--silent", help="set log level to WARNING",
                      dest="loglevel", action="store_const",
                      const=logging.WARNING, default=logging.INFO)
  args = parser.parse_args(argv[1:])
  return argv[0], args

if __name__ == "__main__":
  sys.exit(main(sys.argv))
