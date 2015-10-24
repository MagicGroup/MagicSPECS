# The git_commit define will have the complement given by git-hub to the source downloaded
%define git_commit fadf11e
Name:           cwiid
Version:        0.6.00
Release:        27.20100505git%{git_commit}%{?dist}
Summary:        Wiimote interface library
Summary(zh_CN.UTF-8): Wii 的遥控接口库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://abstrakraft.org/cwiid/

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# source URL : http://github.com/abstrakraft/cwiid/tarball/%%{git_commit} 
Source0:        abstrakraft-cwiid-%{git_commit}.tar.gz
Source1:        wmgui.desktop

# this patch is in my git-hub fork git://github.com/bogado/cwiid.git
# there is an upstream bug filed by me at http://abstrakraft.org/cwiid/ticket/105
Patch0:         0001-Fix-missing-library-from-wmdemo.patch

BuildRequires:  bluez-libs-devel, gawk, bison, flex, gtk2-devel, python-devel >= 2.4, desktop-file-utils
BuildRequires:  autoconf automake

%description
Cwiid is a library that enables your application to communicate with
a wiimote using a bluetooth connection.

%description -l zh_CN.UTF-8
Wii 的遥控接口库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}, bluez-libs-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        python2
Summary:        Python binding for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires:       %{name} = %{version}-%{release}

%description    python2
Python2 binding for %{name}

%description python2 -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%package        utils
Summary:        Wiimote connection test application
Summary(zh_CN.UTF-8): %{name} 的测试程序
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-wmgui = %{version}-%{release}
Obsoletes:      %{name}-wmgui < 0.6.00-7

%description    utils
Applications to test the wiimote connection

%description utils -l zh_CN.UTF-8
%{name} 的测试程序。

%package        wminput
Summary:        Enables using the wiimote as an input source
Summary(zh_CN.UTF-8): 把 Wii 的遥控做为输入源
# The licence must be GPLv2 instead of GPLv2+ for this package
# since the file wminput/action_enum.txt is GPLv2 as stated
# in the file.
License:        GPLv2
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires:       %{name} = %{version}-%{release}, %{name}-python2

%description    wminput
This program allows the user to use the wiimote to emulate normal system
input sources like the mouse and keyboard.

%description wminput -l zh_CN.UTF-8
把 Wii 的遥控做为输入源。

%prep
%setup -q -n abstrakraft-cwiid-%{git_commit}
%patch0 -p1

%build
aclocal
autoconf
%configure CC="gcc %{optflags}" --disable-static --docdir="%{_pkgdocdir}"
make %{?_smp_mflags}

%install
%make_install LDCONFIG=/bin/true
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# find all directories 
find $RPM_BUILD_ROOT%{_sysconfdir} -type f -exec chmod 0644 {} ';'
rm $RPM_BUILD_ROOT/%{_libdir}/*.a
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README COPYING ChangeLog
%exclude %{_pkgdocdir}/Xmodmap
%exclude %{_pkgdocdir}/wminput.list
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files python2
%{python_sitearch}/*

%files wminput
# Fold-in wminput docs into main-package
%{_pkgdocdir}/Xmodmap
%{_pkgdocdir}/wminput.list
%config(noreplace) %{_sysconfdir}/cwiid/
%{_bindir}/wminput
%{_mandir}/man1/wminput*
%{_libdir}/cwiid

%files utils
%{_bindir}/lswm
%{_bindir}/wmgui
%{_mandir}/man1/wmgui*
%{_datadir}/applications/wmgui.desktop

%changelog
* Wed Oct 21 2015 Liu Di <liudidi@gmail.com> - 0.6.00-27.20100505gitfadf11e
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-26.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-25.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-24.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.6.00-23.20100505gitfadf11e
- Add BR: autoconf, automake (FTBFS, RHBZ #992105).
- Reflect docdir changes.
- Fix bogus %%changelog date.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-22.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.00-21.20100505gitfadf11e
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines
- fix desktop file to follow specification

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-20.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-19.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-18.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.00-17.20100505gitfadf11e
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-16.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.00-15.20100505gitfadf11e
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May 06 2010 Victor Bogado <victor@bogado.net> 0.6.00-14.20100505gitfadf11e
- updated to latest git version, that adds suport for the wii balance board and the wii motion plus
- Fixed DSO linking issues

* Wed Jan 27 2010 Victor Bogado <victor@bogado.net> 0.6.00-13
- atempt to fix bug #555449

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.00-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.00-10
- Rebuild for Python 2.6

* Thu Sep 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 0.6.00-9
- F-10: rebuild against new bluez
- Fix for bluez api change

* Thu May  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 0.6.00-7
- Rename -wmgui to -tools and repackage.

* Fri Apr 25 2008 Victor Bogado <victor@bogado.net> 0.6.00-6
- Fix mode for configuration files.

* Thu Apr 24 2008 Victor Bogado <victor@bogado.net> 0.6.00-5
- comment explaining why a subpackage has a different license.
- BuildRequires needed one more program.

* Mon Apr 21 2008 Victor Bogado <victor@bogado.net> 0.6.00-4
- Source URL has version on it.

* Sun Apr 20 2008 Victor Bogado <victor@bogado.net>
- Removing files that are included twice.

* Sat Apr 19 2008 Victor Bogado <victor@bogado.net> 0.6.00-3
- solved directory ownership problems
- Changed license of wminput to GPLv2
- AUTHORS and NEWS bundled as docs.
- Added desktop file 
- Removed static library files
- Made the spec honor compiler flags.
- Added bluez-libs-devel to requires of the devel package
- Removed python from BuildRequires list
- Added bluez-libs-devel to requires of development package

* Wed Apr 09 2008 Victor Bogado <victor@bogado.net> 0.6.00-2
- added changelog. 
- doc section of files.
- changed the line that specifies the python library to accomodate the file *.info that is generates with other versions of python.
- cutted long description lines
- fixed documentations tags

* Sat Apr 05 2008 Victor Bogado <victor@bogado.net>
- First verion

