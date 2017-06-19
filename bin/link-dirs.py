#!/usr/bin/env python

import argparse
import errno
import os
import sys

import json

def symlink(src, target, force=False):
  try:
    os.symlink(src, target)
  except OSError as ex:
    if ex.errno == errno.EEXIST and force:
      os.remove(target)
      os.symlink(src, target)
    else:
      raise ex

def find_sources(conf, salt, secret, formulas):
  sources = {}
  if conf:
    with open(conf, "r") as ff:
      sources = json.load(ff)

  # Prefer command line over config file
  # Normalize path relative to CWD for command line paths
  if salt:
    sources["salt"] = os.path.abspath(salt)
  if secret:
    sources["secret"] = os.path.abspath(secret)
  if formulas:
    sources["formulas"] = os.path.abspath(formulas)

  # Check that necessary sources have all been defined
  for name in ("salt", "secret", "formulas"):
    if name not in sources:
      raise argparse.ArgumentError("--%s" % name, "must be defined in "
                                   "either command line or config file")

  for name, path in sources.items():
    expanded = os.path.expanduser(path)
    expanded = os.path.expandvars(expanded)
    sources[name] = expanded

  return ( sources["salt"], sources["secret"], sources["formulas"] )

def main(argv):
  cmd, args = parse_args(argv)

  sources = find_sources(args.config, args.salt, args.secret, args.formulas)

  parent = os.path.dirname(os.path.dirname(os.path.abspath(cmd)))
  targets = (
    os.path.join(parent, "srv/salt"),
    os.path.join(parent, "srv/secret"),
    os.path.join(parent, "srv/formulas")
  )

  for src, target in zip(sources, targets):
    rel_target = os.path.relpath(target)
    print "Linking %s -> %s" % (rel_target, src)
    try:
      symlink(src, target, force=True)
    except OSError as ex:
      print "Failed to link %s -> %s" % (rel_target, src)
  return 0

def parse_args(argv):
  parser = argparse.ArgumentParser(description="Symlink host directories "
                                   " into Vagrant guest /srv folder")
  parser.add_argument("--salt", help="Dir that will be used as /srv/salt")
  parser.add_argument("--secret", help="Dir that will be used as /srv/secret")
  parser.add_argument("--formulas", help="Dir that will be mounted as ")
  parser.add_argument("--config", help="Config file containing symlink "
                      "mappings for /srv/")
  args = parser.parse_args(argv[1:])
  return argv[0], args

if __name__ == "__main__":
  sys.exit(main(sys.argv))
