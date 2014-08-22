%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define buildflags WXPORT=gtk2 UNICODE=1

Name:           wxPython
Version:        2.8.12.0
Release:        3%{?dist}

Summary:        GUI toolkit for the Python programming language
Summary(zh_CN.UTF-8): Python 程序开发的 GUI 工具箱

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+ and wxWidgets 
URL:            http://www.wxpython.org/
Source0:        http://downloads.sourceforge.net/wxpython/%{name}-src-%{version}.tar.bz2
# fix aui imports
# http://trac.wxwidgets.org/ticket/12107
Patch0:         wxPython-2.8.12.0-aui.patch
Patch1:		wxPython-2.8.12.0-format.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# make sure to keep this updated as appropriate
BuildRequires:  wx-gtk2-unicode-devel >= 2.8.11
BuildRequires:  python-devel

# packages should depend on "wxPython", not "wxPythonGTK2", but in case
# one does, here's the provides for it.
Provides:       wxPythonGTK2 = %{version}-%{release}

%description
wxPython is a GUI toolkit for the Python programming language. It allows
Python programmers to create programs with a robust, highly functional
graphical user interface, simply and easily. It is implemented as a Python
extension module (native code) that wraps the popular wxWindows cross
platform GUI library, which is written in C++.

%description -l zh_CN.UTF-8
Python 语言的图形界面开发工具箱，是 wxWindows 的 Python 扩展模块实现。

%package        devel
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Development files for wxPython add-on modules
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name} = %{version}-%{release}
Requires:       wx-gtk2-unicode-devel

%description devel
This package includes C++ header files and SWIG files needed for developing
add-on modules for wxPython. It is NOT needed for development of most
programs which use the wxPython toolkit.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        docs
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Summary:        Documentation and samples for wxPython
Summary(zh_CN.UTF-8): %{name} 的文档。
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description docs
Documentation, samples and demo application for wxPython.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n wxPython-src-%{version}
%patch0 -p1 -b .aui
%patch1 -p1 -b .format

# fix libdir otherwise additional wx libs cannot be found
sed -i -e 's|/usr/lib|%{_libdir}|' wxPython/config.py


%build
# Just build the wxPython part, not all of wxWindows which we already have
# in Fedora
cd wxPython
# included distutils is not multilib aware; use normal
rm -rf distutils
python setup.py %{buildflags} build


%install
rm -rf $RPM_BUILD_ROOT
cd wxPython
python setup.py %{buildflags} install --root=$RPM_BUILD_ROOT

