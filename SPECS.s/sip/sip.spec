%if 0%{?fedora} > 12
%global with_python3 1
%endif

%if 0%{?with_python3}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%endif
%{!?__python2:%global __python2 /usr/bin/python2}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: SIP - Python/C++ Bindings Generator
Name: sip
Version: 4.16.7
Release: 1%{?dist}

# sipgen/parser.{c.h} is GPLv3+ with exceptions (bison)
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)
Url: http://www.riverbankcomputing.com/software/sip/intro 
#URL: http://sourceforge.net/projects/pyqt/
Source0:  http://downloads.sourceforge.net/pyqt/sip-%{version}%{?snap:-snapshot-%{snap}}.tar.gz

## upstreamable patches
# make install should not strip (by default), kills -debuginfo
Patch50: sip-4.16.3-no_strip.patch
# try not to rpath the world
Patch51: sip-4.16.3-no_rpath.patch

## upstream patches

# extracted from sip.h, SIP_API_MAJOR_NR SIP_API_MINOR_NR defines
Source1: macros.sip
%global _sip_api_major 11
%global _sip_api_minor 1
%global _sip_api %{_sip_api_major}.%{_sip_api_minor}

Provides: sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}

BuildRequires: python2-devel
BuildRequires: sed

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

%description
SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python bindings for any C++
class library.

%package devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-macros = %{version}-%{release}
Requires: python2-devel
%description devel
This package contains files needed to generate Python bindings for any C++
classes library.

%package macros
Summary: RPM macros for use when working with SIP
Requires: rpm
# when arch->noarch happened
Obsoletes: sip-macros < 4.15.5
BuildArch: noarch
%description macros
This package contains RPM macros for use when working with SIP.
%if 0%{?with_python3}
It is used by both the sip-devel (python 2) and python3-sip-devel subpackages.
%endif

%if 0%{?with_python3}
%package -n python3-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python3-sip-api(%{_sip_api_major}) = %{_sip_api}
Provides: python3-sip-api(%{_sip_api_major})%{?_isa} = %{_sip_api}
%description -n python3-sip
This is the Python 3 build of SIP.

SIP is a tool for generating bindings for C++ classes so that they can be
accessed as normal Python 3 classes. SIP takes many of its ideas from SWIG but,
because it is specifically designed for C++ and Python, is able to generate
tighter bindings. SIP is so called because it is a small SWIG.

SIP was originally designed to generate Python bindings for KDE and so has
explicit support for the signal slot mechanism used by the Qt/KDE class
libraries. However, SIP can be used to generate Python 3 bindings for any C++
class library.

%package -n python3-sip-devel
Summary: Files needed to generate Python 3 bindings for any C++ class library
Requires: %{name}-macros = %{version}-%{release}
Requires: python3-sip%{?_isa} = %{version}-%{release}
Requires: python3-devel
%description -n python3-sip-devel
This package contains files needed to generate Python 3 bindings for any C++
classes library.
%endif


%prep

%setup -q -n %{name}-%{version}%{?snap:-snapshot-%{snap}}

%patch50 -p1 -b .no_strip
%patch51 -p1 -b .no_rpath

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} configure.py -d %{python3_sitearch} CXXFLAGS="%{optflags}" CFLAGS="%{optflags}" --sipdir=%{_datadir}/python3-sip

make %{?_smp_mflags} 
popd
%endif

%{__python2} configure.py -d %{python2_sitearch} CXXFLAGS="%{optflags}" CFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
# Perform the Python 3 installation first, to avoid stomping over the Python 2
# /usr/bin/sip:
%if 0%{?with_python3}
pushd %{py3dir}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/python3-sip
mv %{buildroot}%{_bindir}/sip %{buildroot}%{_bindir}/python3-sip
popd
%endif

# Python 2 installation:
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/sip

# Macros used by -devel subpackages:
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip


%files
%doc LICENSE LICENSE-GPL2 LICENSE-GPL3
%doc NEWS README
%{python2_sitearch}/sip.so
%{python2_sitearch}/sip*.py*

