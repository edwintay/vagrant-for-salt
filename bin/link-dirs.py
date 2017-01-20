#!/usr/bin/env python

import argparse
import errno
import os
import sys

def symlink(src, target, force=False):
  try:
    os.symlink(src, target)
  except OSError as ex:
    if ex.errno == errno.EEXIST and force:
      os.remove(target)
      os.symlink(src, target)
    else:
      raise ex

def main(argv):
  cmd, args = parse_args(argv)

  sources = (
    os.path.abspath(args.salt),
    os.path.abspath(args.secret),
    os.path.abspath(args.formulas)
  )

  parent = os.path.dirname(os.path.dirname(os.path.abspath(cmd)))
  targets = (
    os.path.join(parent, "srv/salt"),
    os.path.join(parent, "srv/secret"),
    os.path.join(parent, "srv/formulas")
  )

  print "Linking:"
  for src, target in zip(sources, targets):
    print "\t%s: %s" % (src, target)
    try:
      symlink(src, target, force=True)
    except OSError as ex:
      print "Failed to create %s" % target
  return 0

def parse_args(argv):
  parser = argparse.ArgumentParser(description="Symlink host directories "
                                   " into Vagrant guest /srv folder")
  parser.add_argument("--salt", help="Dir that will be used as /srv/salt",
                      required=True)
  parser.add_argument("--secret", help="Dir that will be used as /srv/secret",
                      required=True)
  parser.add_argument("--formulas", help="Dir that will be mounted as "
                      "/srv/formulas", required=True)
  args = parser.parse_args(argv[1:])
  return argv[0], args

if __name__ == "__main__":
  sys.exit(main(sys.argv))
