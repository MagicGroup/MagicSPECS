<<<<<<< HEAD
%define git 1
%define vcsdate 20150413
=======
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
%global gitrev f9ca1a4
# gitrev is output of: git rev-parse --short HEAD

%if 0%{?rhel} != 0 && 0%{?rhel} <= 7
# Do not build bindings for python3 for RHEL <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           librepo
<<<<<<< HEAD
Version:        1.7.14
%if 0%{git}
Release:        0.git%{vcsdate}%{?dist}.1
%else
Release:	2%{?dist}
%endif
=======
Version:        1.7.5
Release:        2%{?dist}
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
Summary:        Repodata downloading library
Summary(zh_CN.UTF-8): Repo 数据下载库
 
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            https://github.com/Tojaj/librepo
# Use the following commands to generate the tarball:
#  git clone https://github.com/Tojaj/librepo.git
#  cd librepo
#  utils/make_tarball.sh %{gitrev}
<<<<<<< HEAD
%if 0%{git}
Source0:	librepo-git%{vcsdate}.tar.xz
%else
Source0:        librepo-%{gitrev}.tar.xz
%endif
Source1:	make_librepo_git_package.sh
=======
Source0:        librepo-%{gitrev}.tar.xz
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697

BuildRequires:  check-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  glib2-devel >= 2.22.0
BuildRequires:  gpgme-devel
BuildRequires:  libattr-devel
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel

# prevent provides from nonstandard paths:
%filter_provides_in %{python_sitearch}/.*\.so$
%if %{with python3}
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
%filter_setup

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%description -l zh_CN.UTF-8
Repo 数据下载库。

%package devel
Summary:        Repodata downloading library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for librepo.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n python-librepo
Summary:        Python bindings for the librepo library
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildRequires:  pygpgme
BuildRequires:  python2-devel
BuildRequires:  python-flask
BuildRequires:  python-nose
BuildRequires:  python-sphinx
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python-librepo
Python bindings for the librepo library.

%description -n python-librepo -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%if %{with python3}
%package -n python3-librepo
Summary:        Python 3 bindings for the librepo library
Summary(zh_CN.UTF-8): %{name} 的 Python3 绑定
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
BuildRequires:  python3-pygpgme
BuildRequires:  python3-devel
BuildRequires:  python3-flask
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-librepo
Python 3 bindings for the librepo library.

%description -n python3-librepo -l zh_CN.UTF-8
%{name} 的 Python3 绑定。
%endif

%prep
<<<<<<< HEAD
%if 0%{git}
%setup -q -n librepo-git%{vcsdate}
%else
%setup -q -n librepo
%endif
=======
%setup -q -n librepo
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697

%if %{with python3}
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./
%endif

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make %{?_smp_mflags}

%if %{with python3}
pushd py3
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DPYTHON_DESIRED:str=3 .
make %{?_smp_mflags}
popd
%endif

%check
make ARGS="-V" test

%if %{with python3}
pushd py3
make ARGS="-V" test
popd
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
%if %{with python3}
pushd py3
make install DESTDIR=$RPM_BUILD_ROOT
popd
%endif
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README.md
%{_libdir}/librepo.so.*

%files devel
%{_libdir}/librepo.so
%{_libdir}/pkgconfig/librepo.pc
%{_includedir}/librepo/

%files -n python-librepo
%{python_sitearch}/librepo/

%if %{with python3}
%files -n python3-librepo
%{python3_sitearch}/
%endif

%changelog
<<<<<<< HEAD
* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 1.7.14-0.git20150413.1
- 更新到 20150413 日期的仓库源码

* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 1.7.14-0.git20150402.1
- 为 Magic 3.0 重建

=======
>>>>>>> 54cb407384ac63300039a28ea6cd00ef0bab6697
* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.7.5-2
- 为 Magic 3.0 重建

* Tue Jul  8 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.5-1
- accepts unicoded destination as UTF-8 string (Related: RhBug:1108908)
- downloader: Do not print debug message about preparing internal mirror list
  if no internal mirror is available
- fastestmirror: subtract name lookup (dns) time from plain connect time
- fastestmirror: Small refactoring

* Thu Jun 26 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.4-3
- Increase default value of LRO_LOWSPEEDTIME from 10 to 30 (RhBug: 1109189)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun   2 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.4-1
- Add LRO_IPRESOLVE option to set a kind of IP addresses to use when resolving host names
- Relicenced from GPLv2 to LGPLv2+
- error mesage is in unicode (RhBug:1096452)

