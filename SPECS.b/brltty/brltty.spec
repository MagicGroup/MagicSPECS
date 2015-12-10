%define pkg_version 5.2
%define api_version 0.6.3

%global with_python3 1

%if 0%{?rhel}
%global with_python3 0
%endif

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_prefix}/%{_lib}/tcl%{tcl_version}}

# with speech dispatcher iff on Fedora:
%define with_speech_dispatcher 1

%global with_ocaml 1

# Filter private libraries
%global _privatelibs libbrltty.+\.so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

Name: brltty
Version: %{pkg_version}
Release: 11%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://mielke.cc/brltty/
Source0: http://mielke.cc/brltty/archive/%{name}-%{version}.tar.xz
Source1: brltty.service
Patch4: brltty-loadLibrary.patch
# libspeechd.h moved in latest speech-dispatch (NOT sent upstream)
Patch5: brltty-5.0-libspeechd.patch
Patch6: brltty-5.2-man-fix.patch
Summary: Braille display driver for Linux/Unix
BuildRequires: byacc glibc-kernheaders bluez-libs-devel
BuildRequires: gettext, at-spi2-core-devel, espeak-devel
# work around a bug in the install process:
Requires(post): coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
BRLTTY is a background process (daemon) which provides
access to the Linux/Unix console (when in text mode)
for a blind person using a refreshable braille display.
It drives the braille display and provides complete
screen review functionality.
%if %{with_speech_dispatcher}
BRLTTY can also work with speech synthesizers; if you want to use it with
Speech Dispatcher, please install also package %{name}-speech-dispatcher.

%package speech-dispatcher
Summary: Speech Dispatcher driver for BRLTTY
Group: System Environment/Daemons
License: GPLv2+
BuildRequires: speech-dispatcher-devel
Requires: %{name} = %{pkg_version}-%{release}
%description speech-dispatcher
This package provides the Speech Dispatcher driver for BRLTTY.
%endif

%package docs
Summary: Documentation for BRLTTY
Group: System Environment/Daemons
License: GPLv2+
Requires: %{name} = %{pkg_version}-%{release}
BuildArch: noarch
%description docs
This package provides the documentation for BRLTTY.

%package xw
Summary: XWindow driver for BRLTTY
Group: System Environment/Daemons
License: GPLv2+
BuildRequires: libSM-devel libICE-devel libX11-devel libXaw-devel libXext-devel libXt-devel libXtst-devel
Requires: %{name} = %{pkg_version}-%{release}
%description xw
This package provides the XWindow driver for BRLTTY.

%package at-spi2
Summary: AtSpi driver for BRLTTY
Group: System Environment/Daemons
# The data files are licensed under LGPLv2+, see the README file.
License: GPLv2+ and LGPLv2+
Requires: %{name} = %{pkg_version}-%{release}
%description at-spi2
This package provides the AtSpi driver for BRLTTY.

%package -n brlapi
Version: %{api_version}
Group: Applications/System
License: LGPLv2+
Summary: Application Programming Interface for BRLTTY
Requires: %{name} = %{pkg_version}-%{release}
Requires(pre): glibc-common, shadow-utils
Requires(post): coreutils, util-linux
%description -n brlapi
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n brlapi-devel
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
Summary: Headers, static archive, and documentation for BrlAPI

%description -n brlapi-devel
This package provides the header files, static archive, shared object
linker reference, and reference documentation for BrlAPI (the
Application Programming Interface to BRLTTY).  It enables the
implementation of applications which take direct advantage of a
refreshable braille display in order to present information in ways
which are more appropriate for blind users and/or to provide user
interfaces which are more specifically attuned to their needs.

Install this package if you are developing or maintaining an application
which directly accesses a refreshable braille display.

%package -n tcl-brlapi
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
BuildRequires: tcl-devel
Summary: Tcl binding for BrlAPI
%description -n tcl-brlapi
This package provides the Tcl binding for BrlAPI.

