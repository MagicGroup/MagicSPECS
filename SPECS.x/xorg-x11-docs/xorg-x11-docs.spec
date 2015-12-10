%define tarname xorg-docs

Summary: X.Org X11 documentation
Summary(zh_CN.UTF-8): X.Org X11 文档
Name: xorg-x11-docs
Version:	1.7.1
Release:	4%{?dist}
License: MIT
Group: Documentation
Group(zh_CN.UTF-8): 文档
URL: http://www.x.org

BuildArch: noarch

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/doc/%{tarname}-%{version}.tar.bz2
Patch0: docs-1.3-registry.patch

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: xorg-sgml-doctools >= 1.1.1
BuildRequires: xorg-x11-util-macros
BuildRequires: ghostscript
BuildRequires: xmlto >= 0.0.24-2
BuildRequires: xmlto-tex 

%define x11docdir %{_datadir}/doc/xorg-x11-docs-%{version}

%description
Protocol and other technical documentation for the X.Org X11 X Window System
implementation.

%description -l zh_CN.UTF-8
X.Org X11 文档。

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1 -b .registry

%build
autoreconf -v --install || exit 1
%configure --docdir=%{x11docdir}
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/Xprint.7*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{x11docdir}
%{_mandir}/man7/Consortium.7*
%{_mandir}/man7/Standards.7*
%{_mandir}/man7/X.7*
%{_mandir}/man7/XOrgFoundation.7*
%{_mandir}/man7/XProjectTeam.7*
%{_mandir}/man7/Xsecurity.7*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.7.1-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.7.1-3
- 为 Magic 3.0 重建

* Sun Oct 25 2015 Liu Di <liudidi@gmail.com> - 1.7.1-2
- 更新到 1.7.1

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Dave Airlie <airlied@redhat.com> 1.6-3
- update build requires + docdir + (temporary jdk 1.7 to workaround bug in rawhide)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Matěj Cepl <mcepl@redhat.com> - 1.6-1
- New upstream version (#640564)

* Mon Nov 22 2010 Adam Jackson <ajax@redhat.com> 1.3-7
- Fix ps-to-pdf conversion even harder.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Adam Jackson <ajax@redhat.com> 1.3-4
- Fix %%x11docdir to match %%name. (#484734)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.3-3
- Fix license tag.

* Tue Dec 25 2007 Adam Jackson <ajax@redhat.com> 1.3-2
- Install PDF instead of gzipped PostScript.
- Move everything to /usr/share/doc to be more like other doc packages.
- Add 'registry' to the doc set.

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 1.3-1
- Update to 1.3

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 1.2-4.fc6
- Fix the package summary/description.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-3.fc6
- Added "Provides: XFree86-doc, xorg-x11-doc" as per request in (#199927)

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-2.fc6
- Change rpm Group to "Documentation", which is what other docs packages use.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.2-1.fc6
- Initial build.