* Tue May   6 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.3-1
- Fix some issues which were found by coverity scan
- Add missing support for Handle Mirror Failure Callback (hmfcb)
  while downloading repomd.xml (related to RhBug: 1093014)
- Add LRO_SSLVERIFYPEER and LRO_SSLVERIFYHOST options (RhBug: 1093014)

* Wed Apr  23 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.2-1
- Fix segfault in headercb if only base_url and no mirrolist is used (RhBug: 1090325)
- Set environmental variable LIBREPO_DEBUG enables librepo debug output to stderr

* Mon Apr   7 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.1-1
- Don't try to call cb if no cb is set (RhBug: 1083659)

* Mon Mar  31 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.7.0-1
- Support for xml:base tag in repomd.xml.
- Downloader: If checksums don't match, include the expected values and types
  in the error message.
- Handle: Add LRO_HMFCB and LRI_HMFCB options.
- API CHANGE: lr_download_single_cb() new param mfcb (LrMirrorFailureCb)
- API CHANGE: Removed cbdata param from lr_download_single_cb(). Use specific
  data for each target.
- New callback LrHandleMirrorFailureCb
- Python doc update (Check it out: http://tojaj.github.io/librepo/)

* Thu Mar 27 2014 Matěj Cepl <mcepl@redhat.com> - 1.6.0-2
- Make building of python3 components conditional
- replace all TABs with spaces

* Thu Feb  20 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.6.0-1
- Small API change: End callback now must return integer and not void)
- downloader: Check for the lr_interrupt regularly
- Handle exceptions in python callbacks as return values (RhBug: 1066321)
- Support for byterange of download (RhBug: 1058777)

* Tue Jan  28 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.5.2-2
- Ignore rsyc mirrors silently.

* Thu Jan  16 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.5.2-1
- Better download resume logic

* Fri Jan   3 2014 Tomas Mlcoch <tmlcoch at redhat.com> - 1.5.1-1
-  Downloading: LRO_MAXSPEED has effect over whole downloading, it is not
   per target max speed anymore.
-  Sanitize progresscb (GitHub issue 24) (Thanks zde/zpavlas)