%package -n python-brlapi
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
BuildRequires: Cython
BuildRequires: python2-devel
BuildRequires: python-setuptools
Summary: Python binding for BrlAPI
%description -n python-brlapi
This package provides the Python binding for BrlAPI.

%if 0%{?with_python3}
%package -n python3-brlapi
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
BuildRequires: Cython
BuildRequires: python3-devel
Summary: Python 3 binding for BrlAPI
%description -n python3-brlapi
This package provides the Python 3 binding for BrlAPI.
%endif

%package -n brlapi-java
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
BuildRequires: jpackage-utils
BuildRequires: java-devel
Summary: Java binding for BrlAPI
%description -n brlapi-java
This package provides the Java binding for BrlAPI.

%if 0%{?with_ocaml}
%package -n ocaml-brlapi
Version: %{api_version}
Group: Development/System
License: LGPLv2+
Requires: brlapi = %{api_version}-%{release}
BuildRequires: ocaml
Summary: OCaml binding for BrlAPI
%description -n ocaml-brlapi
This package provides the OCaml binding for BrlAPI.
%endif


%define version %{pkg_version}

%prep
%setup -q
%patch4 -p1 -b .loadLibrary
%patch5 -p1
%patch6 -p1 -b .man-fix

%if 0%{?with_python3}
# Make a copy of the source tree for building the Python 3 module
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
# If MAKEFLAGS=-jN is set it would break local builds.
unset MAKEFLAGS

# Add the openjdk include directories to CPPFLAGS
for i in -I/usr/lib/jvm/java/include{,/linux}; do
      java_inc="$java_inc $i"
done
export CPPFLAGS="$java_inc"

export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

# there is no curses packages in BuildRequires, so the package builds
# without them in mock; let's express this decision explicitly
configure_opts=" \
  --disable-stripping \
  --without-curses \
%if %{with_speech_dispatcher}
  --with-speechd=%{_prefix} \
%endif
  --with-install-root=$RPM_BUILD_ROOT
  JAVA_JAR_DIR=%{_jnidir} \
  JAVA_JNI_DIR=%{_libdir}/brltty \
  JAVA_JNI=yes"

# First build everything with Python 2 support
%configure $configure_opts PYTHON=%{__python2}
# Parallel build seems broken, thus disabling it
make

%if 0%{?with_python3}
# ... and then do it again for the Python 3 module
pushd %{py3dir}
%configure $configure_opts PYTHON=%{__python3}
# Parallel build seems broken, thus disabling it
make
popd
%endif

find . \( -path ./doc -o -path ./Documents \) -prune -o \
  \( -name 'README*' -o -name '*.txt' -o -name '*.html' -o \
     -name '*.sgml' -o -name '*.patch' -o \
     \( -path './Bootdisks/*' -type f -perm /ugo=x \) \) -print |