# this is a kludge....
%if "%{python_sitelib}" != "%{python_sitearch}"
mv $RPM_BUILD_ROOT%{python_sitelib}/wx.pth  $RPM_BUILD_ROOT%{python_sitearch}
mv $RPM_BUILD_ROOT%{python_sitelib}/wxversion.py* $RPM_BUILD_ROOT%{python_sitearch}
%endif
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc wxPython/licence
%{_bindir}/*
%{python_sitearch}/wx.pth
%{python_sitearch}/wxversion.py*
%dir %{python_sitearch}/wx-2.8-gtk2-unicode/
%{python_sitearch}/wx-2.8-gtk2-unicode/wx
%{python_sitearch}/wx-2.8-gtk2-unicode/wxPython
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitelib}/*egg-info
%{python_sitearch}/wx-2.8-gtk2-unicode/*egg-info
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/wx-2.8/wx/wxPython
%{_includedir}/wx-2.8/wx/wxPython/*.h
%dir %{_includedir}/wx-2.8/wx/wxPython/i_files
%{_includedir}/wx-2.8/wx/wxPython/i_files/*.i
%{_includedir}/wx-2.8/wx/wxPython/i_files/*.py*
%{_includedir}/wx-2.8/wx/wxPython/i_files/*.swg

%files docs
%defattr(-,root,root,-)
%doc wxPython/docs wxPython/demo wxPython/samples


%changelog
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 26 2011 Dan Horák <dan[at]danny.cz> - 2.8.12.0-1
- update to 2.8.12.0 (#699207)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.8.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 12 2010 Dan Horák <dan@danny.cz> - 2.8.11.0-3
- rebuilt against wxGTK-2.8.11-2

* Sun Jul 11 2010 Lubomir Rintel <lkundrak@v3.sk> - 2.8.11.0-2
- Include egg-info when build on recent RHEL

* Mon May 31 2010 Dan Horák <dan[at]danny.cz> - 2.8.11.0-1
- update to 2.8.11.0 (#593837, #595936, #597639)

* Sun May  2 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-3
- rebuilt with wxGTK 2.8.11

* Wed Mar 17 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-2
- add missing module (#573961)

* Sat Jan 16 2010 Dan Horák <dan[at]danny.cz> - 2.8.10.1-1
- update to 2.8.10.1
- backport to wxGTK 2.8.10 API
- cleaned up BRs

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> - 2.8.9.2-4
- Change python_foo macros to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 10 2009 Dan Horák <dan[at]danny.cz> - 2.8.9.2-2
- add patch to fix compile failure for contrib/gizmos/_treelist.i

* Fri Apr 10 2009 Dan Horák <dan[at]danny.cz> - 2.8.9.2-1
- update to 2.8.9.2
- create noarch docs subpackage

* Thu Mar  5 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.8.9.1-4
- Rebuilt for newer wxgtk package

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.9.1-2
- Rebuild for Python 2.6

* Tue Sep 30 2008 Dan Horak <dan[at]danny.cz> - 2.8.9.1-1
- update to 2.8.9.1
- fix libdir for additional wx libraries (#306761)

* Mon Sep 29 2008 Dan Horak <dan[at]danny.cz> - 2.8.9.0-1
- update to 2.8.9.0

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.8.0-2
- fix license tag

* Thu Jul 31 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.8.0-1
- update to 2.8.8.0 (bug #457408)
- a fix for bug #450073 is included in the upstream release, so
  dropping that patch.

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.8.7.1-5
- Fix an attribute error when importing wxPython (compat) module
  (redhat bugzilla 450073, 450074)

* Sat Jun  6 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-4
- gratuitously bump package release number to work around build system
  glitch. again, but it will work this time.

* Wed Jun  4 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-3
- gratuitously bump package release number to work around build system
  glitch

* Thu Feb 21 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-2
- include egg-info files for fedora 9 or greater

* Wed Feb 20 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7.1-1
- update to 2.8.7.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.4.0-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.8.4.0-2
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4.0-1
- update to 2.8.4.0
- obsolete compat-wxPythonGTK

* Sun Apr 15 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.3.0-1
- update to 2.8.3.0

* Fri Dec 15 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0.1-1
- update to 2.8.0.1
- make buildrequire wxGTK of version-wxpythonsubrelease
- add wxaddons to filelist

* Mon Dec 11 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-3
- bump release for rebuild against python 2.5.

* Mon Aug 28 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-2
- bump release for FC6 rebuild

* Thu Apr 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.2-1
- version 2.6.3.2
- move wxversion.py _into_ lib64. Apparently that's the right thing to do. :)
- upstream tarball no longer includes embedded.o (since I finally got around
  to pointing that out to the developers instead of just kludging it away.)
- buildrequires to just libGLU-devel instead of mesa-libGL-devel

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-4
- grr. bump relnumber.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-3
- oh yeah -- wxversion.py not lib64.

* Fri Mar 31 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-2
- buildrequires mesa-libGLU-devel

* Thu Mar 30 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3.0-1
- update to 2.6.3.0
- wxGTK and wxPython versions are inexorably linked; make BuildRequires
  be exact, rather than >=.
- make devel subpackage as per comment #7 in bug #163440.

* Thu Nov 24 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.1.0-1
- update to 2.6.0.0
- merge in changes from current extras 2.4.x package
- Happy Thanksgiving
- build animate extention again -- works now.

* Thu Apr 28 2005 Matthew Miller <mattdm@bu.edu> - 2.6.0.0-bu45.1
- get rid of accidental binaries in source tarball -- they generates
  spurious dependencies and serve no purpose
- update to 2.6.0.0 and build for Velouria
- switch to Fedora Extras base spec file
- enable gtk2 and unicode and all the code stuff (as FE does)
- disable BUILD_ANIMATE extension from contrib -- doesn't build
- files are in a different location now -- adjust to that
- zap include files (needed only for building wxPython 3rd-party modules),
  because I don't think this is likely to be very useful. Other option
  would be to create a -devel package, but I think that'd be confusing.

* Tue Feb 08 2005 Thorsten Leemhuis <fedora at leemhuis dot info> 0:2.4.2.4-4
- remove included disutils - it is not multilib aware; this
  fixes build on x86_64

* Tue Jan 06 2004 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.3
- rename package to wxPythonGTK2, provide wxPython (see bug 927)
- dont ship binaries in /usr/share

* Thu Nov 20 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.2
- add missing buildrequires: python-devel, wxGTK2-gl

* Sun Nov 02 2003 Panu Matilainen <pmatilai@welho.com> 0:2.4.2.4-0.fdr.1
- Initial RPM release.
~
