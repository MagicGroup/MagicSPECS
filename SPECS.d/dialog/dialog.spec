Summary: A utility for creating TTY dialog boxes
SUmmary(zh_Cn.UTF-8): 在控制台界面下显示对话框的工具
Name: dialog
Version: 1.2.20150528
Release: 1%{?dist}
License: LGPLv2
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://invisible-island.net/dialog/dialog.html
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
%define dialogsubversion %(echo %{version} | awk -F. '{print $3}')
Source: ftp://invisible-island.net/dialog/dialog-%{majorver}-%{dialogsubversion}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ncurses-devel gettext findutils libtool
Patch1: dialog-incdir.patch
Patch2: dialog-multilib.patch
Patch3: dialog-libs.patch

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.  

Install dialog if you would like to create TTY dialog boxes.

%description -l zh_CN.UTF-8
在控制台界面下显示对话框的工具。主要用在脚本文件编写中。

%package devel 
Summary: Development files for building applications with the dialog library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release} ncurses-devel

%description devel
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces. This package 
contains the files needed for developing applications, which use the 
dialog library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n dialog-%{majorver}-%{dialogsubversion}
%patch1 -p1 -b .incdir
%patch2 -p1 -b .multilib
#%patch3 -p1 -b .libs

%build
%configure \
	--enable-nls \
	--with-libtool \
	--with-ncursesw \
	--includedir=%{_includedir}/dialog
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# prepare packaged samples
rm -rf _samples
mkdir _samples
cp -a samples _samples
rm -rf _samples/samples/install
find _samples -type f -print0 | xargs -0 chmod a-x

make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/libdialog.so.*.*.*
rm -f $RPM_BUILD_ROOT%{_libdir}/libdialog.{,l}a
magic_rpm_clean.sh
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING dialog.lsm README _samples/samples
%{_bindir}/dialog
%{_libdir}/libdialog.so.*
%{_mandir}/man1/dialog.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/dialog-config
%{_includedir}/dialog
%{_libdir}/libdialog.so
%{_mandir}/man3/dialog.*

%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.2.20150528-1
- 更新到 1.2.20150528

* Thu Mar 20 2014 Liu Di <liudidi@gmail.com> - 1.2.20140219-1
- 更新到 1.2.20140219

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.1-16.20110707
- 为 Magic 3.0 重建

* Mon Nov 19 2012 Liu Di <liudidi@gmail.com> - 1.1-15.20110707
- 为 Magic 3.0 重建

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-14.20110707
- Rebuilt for glibc bug#747377

* Tue Jul 26 2011 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-13.20110707
- update to 1.1-20110707

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12.20100428
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 12 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-11.20100428
- update to 1.1-20100428

* Thu Feb 04 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-10.20100119
- update to 1.1-20100119

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9.20080819
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8.20080819
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 25 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-7.20080819
- update to 1.1-20080819

* Wed Jul 30 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-6.20080727
- update to 1.1-20080727

* Fri Apr 11 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-5.20080316
- update to 1.1-20080316

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1-4.20071028
- Autorebuild for GCC 4.3

* Mon Nov 05 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.1-3.20071028
- update to 1.1-20071028
- fix multilib conflicts (#341001)
- use shared library, drop static
- merge review fixes (#225693)

* Fri Aug 17 2007 Harald Hoyer <harald@redhat.com> - 1.1-2.20070704
- changed license to LGPLv2

* Thu Jul  5 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070704
- version 1.1-20070704

* Wed Jun 27 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070604
- dialog-1.1-20070604

* Wed Feb 28 2007 Harald Hoyer <harald@redhat.com> - 1.1-1.20070227svn
- version 1.1-20070227
- added devel subpackage
- specfile fixes (bug#225693)
- Resolves: rhbz#225693

* Wed Jan 17 2007 Harald Hoyer <harald@redhat.com> - 1.0.20060221-1
- version 1.0-20060221

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.20051107-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Harald Hoyer <harald@redhat.com> 1.0-20051107-1
- version 1.0-20051107

* Mon Apr 18 2005 Harald Hoyer <harald@redhat.com> 1.0-20050306-1
- version 1.0-20050306

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 1.0-20050206-1
- new version 1.0-20050206

* Tue Dec 21 2004 Harald Hoyer <harald@redhat.com> 1.0-20041219-1
- new version 1.0-20041219

* Wed Oct 20 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-3
- rlandry@redhat.com refined his patch (bug 136374)

* Tue Oct 19 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-2
- added patch from rlandry@redhat.com which removes extra trailing
  spaces (bug 136374)

* Fri Aug 27 2004 Harald Hoyer <harald@redhat.com> 1.0-20040731-1
- new version 1.0-20040731

* Wed Jul 29 2004 Harald Hoyer <harald@redhat.com> 1.0-20040728-1
- new version 1.0-20040728

* Wed Jul 28 2004 Harald Hoyer <harald@redhat.de> 1.0-20040721-1
- new version 1.0-20040721

* Wed Jun 23 2004 Harald Hoyer <harald@redhat.de> 0.9b.20040606-1
- new version 0.9b-20040606
- new Version scheme

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 08 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031207.1
- version 20031207

* Thu Nov 27 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031126.1
- version 20031126

* Mon Nov 24 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031002.2
- added gettext BuildReq (#109192)

* Wed Oct  8 2003 Harald Hoyer <harald@redhat.de> 0.9b-20031002.1
- version 20031002

* Thu Sep 11 2003 Harald Hoyer <harald@redhat.de> 0.9b-20030910.1
- new version 20030910 which also fixes #104236

* Tue Aug 12 2003 Harald Hoyer <harald@redhat.de> 0.9b-20020814.5
- --with-ncursesw

* Fri Aug  8 2003 Elliot Lee <sopwith@redhat.com> 0.9b-20020814.4
- Rebuilt

* Tue Jun 17 2003 Harald Hoyer <harald@redhat.de> 0.9b-20020814.3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 0.9b-20020814.2
- rebuild

* Tue Nov 05 2002 Harald Hoyer <harald@redhat.de> 0.9b-20020814.1
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 0.9b-20020519.1
- update to dialog-0.9b-20020519

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 18 2001 Harald Hoyer <harald@redhat.de>
- update to 20010527
- added ncurses-devel dependency (#44733)
- removed perl dependency

* Tue Jan 09 2001 Harald Hoyer <harald@redhat.com>
- update to 20001217

* Mon Aug  7 2000 Bill Nottingham <notting@redhat.com>
- fix one of the examples (#14073)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- rebuild against current ncurses/readline

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Jan 20 2000 Bill Nottingham <notting@redhat.com>
- fix loop patch for reading from pipe

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 7 1998 Michael Maher <mike@redhat.com> 
- Added Sean Reifschneider <jafo@tummy.com> patches for 
  infinite loop problems.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 15 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