while read file; do
   mkdir -p doc/${file%/*} && cp -rp $file doc/$file || exit 1
done

find . -name '*.sgml' |
while read file; do
   iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
done
find . -name '*.txt' |
while read file; do
   iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
done
find . -name 'README*' |
while read file; do
   iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
done

%install
%if 0%{?with_ocaml}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
%endif

# Python 2
make install JAVA_JAR_DIR=%{_jnidir} \
             JAVA_JNI_DIR=%{_libdir}/brltty \
             JAVA_JNI=yes

%if 0%{?with_python3}
# Python 3
pushd %{py3dir}
make install JAVA_JAR_DIR=%{_jnidir} \
             JAVA_JNI_DIR=%{_libdir}/brltty \
             JAVA_JNI=yes
popd
%endif

install -d -m 755 "${RPM_BUILD_ROOT}%{_sysconfdir}" "$RPM_BUILD_ROOT%{_mandir}/man5"
install -m 644 Documents/brltty.conf "${RPM_BUILD_ROOT}%{_sysconfdir}"
echo ".so man1/brltty.1" > $RPM_BUILD_ROOT%{_mandir}/man5/brltty.conf.5

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/brltty.service

# clean up the manuals:
rm Documents/Manual-*/*/{*.mk,*.made,Makefile*}
mv Documents/BrlAPIref/{html,BrlAPIref}

# Don't want static lib
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libbrlapi.a

# ghost brlapi.key
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/brlapi.key

# disable xbrlapi gdm autostart, there is already orca
rm -f ${RPM_BUILD_ROOT}%{_datadir}/gdm/greeter/autostart/xbrlapi.desktop

# handle locales
%find_lang %{name}

%post
%systemd_post brltty.service

%preun
%systemd_preun brltty.service

%postun
%systemd_postun_with_restart brltty.service

%pre -n brlapi
getent group brlapi >/dev/null || groupadd -r brlapi >/dev/null

%post -n brlapi
if [ ! -e %{_sysconfdir}/brlapi.key ]; then
  mcookie > %{_sysconfdir}/brlapi.key
  chgrp brlapi %{_sysconfdir}/brlapi.key
  chmod 0640 %{_sysconfdir}/brlapi.key
fi
/sbin/ldconfig

%postun -n brlapi -p /sbin/ldconfig

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/brltty.conf
%{_sysconfdir}/brltty/
%{_unitdir}/brltty.service
%{_bindir}/brltty
%{_bindir}/brltty-*
%{_libdir}/brltty/
%exclude %{_libdir}/brltty/libbrlttybba.so
%exclude %{_libdir}/brltty/libbrlttybxw.so
%exclude %{_libdir}/brltty/libbrlapi_java.so
%if %{with_speech_dispatcher}
%exclude %{_libdir}/brltty/libbrlttyssd.so
%endif
%exclude %{_libdir}/brltty/libbrlttyxas.so
%doc LICENSE-GPL LICENSE-LGPL
%doc %{_mandir}/man[15]/brltty.*

%if %{with_speech_dispatcher}
%files speech-dispatcher
%doc Drivers/Speech/SpeechDispatcher/README
%{_libdir}/brltty/libbrlttyssd.so
%endif

%files docs
%doc Documents/ChangeLog Documents/TODO
%doc Documents/Manual-BRLTTY/
%doc doc/*

%files xw
%doc Drivers/Braille/XWindow/README
%{_libdir}/brltty/libbrlttybxw.so

%files at-spi2
%{_libdir}/brltty/libbrlttyxa2.so

%files -n brlapi
%{_bindir}/vstp
%{_bindir}/eutp
%{_bindir}/xbrlapi
%{_libdir}/brltty/libbrlttybba.so
%{_libdir}/libbrlapi.so.*
%ghost %{_sysconfdir}/brlapi.key
%doc Drivers/Braille/XWindow/README
%doc Documents/Manual-BrlAPI/
%doc %{_mandir}/man1/xbrlapi.*
%doc %{_mandir}/man1/vstp.*
%doc %{_mandir}/man1/eutp.*

%files -n brlapi-devel
%{_libdir}/libbrlapi.so
%{_includedir}/brltty
%{_includedir}/brlapi*.h
%doc %{_mandir}/man3/brlapi_*.3*
%doc Documents/BrlAPIref/BrlAPIref/

%files -n tcl-brlapi
%{tcl_sitearch}/brlapi-%{api_version}

%files -n python-brlapi
%{python_sitearch}/brlapi.so
%{python_sitearch}/Brlapi-%{api_version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-brlapi
%{python3_sitearch}/brlapi.cpython-*.so
%{python3_sitearch}/Brlapi-%{api_version}-*.egg-info
%endif

%files -n brlapi-java
%{_libdir}/brltty/libbrlapi_java.so
%{_jnidir}/brlapi.jar

%if 0%{?with_ocaml}
%files -n ocaml-brlapi
%{_libdir}/ocaml/brlapi/
%{_libdir}/ocaml/stublibs/
%endif

%changelog
* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 5.1-11
- 为 Magic 3.0 重建

* Wed Nov 25 2015 Liu Di <liudidi@gmail.com> - 5.1-10
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 5.1-9
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 5.1-8
- 为 Magic 3.0 重建

* Thu Mar 05 2015 Liu Di <liudidi@gmail.com> - 5.1-7
- 为 Magic 3.0 重建

* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 5.1-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.1-3
- Rebuilt for tcl/tk8.6

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Thu Mar 27 2014 Jon Ciesla <limburgher@gmail.com> - 5.1-1
- 5.1, BZ 1081459.
- Fixed Source URL.

* Thu Feb 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.0-1
- New version
  Resolves: rhbz#1067337
- Dropped man-fix patch (upstreamed)
- De-fuzzified libspeechd patch
- Handled locales
- Switched to xz compressed sources

* Thu Feb 13 2014 Jon Ciesla <limburgher@gmail.com> - 4.5-10
- libicu rebuild.
- Add python-setuptools BR.

* Mon Sep 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-9
- The brlapi.key is now preset, users in the brlapi group have access
  Resolves: rhbz#1010656

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.5-8
- Rebuild for OCaml 4.01.0.
- Create stublibs directory for OCaml, else install fails.
- Unset MAKEFLAGS so that MAKEFLAGS=-j<N> does not break local builds.
- In new speech-dispatcher, <libspeechd.h> has moved to a subdirectory.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-6
- Updated man page

* Fri May 10 2013 Jon Ciesla <limburgher@gmail.com> - 4.5-5
- Add systemd unit file, BZ 916628.
- Drop spurious post scripts.
- Move eveything but man pages and license files top -docs.

* Thu May  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-4
- Conditionally build python3

* Tue Apr 30 2013 Jon Ciesla <limburgher@gmail.com> - 4.5-3
- Add bluetooth support, BZ 916628.

* Thu Apr 04 2013 Kalev Lember <kalevlember@gmail.com> - 4.5-2
- Don't install the library in /lib now that we have UsrMove

* Thu Apr 04 2013 Kalev Lember <kalevlember@gmail.com> - 4.5-1
- Update to 4.5
- Add Python 3 support (python3-brlapi)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.3-12
- Build with -fno-strict-aliasing

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.3-11
- revbump after jnidir change

* Wed Dec 12 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.3-10
- Fixed directories, install to /usr prefix

* Wed Dec 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.3-9
- Fix up java subpackage installation directories
- Fix java JNI loading code

* Wed Oct 17 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-8
- Bump and rebuild for new ocaml.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-6
- Bump and rebuild for ocaml 4.00.0.

* Fri Mar 23 2012 Dan Horák <dan[at]danny.cz> - 4.3-5
- conditionalize ocaml support
- fix build on 64-bit arches

* Mon Feb 06 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-4
- Added ocaml subpackage, BZ 702724.

* Fri Feb 03 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-3
- Fixed libbrlapi.so symlink, BZ 558132.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Jon Ciesla <limb@jcomserv.net> - 4.3-1
- New upstream.
- S_ISCHR patch upstreamed.
- parallel patch updated.
- Cleaned up some file encodings.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.2-2
- rework parallel patch slightly and reapply

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.2-1
- update to 4.2
- drop static lib (bz 556041)
- fix undefined S_ISCHR call

* Wed Jan 20 2010 Stepan Kasal <skasal@redhat.com> - 4.1-5
- requires(post): coreutils to work around an installator bug
- Resolves: #540437

* Wed Jan 13 2010 Stepan Kasal <skasal@redhat.com> - 4.1-4
- limit building against speech-dispatcher to Fedora
- Resolves: rhbz#553795

* Sun Nov  1 2009 Stepan Kasal <skasal@redhat.com> - 4.1-3
- build the TTY driver (it was disabled since it first appered in 3.7.2-1)
- build with speech-dispatcher, packed into a separate sub-package

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 4.1-2
- move data-directory back to default: /etc/brltty
- move brltty to /bin and /lib, so that it can be used to repair the system
  without /usr mounted (#276181)
- move vstp and libbrlttybba.so to brlapi
- brltty no longer requires brlapi
- brlapi now requires brltty from the same build

* Wed Oct 28 2009 Stepan Kasal <skasal@redhat.com> - 4.1-1
- new upstream version
- use --disable-stripping instead of make variable override
- install the default brltty-pm.conf to docdir only (#526168)
- remove the duplicate copies of rhmkboot and rhmkroot from docdir
- patch configure so that the dirs in summary are not garbled:
  brltty-autoconf-quote.patch
- move data-directory to ${datadir}/brltty

* Tue Oct 20 2009 Stepan Kasal <skasal@redhat.com> - 4.0-2
- escape rpm macros in the rpm change log
- add requires to bind subpackages from one build together

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 4.0-1
- new upstream version
- drop upstreamed patches; ./autogen not needed anymore
- pack the xbrlapi server; move its man page to brlapi package
- add man-page for brltty.conf (#526168)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Stepan Kasal <skasal@redhat.com> - 3.10-5
- rebuild after java-1.5.0-gcj rebuild

* Thu Apr 30 2009 Stepan Kasal <skasal@redhat.com> - 3.10-4
- own the tcl subdirectory (#474032)
- set CPPFLAGS to java include dirs, so that the java bindings build with
  any java implementation (#498964)
- add --without-curses; there is no curses package BuildRequired anyway

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.10-2
- Rebuild for Python 2.6

* Sat Sep 13 2008 Stepan Kasal <skasal@redhat.com> - 3.10-1
- new upstream release
- drop brltty-3.9-java-svn.patch, brltty-3.9-tcl85path.patch,
  and brltty-3.9-pyxfix.patch, they are upstream
- fix BuildRoot
- fix many sub-packages' Requires on brlapi

* Wed Sep 10 2008 Stepan Kasal <skasal@redhat.com> - 3.9-3
- add brltty-3.9-autoconf.patch to fix to build with Autoconf 2.62
- add brltty-3.9-parallel.patch to fix race condition with parallel make
- add brltty-3.9-pyxfix.patch to fix build with current pyrex
- Summary lines shall not end with a dot

* Thu Feb 28 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-2.2
- glibc build fixes
- applied java reorganisations from svn

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.9-2.1
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-1.1
- specfile update to comply with tcl packaging guidelines

* Mon Jan 07 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-1
- update to latest upstream (3.9)

* Tue Sep 18 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-2.svn3231
- update to r3231 from svn
- added java binding subpackage

* Wed Aug 29 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-2.svn3231
- update to r3231 from svn

* Tue Aug 21 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-1
- update to latest upstream
- added the at-spi driver, tcl and python bindings
- fixed the license tags

* Mon Mar 05 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-3
- added the XWindow driver
- build fix for newer byacc

* Tue Jan 30 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-2.1
- quiet postinstall scriptlet, really fixes #224570

* Tue Jan 30 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-2
- failsafe postinstall script, fixes #224570
- makefile fix - debuginfo extraction now works

* Thu Jan 25 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-1.1
- fix building with newer kernel-headers (#224149)

* Wed Jul 12 2006 Petr Rockai <prockai@redhat.com> - 3.7.2-1
- upgrade to latest upstream version
- split off brlapi and brlapi-devel packages

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2-12.1
- rebuild

* Sun Jul 02 2006 Florian La Roche <laroche@redhat.com>
- for the post script require coreutils

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.2-11
- Added byacc BuildRequires, removed prereq, coreutils is always there

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2-10.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2-10.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Bill Nottingham <notting@redhat.com> 3.2-10
- rebuild

* Fri Nov 26 2004 Florian La Roche <laroche@redhat.com>
- add a %%clean into .spec

* Thu Oct 14 2004 Adrian Havill <havill@redhat.com> 3.2-5
- chmod a-x for conf file (#116244)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq coreutils for mknod/chown/chmod

* Mon Jul 07 2003 Adrian Havill <havill@redhat.com> 3.2-2
- changed spec "Copyright" to "License"
- use %%configure macro, %%{_libdir} for non-ia32 archs
- removed unnecessary set and unset, assumed/default spec headers
- fixed unpackaged man page, duplicate /bin and /lib entries
- use plain install vs scripts for non-i386 buildsys
