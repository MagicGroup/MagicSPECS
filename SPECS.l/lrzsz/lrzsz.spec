Summary: The lrz and lsz modem communications programs
Summary(zh_CN.UTF-8): lrz 和 lsz 通信程序
Name: lrzsz
Version: 0.12.20
Release: 32%{?dist}
License: GPLv2+
Group: Applications/Communications
Group(zh_CN.UTF-8): 应用程序/通信
Source: http://www.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Patch1: lrzsz-0.12.20-glibc21.patch
Patch2: lrzsz-0.12.20.patch
Patch3: lrzsz-0.12.20-man.patch
Url: http://www.ohse.de/uwe/software/lrzsz.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext

%description
Lrzsz (consisting of lrz and lsz) is a cosmetically modified
zmodem/ymodem/xmodem package built from the public-domain version of
the rzsz package. Lrzsz was created to provide a working GNU
copylefted Zmodem solution for Linux systems.

%description -l zh_CN.UTF-8
这是使用 zmodem/ymodem/xmodem 协议的文件传输程序.

%prep
%setup -q

%patch1 -p1 -b .glibc21
%patch2 -p1 -b .crc
%patch3 -p1 -b .man

rm -f po/*.gmo

%build
%configure --disable-pubdir \
           --enable-syslog \
           --program-transform-name=s/l//

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 0.12.20-32
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.12.20-31
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Liu Di <liudidi@gmail.com> - 0.12.20-30
- 为 Magic 3.0 重建

* Mon Mar 07 2011 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-29
- fix typos in sz man page (#668900)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.20-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Miroslav Lichvar <mlichvar@redhat.com> 0.12.20-25
- rebuild message catalogs (#485024)
- remove dot from summary

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12.20-24
- fix license tag

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 0.12.20-23
- rebuilt against GCC 3.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-22.1
- rebuild

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 0.12.20-22
- add BR on gettext #193513

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-21.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.12.20-21.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 0.12.20-21
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 0.12.20-20
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Oct 11 2002 Than Ngo <than@redhat.com> 0.12.20-15
- Fixed a bug with 16 bit ZMODEM transfer, jordanc@censoft.com (bug #75473)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 0.12.20-12
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Aug 10 2001 Than Ngo <than@redhat.com> 0.12.20-10
- Copyright->License
- use %%find_lang

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- use RPM macros

* Sat May 27 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- cleanup specfile
- add Url
- put man pages to correct place

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Sat Feb 05 2000 Preston Brown <pbrown@redhat.com>
- rebuild to compress man pages, get new description

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 0.12.20, i18n translations included.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups 

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- Upgraded to 0.12.14 and changed makefiles so gettext isnt built.
