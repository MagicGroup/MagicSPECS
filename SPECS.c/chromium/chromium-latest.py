#!/usr/bin/python
# Copyright 2010 Tom Callaway <tcallawa@redhat.com>
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
import errno
import glob
import locale
import os
import re
import shutil
import StringIO
import sys
import tarfile
import urllib
from sgmllib import SGMLParser

#chromium_url = "http://build.chromium.org/buildbot/official/"
chromium_url = "http://commondatastorage.googleapis.com/chromium-browser-official/"

#chromium_root_dir = os.expanduser("~/chromium")
chromium_root_dir = "."

name = 'Chromium Latest'
script_version = 0.3
my_description = '{0} {1}'.format(name, script_version)

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []
	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST:
			pass
		else: raise

def dlProgress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r" + "Downloading %s ... %d%%" % (latest, percent))
	sys.stdout.flush()

def delete_chromium_dir(dir):
	full_dir = "%s/%s" % (latest_dir, dir)
	print 'Deleting ' + full_dir + ' ',
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

def try_int(s):
    "Convert to integer if possible."
    try: return int(s)
    except: return s

def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))

def natcmp(a, b):
    "Natural string comparison, case sensitive."
    return cmp(natsort_key(a), natsort_key(b))

def natcasecmp(a, b):
    "Natural string comparison, ignores case."
    return natcmp(a.lower(), b.lower())

def natsort(seq, cmp=natcmp):
    "In-place natural string sort."
    seq.sort(cmp)
    
def natsorted(seq, cmp=natcmp):
    "Returns a copy of seq, sorted by natural string sort."
    import copy
    temp = copy.copy(seq)
    natsort(temp, cmp)
    return temp

def check_latest(chromium_version):
    usock = urllib.urlopen(chromium_url)
    parser = URLLister()
    parser.feed(usock.read())
    usock.close()

    # sort the list of urls we got
    natsorted_list = natsorted(parser.urls)

    # get the last item in the list
    # this should always be the newest build
    latest = natsorted_list.pop()

    if latest == "official/":
       latest = natsorted_list.pop()

    version = re.sub('chromium-', '', latest)
    version = re.sub('.tar.bz2', '', chromium_version)

    print "Latest Chromium Version found at %s is %s" % (chromium_url, version)
    return version

def check_omahaproxy(channel = "stable"):
    version = 0;
    status_url = "http://omahaproxy.appspot.com/?os=linux&channel=" + channel

    usock = urllib.urlopen(status_url)
    status_dump = usock.read()
    usock.close()
    status_list = StringIO.StringIO(status_dump)
    status_reader = csv.reader(status_list, delimiter=',')
    # we always want second row; iterate two times
    status_reader.next()
    version = status_reader.next()[2]

    if version == 0:
       print 'I could not find the latest %s build. Bailing out.' % channel
       sys.exit(1)
    else:
       print 'Latest Chromium Version on %s at %s is %s' % (channel, status_url, version)
       return version

def download_version(version):

    file = 'chromium-%s.tar.bz2' % version
    path = '%s%s' % (chromium_url, file)

    # Let's make sure we haven't already downloaded it.
    if os.path.isfile("./%s" % file):
	print "%s already exists!" % file
    else:
	# Perhaps look at using python-progressbar at some point?
	urllib.urlretrieve(path, file, reporthook=dlProgress)
	urllib.urlcleanup()
	print ""

