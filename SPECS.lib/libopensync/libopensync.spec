%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:           libopensync
Epoch:          1
Version:        0.22
Release:        12%{?dist}
Summary:        A synchronization framework
Summary(zh_CN.UTF-8): 一个同步框架

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.opensync.org/
Source0:        http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
Patch0:         libopensync-wrapper-err.patch
Patch1:         libopensync-0.22-unusedvar.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  sqlite-devel
BuildRequires:  python-devel
BuildRequires:  swig
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  chrpath

# For now (workaround for SWIG major-version bump)
BuildRequires:  autoconf

# provide clean downgrade path
Provides: libopensync-plugin-kdepim = 0:0.36-2
Obsoletes: libopensync-plugin-kdepim <= 0:0.36-2
Provides: libopensync-plugin-vformat = 0:0.36-2
Obsoletes: libopensync-plugin-vformat <= 0:0.36-2

%description
OpenSync is a synchronization framework that is platform and distribution
independent. It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself. The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files. 

%description -l zh_CN.UTF-8
一个同步框架。

%package devel
Summary:        Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       glib2-devel
Requires:       libxml2-devel
Requires:       sqlite-devel

%description    devel
The %{name}-devel package contains the files needed for development
with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0
%patch1 -p1 -b .unusedvar

# Fixup expected version of SWIG:
sed -i -e "s|AC_PROG_SWIG(1.3.17)|AC_PROG_SWIG(3.0.0)|" configure.in
# and rebuild the configure script:
autoconf

find . -type f -name *.c -exec chmod 644 {} \;
find . -type f -name *.h -exec chmod 644 {} \;

%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-error"
%configure --disable-static
make %{?_smp_mflags}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name *.la -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name *.a -exec rm -f {} \;

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/opensync
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/opensync/formats
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/opensync/{python-,}plugins

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/osync*
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/osplugin
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libosengine.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/opensync/formats/*so
chrpath --delete $RPM_BUILD_ROOT%{python_sitearch}/_opensync.so
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_libexecdir}/osplugin
%dir %{_libdir}/opensync
%dir %{_libdir}/opensync/formats
%dir %{_libdir}/opensync/python-plugins
%dir %{_libdir}/opensync/plugins
%{_libdir}/opensync/formats/*
%dir %{_datadir}/opensync
%{python_sitearch}/*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%dir %{_includedir}/opensync-1.0
%{_includedir}/opensync-1.0/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:0.22-10
- fix ftbfs (rhbz#716135)
- fix rpath

* Tue Feb 22 2011 Karsten Hopp <karsten@redhat.com> 0.22-9
- fix failure with -Werror=unused-but-set-variable, libopensync-0.22-unusedvar.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 1:0.22-7
- the SWIG major-version bump led to SWIG_LIB not being set in configure,
leading to python bindings not being built.  Work around this by bumping the
expected version in the configure file

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 25 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:0.22-4
- add patch for werr build failure

* Tue Feb 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:0.22-3
- fix rpath on x86_64
- cleanup

* Tue Feb 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:0.22-2
- reference versions with epoch

* Fri Feb 06 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1:0.22-1
- downgrade to 0.22 (#474070)
- build devel docs

* Fri Jan 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.36-5
- fix swig version


* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.36-4
- Rebuild for Python 2.6

* Sat Sep 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.36-3
- upgrade for new swig

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.36-2
- Rebuilt for gcc43

* Mon Jan 28 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.36-1
- version upgrade

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.35-2
- use cmake macro

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.35-1
- version upgrade

* Sun Oct 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.33-1
- version upgrade

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.22-4
- new license tag
- rebuild for buildid

* Thu Apr 26 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.22-3
- fix typo

* Wed Apr 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.22-2
- fix #228375

* Wed Apr 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.22-1
- version upgrade #231845

* Wed Dec 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.20-1
- version upgrade #217150

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu>
0.19-2
- Rebuild for new Python

* Thu Oct 12 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.19-1
- version upgrade #210443 #209281

* Wed Sep 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-7
- FE6 rebuild

* Wed Feb 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-6
- Rebuild for Fedora Extras 5

* Tue Dec 13 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-5
- change handling of ld.so.conf files
- patch configure for x86_64 python
- add wrapper compile patch (no Werror)

* Sun Dec 11 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-4
- add dist

* Sun Dec 11 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-3
- .c and .h files should not be marked executable

* Sun Dec 04 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-2
- fix missing BR
- mark ldconf as config

* Sat Nov 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.18-1
- Version upgrade

* Mon Oct 03 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.17-1
- Initial Release
