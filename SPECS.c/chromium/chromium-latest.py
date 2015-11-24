#!/usr/bin/python
# Copyright 2010,2015 Tom Callaway <tcallawa@redhat.com>
# Copyright 2013 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import csv
import glob
import locale
import os
import shutil
import StringIO
import sys
import urllib

chromium_url = "http://commondatastorage.googleapis.com/chromium-browser-official/"

chromium_root_dir = "."
version_string = "stable"

name = 'Chromium Latest'
script_version = 0.5
my_description = '{0} {1}'.format(name, script_version)


def dlProgress(count, blockSize, totalSize):
  percent = int(count * blockSize * 100 / totalSize)
  sys.stdout.write("\r" + "Downloading ... %d%%" % percent)
  sys.stdout.flush()


def delete_chromium_dir(ch_dir):
  full_dir = "%s/%s" % (latest_dir, ch_dir)
  print 'Deleting %s ' % full_dir
  if os.path.isdir(full_dir):
    shutil.rmtree(full_dir)
    print '[DONE]'
  else:
    print '[NOT FOUND]'


def delete_chromium_files(files):
  full_path = "%s/%s" % (latest_dir, files)
  print 'Deleting ' + full_path + ' ',
  for filename in glob.glob(full_path):
    print 'Deleting ' + filename + ' ',
    os.remove(filename)
    print '[DONE]'


def check_omahaproxy(channel="stable"):
  version = 0
  status_url = "http://omahaproxy.appspot.com/all?os=linux&channel=" + channel

  usock = urllib.urlopen(status_url)
  status_dump = usock.read()
  usock.close()
  status_list = StringIO.StringIO(status_dump)
  status_reader = list(csv.reader(status_list, delimiter=','))
  linux_channels = [s for s in status_reader if "linux" in s]
  linux_channel = [s for s in linux_channels if channel in s]
  version = linux_channel[0][2]

  if version == 0:
    print 'I could not find the latest %s build. Bailing out.' % channel
    sys.exit(1)
  else:
    print 'Latest Chromium Version on %s at %s is %s' % (channel, status_url, version)
    return version


def remove_file_if_exists(filename):
  if os.path.isfile("./%s" % filename):
    try:
      os.remove(filename)
    except Exception:
      pass


def download_version(version):

  chromium_file = 'chromium-%s.tar.xz' % version
  path = '%s%s' % (chromium_url, chromium_file)

  if (args.clean):
    remove_file_if_exists(chromium_file)

  # Let's make sure we haven't already downloaded it.
  if os.path.isfile("./%s" % chromium_file):
    print "%s already exists!" % chromium_file
  else:
    print "Downloading %s" % path
    # Perhaps look at using python-progressbar at some point?
    urllib.urlretrieve(path, chromium_file, reporthook=dlProgress)
    urllib.urlcleanup()
    print ""

  if (args.tests):
    chromium_testdata_file = 'chromium-%s-testdata.tar.xz' % version
    path = '%s%s' % (chromium_url, chromium_testdata_file)

    if (args.clean):
      remove_file_if_exists(chromium_testdata_file)

    # Let's make sure we haven't already downloaded it.
    if os.path.isfile("./%s" % chromium_testdata_file):
      print "%s already exists!" % chromium_testdata_file
    else:
      # Perhaps look at using python-progressbar at some point?
      print "Downloading %s" % path
      urllib.urlretrieve(path, chromium_testdata_file, reporthook=dlProgress)
      urllib.urlcleanup()
      print ""


def download_chrome_latest_rpm(arch):

  chrome_rpm = 'google-chrome-%s_current_%s.rpm' % (version_string, arch)
  path = 'https://dl.google.com/linux/direct/%s' % chrome_rpm

  if (args.clean):
    remove_file_if_exists(chrome_rpm)

  # Let's make sure we haven't already downloaded it.
  if os.path.isfile("./%s" % chrome_rpm):
    print "%s already exists!" % chrome_rpm
  else:
    print "Downloading %s" % path
    # Perhaps look at using python-progressbar at some point?
    urllib.urlretrieve(path, chrome_rpm, reporthook=dlProgress)
    urllib.urlcleanup()
    print ""


