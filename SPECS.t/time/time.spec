Summary: A GNU utility for monitoring a program's use of system resources.
Summary(zh_CN.UTF-8): 一个用来监视程序对系统资源使用的 GNU 工具。
Name: time
Version: 1.7
Release: 32%{?dist}
License: GPL
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source: ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
Prereq: /sbin/install-info

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running, and displays
the results.

%description -l zh_CN.UTF-8
GNU time 工具运行另一个程序，搜集关于那个正运行的程序所用的资源的信息，
然后显示结果。 

%prep
%setup -q

%build
echo "ac_cv_func_wait3=\${ac_cv_func_wait3='yes'}" >> config.cache
%configure
make

%install
rm -rf %{buildroot}
%makeinstall
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 
fi

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/time
%{_infodir}/time.info*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.7-32
- 为 Magic 3.0 重建

* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 1.7-31
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.7-30
- 为 Magic 3.0 重建

* Wed Feb 15 2012 Liu Di <liudidi@gmail.com> - 1.7-29
- 为 Magic 3.0 重建

* Wed Oct 11 2006 Liu Di <liudidi@gmail.com> - 1.7-27mgc
- rebuild for Magic

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.7-27.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.7-27
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 1.7-26
- update source URL
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip apps, do not compress info page

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Feb 25 2002 Elliot Lee <sopwith@redhat.com>
- Remove HAVE_WAIT3 hack, tried to replace it with a requirement for an 
autoconf with the fixed test, didn't work, put in another less-bad hack 
instead.

* Wed Dec 05 2001 Tom Tromey <tromey@redhat.com>
- Bump release, force HAVE_WAIT3 to be defined at build time

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jan 31 2001 Preston Brown <pbrown@redhat.com>
- prereq install-info (#24715)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- using / as the file manifesto has weird results.

* Sun Jun  4 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- buildrooted and defattr'd

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 27 1997 Cristian Gafton <gafton@redhat.com>
- fixed info handling

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- updated the spec file; added info file handling

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
