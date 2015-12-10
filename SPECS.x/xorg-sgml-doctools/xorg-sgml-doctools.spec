Summary: X.Org SGML documentation generation tools
Name: xorg-sgml-doctools
Version:	1.11
Release:	5%{?dist}
License: MIT
Group: Development/Tools
URL: http://www.x.org

BuildArch: noarch

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/doc/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
Requires: pkgconfig, xml-common

%description
This package is required in order to generate the X.Org X11 documentation
from source.

%prep
%setup -q

%build
%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_datadir}/sgml/X11/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.11-5
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.11-4
- 为 Magic 3.0 重建

* Sun Oct 25 2015 Liu Di <liudidi@gmail.com> - 1.11-3
- 为 Magic 3.0 重建

* Sun Oct 25 2015 Liu Di <liudidi@gmail.com> - 1.11-2
- 更新到 1.11

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.10-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 14 2011 Matěj Cepl <mcepl@redhat.com> - 1.10-1
- New upstream release.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 02 2010 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.5-1
- Address review commentary https://bugzilla.redhat.com/show_bug.cgi?id=226569
- Update to 1.5, solving license issue.  This adds a few new files and requires
  a pkgconfig dependency.
- Add dependency on xml-common to fix unowned directory issue. 
- Remove some bits (buildroot tag and cleaning) no longer required in Fedora.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.1.1-2
- Fix license tag.

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 1.1.1-1
- Update to 1.1.1

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.1-2.fc6
- Change rpm Group to "Application/Text" which is what sgml-common uses.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.1-1.fc6
- Initial build.
