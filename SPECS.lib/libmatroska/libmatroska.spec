Summary:	Open audio/video container format library
Summary(zh_CN.UTF-8): 开源的音频、视频容器格式库
Name:		libmatroska
Version: 1.4.4
Release:	2%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.matroska.org/
Source0:	http://dl.matroska.org/downloads/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires:	libebml-devel >= 1.2.2

%description
Matroska is an extensible open standard Audio/Video container.  It
aims to become THE standard of multimedia container formats.  Matroska
is usually found as .mkv files (matroska video) and .mka files
(matroska audio).

%description -l zh_CN.UTF-8
开源的音频、视频容器格式库。

%package	devel
Summary:	Matroska container format library development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	libebml-devel >= 1.2.1

%description	devel
Matroska is an extensible open standard Audio/Video container.  It
aims to become THE standard of multimedia container formats.  Matroska
is usually found as .mkv files (matroska video) and .mka files
(matroska audio).

This package contains the files required to rebuild applications which
will use the Matroska container format.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install
rm %{buildroot}%{_libdir}/%{name}.la

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE.LGPL
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/matroska/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/libmatroska.pc

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.4.4-2
- 更新到 1.4.4

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.4.1-1
- 更新到 1.4.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 为 Magic 3.0 重建

* Sun Nov 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Mon Feb 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-1
- New release 1.1.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 18 2010 Martin Sourada <mso@fedoraproject.org> - 1.0.0-1
- New release
- Fixes issues with elements with an unknown size that have come up with the 
  recent popularity of WebM files
- Bumps version of libmatroska.so
  
* Mon May 24 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.0-1
- New release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.1-3
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.1-2
- Update License tag for new Licensing Guidelines compliance

* Mon Feb 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.1-1
- New upstream release 0.8.1

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.0-4
- Drop static lib from -devel package
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.0-3
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5, it seems this may have already
  been done, since the last rebuild was of March 16 and the Rebuild Request
  bug of March 19? Rebuilding anyway to be sure (bug 185875)

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 0.8.0-2.fc5
- Rebuild

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.8.0-1
- Update to 0.8.0.
- Add a full description for the devel package.
- Some other minor spec file changes.

* Sun Jun  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.7-2
- Split development files into a devel subpackage.
- Run ldconfig at post (un)install time.
- Fix shared library file modes.
- Improve description.

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.7.7-1
- update to 0.7.7 (fixes x86_64 build)
- include shared libs

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.7.5-3
- rebuild on all arches

* Sun Feb 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.5-2
- 0.7.5.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 0.7.4-2
- Update to 0.7.4.
- Bump release to provide Extras upgrade path.
- Fix spaces/tabs uglyness.

* Sun Aug 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.3-0.fdr.1
- Update to 0.7.3.
- Honor $RPM_OPT_FLAGS.

* Mon Jul 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Improved 64-bit arch build fix.

* Wed May  19 2004 Justin M. Forbes <64bit_fedora@comcast.net> 0:0.6.3-0.fdr.4
- Change linux makefile to use lib64 ifarch x86_64 for sane build

* Sat Apr  3 2004 Dams <anvil[AT]livna.org> 0:0.6.3-0.fdr.3
- Typo in description

* Sun Feb 29 2004 Dams <anvil[AT]livna.org> 0:0.6.3-0.fdr.2
- Added license files as doc
- Requires libebml-devel (headers needed)

* Sat Feb 28 2004 Dams <anvil[AT]livna.org>
- Initial build.

