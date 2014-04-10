Summary: A perfect hash function generator
Summary(zh_CN.UTF-8): 完美哈希函数生成器
Name: gperf
Version: 3.0.4
Release: 5%{?dist}
License: GPLv3+
Source: ftp://ftp.gnu.org/pub/gnu/gperf/gperf-%{version}.tar.gz
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
URL: http://www.gnu.org/software/gperf/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.

%description -l zh_CN.UTF-8 
完美哈希函数生成器。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT/usr/share/{man,info}

make DESTDIR=$RPM_BUILD_ROOT install INSTALL='install -p'

# remove the stuff from the buildroot
rm -rf $RPM_BUILD_ROOT{%{_mandir}/{dvi,html},%{_datadir}/doc}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/gperf.info.gz %{_infodir}/dir >/dev/null 2>&1 || :
exit 0

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gperf.info.gz %{_infodir}/dir >/dev/null 2>&1|| :
fi
exit 0

%files
%defattr(-,root,root)
%doc README NEWS doc/*.{html,pdf} COPYING
%{_bindir}/%{name}
%{_mandir}/man1/gperf.1*
%{_infodir}/gperf.info*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.0.4-5
- 为 Magic 3.0 重建

* Wed Dec 07 2011 Liu Di <liudidi@gmail.com> - 3.0.4-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 01 2010 Roman Rakus <rrakus@redhat.com> - 3.0.4-2
- Fixed license to the right GPLv3+

* Mon Mar 01 2010 Roman Rakus <rrakus@redhat.com> - 3.0.4-1
- Version 3.0.4

* Tue Aug 11 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-9
- Don't print errors in post and preun sections (#515942)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-6
- Don't use makeinstall
- Remove ps files from doc
  Resolves: #225854

* Mon Jan 19 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-5
- Specfile fixes
  Resolves: #225854

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.3-4
- Autorebuild for GCC 4.3

* Tue Jan 08 2008 Florian La Roche <laroche@redhat.com> - 3.0.3-3
- fix license tag and summary

* Tue Aug 21 2007 Florian La Roche <laroche@redhat.com> - 3.0.3-2
- rebuild

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 3.0.3-1
- 3.0.3

* Mon Jan 22 2007 Florian La Roche <laroche@redhat.com>
- rhbz#223695

* Sat Nov 04 2006 Florian La Roche <laroche@redhat.com>
- 3.0.2 (#213852)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 02 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-7
- Gcc4 fix (Tomo Vuckovic) #164885 

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-6
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-5
- rebuilt

* Mon Oct 11 2004 Ivana Varekova <varekova@redhat.com>
- minor spec updates

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 3.0.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- remove unpackaged files from the buildroot

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.7.2-1
- Update to 2.7.2

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- user infodir and mandir macros for FHS
- use %%makeinstall

* Fri Feb  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild to gzip manpage
- don't use CC=egcs
- fix description

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches for egcs from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- patch for latest egcs

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binary

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- create.
