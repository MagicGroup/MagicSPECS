Summary: Tools for managing a frame buffer's video mode properties.
Summary(zh_CN.UTF-8): 管理帧缓冲的视频模式属性的工具。
Name: fbset
Version: 2.1
Release: 25%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://home.tvd.be/cr26864/Linux/fbdev/
Source: http://home.tvd.be/cr26864/Linux/fbdev/fbset-2.1.tar.gz
BuildRequires: bison flex
Patch0: fbset-2.1-makefile.patch
Patch1: fbset-2.1-fixmode.patch
BuildRoot: %{_tmppath}/%{name}-root
ExcludeArch: s390 s390x

%description
Fbset is a utility for maintaining frame buffer resolutions.  Fbset
can change the video mode properties of a frame buffer device, and is
usually used to change the current video mode.

Install fbset if you need to manage frame buffer resolutions.

%description -l zh_CN.UTF-8
Fbset 是一个用来维护帧缓冲分辨率的工具。Fbset 能够改变一个帧缓冲设
备的视频模式属性，并且通常用来改变当前的视频模式。 如果您需要管理
帧缓冲分辨率，您应该安装 Fbset 软件包。

%prep
%setup -q
%patch0 -p1 -b .makefile
%patch1 -p1 -b .fixmode

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf ${RPM_BUILD_ROOT}

%make_install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man[58]/*
%config	%{_sysconfdir}/fb.modes

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.1-25
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 2.1-24
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.1-23
- 为 Magic 3.0 重建

* Mon Nov 21 2011 Liu Di <liudidi@gmail.com> - 2.1-22
- 为 Magic 3.0 重建

* Fri Oct 06 2006 Liu Di <liudidi@gmail.com> - 2.1-19mgc
- rebuild for Magic

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1-22
- rebuild
- Add missing br flex

* Mon May 29 2006 Jindrich Novy <jnovy@redhat.com> 2.1-21
- add BuildRequires: bison (#193362)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1-20.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1-20.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Mar  4 2005 Jidnrich Novy <jnovy@redhat.com> 2.1-20
- rebuilt with gcc4

* Thu Feb 10 2005 Jindrich Novy <jnovy@redhat.com> 2.1-19
- remove -D_FORTIFY_SOURCE=2 from CFLAGS, present in RPM_OPT_FLAGS

* Wed Feb  9 2005 Jindrich Novy <jnovy@redhat.com> 2.1-18
- Copyright -> License conversion
- rebuilt with -D_FORTIFY_SOURCE=2

* Mon Oct 11 2004 Bill Nottingham <notting@redhat.com> 2.1-17
- add URL (#122128)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2.1-12
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x

* Fri Feb 23 2001 Preston Brown <pbrown@redhat.com>
- fix 1024x768 72 Hz mode (#29024)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Tue Feb 15 2000 Bill Nottingham <notting@redhat.com>
- ship fb.modes everywhere

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- fix man page permissions

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix summary

* Thu Oct  7 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1
- don't include fb devs.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- include fb devs too (#1515)
- update to 19990118 version.

* Thu Nov  5 1998 Jeff Johnson <jbj@redhat.com>
- import from ultrapenguin 1.1.
- upgrade to 19981104.

* Thu Oct 29 1998 Jakub Jelinek <jj@ultra.linux.cz>
- new package