* Tue Dec  17 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.5.0-1
- Extend C example
- Add LRR_YUM_TIMESTAMP (GitHub issue #25)
- Close the correct file when using a metalink.xml file
- Add lr_check_packages()
- Enable checksum caching for already existing local packages
- Library: Call LR_PROGRESSCB with zeroized values, when total_to_download
  value is changed
- Skip fastestmirror detection of only one mirror is present

* Tue Nov  19 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.4.0-1
- Add LRO_FASTESTMIRRORCB
- Add LRO_LOWSPEEDTIME and LRO_LOWSPEEDLIMIT options. (RhBug: 1028444)
- Default connection timeout changed to 30sec instead of 300sec.
- unittests: Fix expired key (RhBug: 1031825)

* Thu Oct  31 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.3.0-1
- Some CURL error codes should be considered as fatal (RhBug: 1022994)
- fastestmirror: Add support for cache - New options: LRO_FASTESTMIRRORCACHE
  and LRO_FASTESTMIRRORMAXAGE
- fastestmirror: For download_packages() do fastestmirror detection for
  all handles in one shot
- Use <mm0:alternates> during repomd.xml download (RhBug: 1019103)
- Don't perform fastest mirror test if file already exists locally.
- fastestmirror.h:26:24: fatal error: mirrorlist.h: No such file
  or directory (#1018006)

* Mon Oct  07 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.2.1-1
- Open fd right before downloading and close them immediately after
  download. (RhBug: 1015957)

* Thu Oct  03 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.2.0-2
- Add target for Python 3 to the spec file
- Fix few python3 related issues

* Tue Oct  01 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.2.0-1
- Better detection of bad content of repomd.xml
- Close files properly (RhBug: 1012290)
- Add fastestmirror module + LRO_FASTESTMIRROR option
- downloader: Fix uninitialized total to download variable (GitHub issue 22)
- Add LRO_MIRRORLISTURL and LRO_METALINKURL. LRO_MIRRORLIST is deprecated.
- Few other small fixes

* Mon Sep  16 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.1.0-1
- New librepo.download_url(url, fd, handle=None) function in Python API.
- Low-level downloader interface is now public in C API.
- Small change of API lr_download_packages() and lr_packagetarget_new
  functions.
- In python download_packages() changed from method of Handle() to
  librepo module function without handle param.
  Param handle was moved to the PackageTarget class that takes handle
  as a optional param during constrution.
- Implements checking size of downloaded files (expectedsize
  param of downloading functions).

* Wed Aug  28 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 1.0.0-1
- Huge API changes
- Library starts to use GLib2
- Support for parallel downloads
- Better error reporting
- More GLib2 style C api
- More descriptive Python exception messages
- A lot of bugfixes
- Updated examples

* Thu Jul  25 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.5-3
- python: Raise exception if handle has bad repo type configured
  (RhBug: 988013)

* Mon Jul  22 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.5-2
- Bump version in versioh.h to 0.0.5
- Python: Fix Handle.mirrors to return empty list instead of None if
  no mirrors available (RhBug: 986228)

* Wed Jul  17 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.5-1
- Return LRE_ALREADYDOWNLOADED if the file exists even if no resume
  is specified. (GitHub issue 15)
- downloadtarget: New module, future replacement for curltarget module.
- Librepo migrated to lr_LrMirrorlist from lr_InternalMirrorlist.
- test: Run python unittest verbosely
- lrmirrorlis: New module. GLib2 ready replacement for the internal_mirrorlist
  module.
- package_downloader: Add LRE_ALREADYDOWNLOADED rc code. (GitHub issue 15)
- handle: After set python SIGINT handler back, check if librepo was
  interrupted by CTRL+C. (RhBug: 977803)
- cmake: Set required python version to 2. (GitHub issue 10)
- Fix missing VAR substitution for mirrorlist. (GitHub issue 11)
- cmake: Add FindXattr module.
- Add support for caching checksum as extended file attribute. (GitHub issue 8)
- util: Add lr_asprintf().
- util: Add lr_vasprintf().
- handle: Fix funky logic in internal error handling. (GitHub issue 9)
- Add lr_yum_repomd_get_age() function. (GitHub issue 6)
- test: Add test for LR_VERSION_CHECK macro.
- Add a LR_VERSION_CHECK macro

* Wed Jun 12 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.4-2
- examples: Add C example of usage.
- Fix predefined lists in types.h (GitHub issue 4). Thank you hughsie
- Add LRO_VARSUB and LRI_VARSUB. (RhBug: 965131)
- py: Change reported name from _librepo.Exception to librepo.LibrepoException

* Thu May  2 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.4-1
- Fix type conversion long long -> long.(RhBug: 957656)
- python: Handle.perfrom() could be called without Result().
- Add LRI_MAXMIRRORTRIES option. (RhBug: 954736)
- py: unittests: Add metalink.xml and mirrorlist files. (RhBug: 954294)
- Fix double free and memory leak. (RhBug: 954294)
- New option LRO_MAXMIRRORTRIES. (RhBug: 949517)
- LRI_MIRRORS return only content of mirrorlist file (without LRO_URL as first item).
- Add LRO_FETCHMIRRORS option.

* Mon Apr  8 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.2-3.git720d68d
- Add CURL_GLOBAL_ACK_EINTR flag to curl init.
- Proper multi handle cleanup. (RhBug: 947388)
- Support for read 'useragent' attr. (RhBug: 947346)
- Add valgrind supress files. (RhBug: 923214)
- Make python bindings interruptible (LRO_INTERRUPTIBLE) (RhBug: 919125)
- Add LRI_MIRRORS option (RhBug: 923198)
- Add LRI_METALINK option. (BzBug: 947767)

* Mon Mar 18 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.2-2.gitb3c3323
- py: Use standard python exception while accessing bad attrs. (RhBug: 920673)
- Default mask for newly created files is 0666. (RhBug: 922557)

* Thu Mar 14 2013 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.2-1.git714e828
- Add LRI_PROGRESSCB and LRI_PROGRESSDATA options (RhBug: 919123)
- Bindings: More pythonic operations with handle's attributes (RhBug: 919124)

* Tue Oct  9 2012 Tomas Mlcoch <tmlcoch at redhat.com> - 0.0.1-1.gitc69642e
- Initial package