# This is where the magic happens
if __name__ == '__main__':

  # Locale magic
  locale.setlocale(locale.LC_ALL, '')

  # Create the parser object
  parser = argparse.ArgumentParser(description=my_description)

  parser.add_argument(
      '--stable', action='store_true',
      help='Get the latest stable Chromium source')
  parser.add_argument(
      '--beta', action='store_true',
      help='Get the latest beta Chromium source')
  parser.add_argument(
      '--dev', action='store_true',
      help='Get the latest dev Chromium source')
  parser.add_argument(
      '--chrome', action='store_true',
      help='Get the latest Chrome rpms for the given channel')
  parser.add_argument(
      '--ffmpegclean', action='store_true',
      help='Get the latest Chromium release from given channel and cleans ffmpeg sources from proprietary stuff')
  parser.add_argument(
      '--tests', action='store_true',
      help='Get the additional data for running tests')
  parser.add_argument(
      '--clean', action='store_true',
      help='Re-download all previously downloaded sources')
  parser.add_argument(
      '--prep', action='store_true',
      help='Prepare everything, but don\'t compress the result')

  # Parse the args
  args = parser.parse_args()

  if args.stable:
    version_string = "stable"
  elif args.beta:
    version_string = "beta"
  elif args.dev:
    version_string = "dev"
  elif (not (args.stable or args.beta or args.dev)):
    print 'No version specified, downloading STABLE'
    args.stable = True

  chromium_version = check_omahaproxy(version_string)

  if args.dev:
    version_string = "unstable"

  if args.chrome:
    latest = 'google-chrome-%s_current_i386' % version_string
    download_chrome_latest_rpm("i386")
    latest = 'google-chrome-%s_current_x86_64' % version_string
    download_chrome_latest_rpm("x86_64")
    if (not (args.ffmpegclean or args.tests)):
      sys.exit(1)

  latest = 'chromium-%s.tar.xz' % chromium_version

  download_version(chromium_version)

  # Lets make sure we haven't unpacked it already
  latest_dir = "%s/chromium-%s" % (chromium_root_dir, chromium_version)
  if os.path.isdir(latest_dir):
    print "%s already exists, perhaps %s has already been unpacked?" % (latest_dir, latest)
  else:
    print "Unpacking %s into %s, please wait." % (latest, latest_dir)
    if (os.system("tar -xJf %s" % latest) != 0):
      print "%s is possibly corrupted, exiting." % (latest)
      sys.exit(1)

  if (not (args.ffmpegclean)):
    junk_dirs = ['third_party/WebKit/Tools/Scripts/webkitpy/layout_tests',
                 'webkit/data/layout_tests', 'third_party/hunspell/dictionaries',
                 'chrome/test/data', 'native_client/tests',
                 'third_party/WebKit/LayoutTests']

    # First, the dirs:
    for directory in junk_dirs:
      delete_chromium_dir(directory)

  courgette_dirs = ['courgette']
  # Cannot do this anymore. Only re-enable if we have to.
  # for directory in courgette_dirs:
  #   delete_chromium_dir(directory)

  # There has got to be a better, more portable way to do this.
  os.system("find %s -depth -name reference_build -type d -exec rm -rf {} \;" % latest_dir)

  # I could not find good bindings for xz/lzma support, so we system call here too.
  chromium_clean_xz_file = "chromium-" + chromium_version + "-clean.tar.xz"

  remove_file_if_exists(chromium_clean_xz_file)

  if (args.ffmpegclean):
    print("Cleaning ffmpeg from proprietary things...")
    os.system("./clean_ffmpeg.sh %s/third_party/ffmpeg" % latest_dir)
    print "Done!"

  if (not args.prep):
    print "Compressing cleaned tree, please wait..."
    os.chdir(chromium_root_dir)
    os.system("tar --exclude=\.svn -cf - chromium-%s | xz -9 -T 0 -f > %s" % (chromium_version, chromium_clean_xz_file))

  print "Finished!"