# This is where the magic happens
if __name__ == '__main__':

    # Locale magic
    locale.setlocale(locale.LC_ALL, '')

    # Create the parser object
    parser = argparse.ArgumentParser(description = my_description)

    parser.add_argument('--stable', action = 'store_true',
                        help = 'Get latest stable chromium source')
    parser.add_argument('--beta', action = 'store_true',
                        help = 'Get latest beta chromium source')
    parser.add_argument('--dev', action = 'store_true',
                        help = 'Get latest dev chromium source')

    # Parse the args
    args = parser.parse_args()

    if args.stable:
       chromium_version = check_omahaproxy("stable")
    else:
       if args.beta:
          chromium_version = check_omahaproxy("beta")
       else:
           if args.dev:
              chromium_version = check_latest()
           else:
              print 'You must select either stable, beta or dev'
              sys.exit(0)

    latest = 'chromium-%s.tar.bz2' % chromium_version

    download_version(chromium_version)

    # Lets make sure we haven't unpacked it already
    latest_dir = "%s/chromium-%s" % (chromium_root_dir, chromium_version)
    if os.path.isdir(latest_dir):
	print "%s already exists, perhaps %s has already been unpacked?" % (latest_dir, latest)
    else:
	# Okay, now we need to open that puppy up.
	print "Unpacking %s into %s, please wait." % (latest, latest_dir)
	tar = tarfile.open(latest, "r:bz2")
	tar.extractall(path=chromium_root_dir)
	tar.close

        junk_dirs = ['courgette', 'o3d', 
	             'third_party/WebKit/WebKitTools/Scripts/webkitpy/layout_tests', 
                     'webkit/data/layout_tests', 'third_party/hunspell/dictionaries', 
                     'chrome/test/data', 'native_client/tests', 
                     'third_party/WebKit/LayoutTests', 'v8/include', 'v8/src', 
                     'third_party/nss', 'third_party/nspr', 'third_party/icu', 
                     'third_party/expat/files', 
                     'third_party/ffmpeg/binaries', 
                     'third_party/ffmpeg/patched-ffmpeg-mt/',
                     'third_party/ffmpeg/ffpresets',
                     'third_party/ffmpeg/libavcodec',
                     'third_party/ffmpeg/libavdevice',
                     'third_party/ffmpeg/libavfilter',
                     'third_party/ffmpeg/libavformat',
                     'third_party/ffmpeg/libavutil',
                     'third_party/ffmpeg/libpostproc',
                     'third_party/ffmpeg/libswresample',
                     'third_party/ffmpeg/libswscale',
                     'third_party/zlib/contrib',
                     'third_party/speex',
                     'third_party/libevent/compat', 'third_party/libevent/linux',
                     'third_party/libevent/mac', 'third_party/libevent/sample', 
                     'third_party/libevent/test', 'third_party/libxml/build', 
                     'third_party/libxml/include', 'third_party/libxml/linux',
                     'third_party/libxml/mac', 'third_party/libxml/win32',
                     'third_party/libxslt/build', 'third_party/libxslt/libexslt',
                     'third_party/libxslt/libxslt', 'third_party/libxslt/linux',
                     'third_party/libxslt/mac', 'third_party/libxslt/win32',
                     'third_party/WebKit/WebCore/platform/image-decoders/zlib/']

        junk_files = ['third_party/bzip2/*.c', 'third_party/bzip2/*.h', 'third_party/bzip2/LICENSE',
                      'third_party/libjpeg/*.c', 'third_party/libjpeg/README*', 
                      'third_party/libpng/*.c', 'third_party/libpng/*.h', 'third_party/libpng/README*', 'third_party/libpng/LICENSE',
                      'third_party/zlib/*.c', 'third_party/zlib/*.h', 'third_party/zlib/README*',
                      'third_party/libevent/*.c', 'third_party/libevent/*.h', 'third_party/libevent/*sh', 'third_party/libevent/config*'
                      'third_party/libevent/*.3', 'third_party/libevent/README', 'third_party/libevent/ChangeLog', 
                      'third_party/libevent/Makefile.*', 'third_party/libevent/aclocal.m4', 'third_party/libevent/*.py', 
                      'third_party/libevent/missing', 'third_party/libevent/mkinstalldirs',
                      'third_party/libxml/*.c', 'third_party/libxml/*.h', 'third_party/libxml/*.in',
                      'third_party/libxml/*.m4', 'third_party/libxml/*.py', 'third_party/libxml/*.xml',
                      'third_party/libxml/missing', 'third_party/libxml/mkinstalldirs', 'third_party/libxml/*.1',
                      'third_party/libxml/AUTHORS', 'third_party/libxml/COPYING', 'third_party/libxml/ChangeLog',
                      'third_party/libxml/Copyright', 'third_party/libxml/INSTALL', 'third_party/libxml/NEWS',
                      'third_party/libxml/README', 'third_party/libxml/README.tests', 'third_party/libxml/TODO*',
                      'third_party/libxml/config*', 'third_party/libxml/*.pl',
                      'third_party/libxslt/AUTHORS', 'third_party/libxslt/COPYING', 'third_party/libxslt/ChangeLog',
                      'third_party/libxslt/FEATURES', 'third_party/libxslt/INSTALL', 'third_party/libxslt/NEWS',
                      'third_party/libxslt/README', 'third_party/libxslt/TODO', 'third_party/libxslt/*.h', 
                      'third_party/libxslt/*.m4', 'third_party/libxslt/compile', 'third_party/libxslt/config*',
                      'third_party/libxslt/depcomp', 'third_party/libxslt/*sh', 'third_party/libxslt/*.in',
                      'third_party/libxslt/*.spec', 'third_party/libxslt/missing', 'third_party/ffmpeg/*.c']

	# Ask Google what V8 this Chromium uses
	v8_checker_url = "http://omahaproxy.appspot.com/v8?version="
	v8sock = urllib.urlopen(v8_checker_url + chromium_version)
	v8_result_html = v8sock.read()
	start_index = v8_result_html.find('V8 Version:')
	end_index = v8_result_html.find(' <br>')
	v8_version = v8_result_html[start_index+12:end_index]

	print "Google claims that Chromium %s bundles V8 %s" % (chromium_version, v8_version)
	print "Download it here: http://gsdview.appspot.com/chromium-browser-official/v8-%s.tar.bz2" % v8_version

        # Lets look at what V8 version is bundled in.
        # v8_changelog = open('%s/v8/ChangeLog' % latest_dir, 'r')
        # v8_changelog_data = v8_changelog.readlines()
        # print "Bundled version of V8 is:"
        # print v8_changelog_data[0]

        # Okay, now we clean out the junk.

        # First, the dirs:
        for dir in junk_dirs: 
	    delete_chromium_dir(dir)

        # Then, the files:
        for file in junk_files:
	    delete_chromium_files(file)

        # There has got to be a better, more portable way to do this.
        os.system("find %s -depth -name reference_build -type d -exec rm -rf {} \;" % latest_dir)

        # I could not find good bindings for xz/lzma support, so we system call here too.

        chromium_clean_xz_file = "chromium-" + chromium_version + "-clean.tar.lzma"

        if os.path.isfile("%s/%s" % (chromium_root_dir, chromium_clean_xz_file)):
             print "%s already exists!" % chromium_clean_xz_file
        else:
	     print "Compressing cleaned tree, please wait..."
	     os.chdir(chromium_root_dir)
	     os.system("tar --exclude=\.svn -cf - chromium-%s | xz -9 -F lzma > %s" % (chromium_version, chromium_clean_xz_file))
	     print "done!"
