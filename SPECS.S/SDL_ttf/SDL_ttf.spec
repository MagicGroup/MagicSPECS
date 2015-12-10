Name:		SDL_ttf
Version:	2.0.11
Release:	5%{?dist}
Summary:	Simple DirectMedia Layer TrueType Font library
Summary(zh_CN.UTF-8): SDL TrueType 字体库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL_ttf/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	zlib-devel


%description
This library allows you to use TrueType fonts to render text in SDL
applications.
%description -l zh_CN.UTF-8
SDL TrueType 字体库。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/SDL/
%{_libdir}/pkgconfig/SDL_ttf.pc

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.11-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.11-4
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 2.0.11-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.0.11-2
- 为 Magic 3.0 重建

* Tue Jan 31 2012 Jon Ciesla <limburgher@gmail.com> - 2.0.11-1
- New upstream.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 12 2010 Thomas Janssen <thomasj@fedoraproject.org> 2.0.10-1
- update to 2.0.10
- fixes #538044

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.0.9-4
- Rebuild for gcc-4.3.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 2.0.9-3
- Rebuild.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 2.0.9-2
- Update license tag.

* Mon Jul 30 2007 Brian Pepple <bpepple@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9.
- Drop freetype-internals patch. fixed upstream.

* Thu Aug 31 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0.8-2
- Update for FC6.

* Sat Aug 26 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8.
- Simplify description & summary for devel package.

* Mon Feb 13 2006 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-4
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 14 2005 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-3
- Add patch for Bug #171020.

* Thu Sep 29 2005 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-2
- General spec formatting changes.
- Rebuild for FC4 upgrade path.

* Sun Sep 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.0.7-1
- 2.0.7, patches applied upstream.
- Require SDL-devel in -devel.
- Build with dependency tracking disabled.
- Don't ship static libs.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.0.6-5
- rebuilt

* Wed Mar 21 2004 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.4
- fix build on FC2-test (bug #1436

* Mon Nov 10 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.3
- add missing buildreq zlib-devel

* Sun Aug 24 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.2
- address issues in #631
- add full URL to source
- better description for -devel package

* Sat Aug 23 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.1
- Fedoraize
- patch to compile on RH9

* Wed Jan 19 2000 Sam Lantinga
- converted to get package information from configure
* Sun Jan 16 2000 Hakan Tandogan <hakan@iconsult.com>
- initial spec file

