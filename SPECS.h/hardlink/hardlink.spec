Summary:	Create a tree of hardlinks
Name:		hardlink
Version:	1.0
Release:	14%{?dist}
Epoch:		1
Group:		System Environment/Base
URL:		http://pkgs.fedoraproject.org/gitweb/?p=hardlink.git
License:	GPL+
Source0:	hardlink.c
Source1:	hardlink.1
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:	kernel-utils

%description
hardlink is used to create a tree of hard links.
It's used by kernel installation to dramatically reduce the
amount of diskspace used by each kernel package installed.

%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} hardlink.c

%build
gcc $RPM_OPT_FLAGS hardlink.c -o hardlink

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/hardlink.1
install -D -m 755 hardlink $RPM_BUILD_ROOT%{_sbindir}/hardlink

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/hardlink
%{_mandir}/man1/hardlink.1*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1:1.0-14
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Jindrich Novy <jnovy@redhat.com> - 1:1.0-12
- fix possible buffer overflows, integer overflows (CVE-2011-3630 CVE-2011-3631 CVE-2011-3632)
- update man page

* Wed Mar  2 2011 Jindrich Novy <jnovy@redhat.com> - 1:1.0-11
- don't use mmap(2) to avoid failures on i386 with 1GB files and larger (#672917)
- fix package URL (#676962)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 1:1.0-7
- manual rebuild because of gcc-4.3 (#434188)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0-6
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> - 1:1.0-5
- update License
- rebuild for BuildID

* Mon Apr 23 2007 Jindrich Novy <jnovy@redhat.com> - 1:1.0-4
- include sources in debuginfo package (#230833)

* Mon Feb  5 2007 Jindrich Novy <jnovy@redhat.com> - 1:1.0-3
- merge review related spec fixes (#225881)

* Sun Oct 29 2006 Jindrich Novy <jnovy@redhat.com> - 1:1.0-2
- update docs to describe highest verbosity -vv option (#210816)
- use dist

* Wed Jul 12 2006 Jindrich Novy <jnovy@redhat.com> - 1:1.0-1.23
- remove ugly suffixes added by rebuild script

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0-1.21.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0-1.20.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.0-1.19.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Jindrich Novy <jnovy@redhat.com>
- more spec cleanup - thanks to Matthias Saou (#172968)
- use UTF-8 encoding in the source

* Mon Nov  7 2005 Jindrich Novy <jnovy@redhat.com>
- add hardlink man page
- add -h option
- use _sbindir instead of /usr/sbin directly
- don't warn because of uninitialized variable
- spec cleanup

* Fri Aug 26 2005 Dave Jones <davej@redhat.com>
- Document hardlink command line options. (Ville Skytta) (#161738)

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com>
- don't try to hardlink 0 byte files (#154404)

* Fri Apr 15 2005 Florian La Roche <laroche@redhat.com>
- remove empty scripts

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- rebuild with -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.