%files devel
%{_bindir}/sip
%{_datadir}/sip/
%{python2_inc}/*

%files macros
%{rpm_macros_dir}/macros.sip

%if 0%{?with_python3}
%files -n python3-sip
%{python3_sitearch}/sip.so
%{python3_sitearch}/sip*.py*
%{python3_sitearch}/__pycache__/*

%files -n python3-sip-devel
# Note that the "sip" binary is invoked by name in a few places higher up
# in the KDE-Python stack; these will need changing to "python3-sip":
%{_bindir}/python3-sip
%{_datadir}/python3-sip/
%{python3_inc}/*
%endif


%changelog
* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 4.16.6-1
- sip-4.16.6

* Fri Dec 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.5-1
- sip-4.16.5

* Sun Oct 26 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.4-1
- sip-4.16.4

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.3-1
- sip-4.16.3

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.2-1
- sip-4.16.2

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16.1-1
- sip-4.16.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16-2
- pull in upstream fix for PyQt-4.11.1 ftbfs

* Wed May 28 2014 Rex Dieter <rdieter@fedoraproject.org> 4.16-1
- sip-4.16, sip-api(11)=11.1

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.5-2
- rebuild (f21-python)

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.15.5-1
- sip-4.15.5, sip-api(11)=11.0
- -macros: noarch
- s/python/python2/

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.4-2
- -macros: use %%_rpmconfigdir/macros.d (where supported)
- .spec cleanup

* Wed Jan 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.15.4-1
- sip-4.15.4

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 4.15.3-1
- sip-4.15.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.7-1
- sip-4.14.7
- sip-api(10) = 10.0

* Sun Apr 21 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.6-1
- sip-4.14.6

* Tue Mar 26 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.5-1
- sip-4.14.5 (#928340)

* Sun Mar 03 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.4-1
- sip-4.14.4, sip-api 9.2

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-1
- sip-4.14.3

* Sun Dec 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.14.2-1
- sip-4.14.2

* Sun Oct 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- sip-4.14.1
- sip-api(9) = 9.1

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.14-1
- sip-4.14
- sip-api(9) = 9.0

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.13.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 4.13.3-3
- make with_python3 be conditional on fedora

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 4.13.3-1
- 4.13.3

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.13.2-1
- 4.13.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.13.1-1
- 4.13.1

* Wed Oct 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.13-1
- 4.13

* Fri Sep 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-3
- License: GPLv2 or GPLv3 and (GPLv3+ with exceptions) (#226419)

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-2
- try not to rpath the world (#737236)

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.4-1
- 4.12.4

* Wed Jun 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.3-1
- 4.12.3

* Mon May 02 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.2-1
- 4.12.2

* Tue Mar 22 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-5
- Provides: (python3-)sip-api(...)%%{_isa} ...  (ie, make it arch'd)

* Fri Feb 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-4
- no_strip patch, fixes -debuginfo

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-2
- macros.sip: %%_sip_api_minor 1

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.12.1-1
- sip-4.12.1

* Sat Jan 15 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-0.1.fa100876a783
- sip-4.12.1 snapshot

* Thu Dec 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.12-2
- rebuild (python3)

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.12-1
- sip-4.12

* Mon Nov 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-2
- add missing %%defattr to python3- pkgs (#226419)

* Sat Oct 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- sip-4.11.2

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- sip-4.11.1
- sip-api(8) = 8.0

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 4.10.5-3
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Rex Dieter <rdieter@fedoraproject.org> 4.10.5-1
- sip-4.10.5

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> 4.10.3-1
- sip-4.10.3

* Fri Jun 25 2010 Karsten Hopp <karsten@redhat.com> 4.10.2-3
- bump and rebuild so that s390 will build the python3-sip packages

* Mon Apr 26 2010 David Malcolm <dmalcolm@redhat.com> - 4.10.2-2
- enable "with_python3" in the build
- use py3dir throughout, as provided by python3-devel
- name the python 3 sip binary "python3-sip"
- fix a typo in the name of the data dir: python-3sip -> python3-sip
- split out macros.sip into a new subpackage

* Sat Apr 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- sip-4.10.2

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-2
- _sip_api_minor 1

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- sip-4.10.1

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-1
- sip-4.10 (final)

* Fri Jan 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-0.2.20100102
- RFE: Support python3 when building sip (#545124)
- drop old pre v4 changelog

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.10-0.1.20100102
- sip-4.10-snapshot-20100102

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- sip-4.9.3

* Fri Nov 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- sip-4.9.2

* Tue Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-3
- move sip binary to -devel 

* Mon Nov 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-2
- Provides: sip-api(%%_sip_api_major) = %%_sip_api
- devel: /etc/rpm/macros.sip helper

* Fri Oct 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- sip-4.9.1

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-0.1.20091014
- sip-4.9.1-snapshot-20091014

* Thu Oct 15 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- sip-4.9
- License: GPLv2 or GPLv3

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.8.2-2
- Convert specfile to UTF-8.

* Tue Jul 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- sip-4.8.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8.1-1
- sip-4.8.1

* Fri Jun 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-1
- sip-4.8

* Thu May 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.8-0.1.20090430
- sip-4.8-snapshot-20090430

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.7.9-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.9-1
- sip-4.7.9

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.7.8-1
- sip-4.7.8

* Thu Sep 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.7.7-3
- fix license tag

* Tue Sep 02 2008 Than Ngo <than@redhat.com> 4.7.7-2
- get rid of BR on qt

* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.7-1
- sip-4.7.7

* Wed May 21 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.6-1
- sip-4.7.6

* Wed May 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.5-1
- sip-4.7.5

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-3
- BR: qt3-devel (f9+)

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-2
- fix 64bit patch

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.7.4-1
- sip-4.7.4

* Thu Dec 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.3-1
- sip-4.7.3

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.2-1
- sip-4.7.2
- omit needless scriptlets

* Mon Nov 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 4.7.1-2
- License: Python Software Foundation License v2
- fix/cleanup some macro usage
- fix Source, Url. 

* Mon Oct 22 2007 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Mon Oct 01 2007 Than Ngo <than@redhat.com> - 4.6-3
- fix rh#289321, sipconfig.py includes wrong py_lib_dir, thanks to Rex Dieter

* Thu Aug 30 2007 Than Ngo <than@redhat.com> - 4.6-2.fc7
- typo in description

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 4.6-1.fc7
- 4.6

* Thu Jan 18 2007 Than Ngo <than@redhat.com> - 4.5.2-1
- 4.5.2 

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 4.5-2
- rebuild against python 2.5
- cleanups for python packaging guidelines

* Mon Nov 06 2006 Than Ngo <than@redhat.com> 4.5-1
- 4.5

* Thu Sep 28 2006 Than Ngo <than@redhat.com> 4.4.5-3
- fix #207297, use qt qmake files

* Wed Sep 20 2006 Than Ngo <than@redhat.com> 4.4.5-2
- fix #206633, own %%_datadir/sip

* Wed Jul 19 2006 Than Ngo <than@redhat.com> 4.4.5-1
- update to 4.4.5

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 4.4.3-2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.4.3-1.1
- rebuild

* Thu Apr 27 2006 Than Ngo <than@redhat.com> 4.4.3-1
- update to 4.4.3
- built with %%{optflags}

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.3.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 12 2005 Than Ngo <than@redhat.com> 4.3.1-1
- update to 4.3.1

* Wed Mar 23 2005 Than Ngo <than@redhat.com> 4.2.1-1
- 4.2.1

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 4.2-1
- 4.2

* Thu Nov 11 2004 Than Ngo <than@redhat.com> 4.1-2
- rebuild against python 2.4

* Fri Sep 24 2004 Than Ngo <than@redhat.com> 4.1-1
- update to 4.1
