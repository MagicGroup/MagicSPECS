Summary: SDL graphics drawing primitives and other support functions
Name: SDL_gfx
Version: 2.0.22
Release: 3%{?dist}
License: LGPLv2
Group: System Environment/Libraries
URL: http://www.ferzkopp.net/Software/SDL_gfx-2.0/
Source: http://www.ferzkopp.net/Software/SDL_gfx-2.0/SDL_gfx-%{version}.tar.gz
Patch0: SDL_gfx-2.0.13-ppc.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: SDL-devel
BuildRequires: libXt-devel

%description
Library providing SDL graphics drawing primitives and other support functions
wrapped up in an addon library for the Simple Direct Media (SDL) cross-platform
API layer.


%package devel
Summary: Development files for SDL_gfx
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: SDL-devel

%description devel
This package contains the files required to develop programs which use SDL_gfx.


%prep
%setup -q
%patch0 -p1 -b .ppc


%build
%configure \
%ifnarch %{ix86}
    --disable-mmx \
%endif
    --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README AUTHORS COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/SDL/*.h
%exclude %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.0.22-3
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 2.0.22-2
- 为 Magic 3.0 重建

* Wed Jul 13 2011 Matthias Saou <http://freshrpms.net/> 2.0.22-1
- Update to 2.0.22.
- Include new pkgconfig file.
- Update descriptions and summaries.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Matthias Saou <http://freshrpms.net/> 2.0.17-1
- Update to 2.0.17.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-4
- Rebuild for new BuildID feature.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-3
- Update License field.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-2
- Minor cleanups.

* Mon May  7 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-1
- Update to 2.0.16.
- Remove no longer needed semicolon patch.
- Add libXt-devel BR to make configure happy (seems unused, though).
- Remove no longer needed autotools BR.

* Mon May  7 2007 Matthias Saou <http://freshrpms.net/> 2.0.13-8
- Include ppc patch (#239130, Bill Nottingham).
- Too late to update to 2.0.16 for F7 (freeze, and soname change).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.0.13-7
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-6
- Fix semicolons in header files (#207665).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-5
- FC6 rebuild.
- Remove gcc-c++ and perl build requirements, they're defaults.
- Add release to the devel sub-package requirement.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-4
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-3
- Rebuild for new gcc/glibc.
- Update URLs.
- Exclude the static library.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jan 28 2005 Matthias Saou <http://freshrpms.net/> 2.0.13-1
- Initial Extras import, minor spec tweaks.

* Tue Dec 21 2004 Dries Verachtert <dries@ulyssis.org> 2.0.13-1
- Updated to release 2.0.13 and removed the patch (has been
  applied upstream)

* Thu Nov 11 2004 Matthias Saou <http://freshrpms.net/> 2.0.12-3
- Explicitly disable mmx for non-ix86 to fix build on x86_64.

* Fri Oct 22 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-3
- fixed some buildrequirements so the correct version of libSDL_gfx.so
  can be found in the list of provides.

* Fri Oct 22 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-2
- rebuild

* Wed Sep 01 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-1
- Update to version 2.0.12.

* Mon Apr 26 2004 Dries Verachtert <dries@ulyssis.org> 2.0.10-1
- Initial package
