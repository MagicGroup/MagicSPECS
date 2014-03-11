Summary: Rendering of internationalized text for SDL (Simple DirectMedia Layer)
Name: SDL_Pango
Version: 0.1.2
Release: 13%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://sdlpango.sourceforge.net/
Source0: http://downloads.sf.net/sdlpango/SDL_Pango-%{version}.tar.gz
Source1: doxygen.png
Patch0: SDL_Pango-0.1.2-suppress-warning.patch
Patch1: SDL_Pango-0.1.2-API-adds.patch
Patch2: SDL_Pango-0.1.2-matrix_declarations.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: pango-devel, SDL-devel, dos2unix
BuildRequires: autoconf, automake, libtool

%description
Pango is the text rendering engine of GNOME 2. SDL_Pango connects that engine
to SDL, the Simple DirectMedia Layer.


%package devel
Summary: Development files for SDL_pango
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pango-devel, SDL-devel, pkgconfig

%description devel
Development files for SDL_pango.


%prep
%setup -q
%patch0 -p1 -b .suppress-warning
%patch1 -p1 -b .API-adds
%patch2 -p1 -b .matrix_declarations
# Clean up, we include the entire "docs/html" content for the devel package
%{__rm} -rf docs/html/CVS/
# Replace the corrupt doxygen.png file with a proper one
%{__install} -m 0644 -p %{SOURCE1} docs/html/doxygen.png
# Fix the (many) DOS encoded files, not *.png since they get corrupt
find . -not -name \*.png -type f -exec dos2unix -k {} \;
# For FC-5 x86_64 this is required, or the shared library doesn't get built
autoreconf
libtoolize --copy --force


%build
%configure --disable-static
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/html/*
%{_includedir}/SDL_Pango.h
%{_libdir}/pkgconfig/SDL_Pango.pc
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.1.2-13
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 0.1.2-9
- Include matrix declaraction patch (#475118), adapted in order to not
  create a regression from the "supress warning" patch.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 0.1.2-7
- Rebuild for new BuildID feature.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 0.1.2-6
- Update License field.
- Remove dist tag, since the package will seldom change.

* Fri Sep 29 2006 Matthias Saou <http://freshrpms.net/> 0.1.2-5
- Update source URL.
- Disable static lib building instead of excluding it from the files list.

* Fri Sep 29 2006 Matthias Saou <http://freshrpms.net/> 0.1.2-4
- Add autoreconf and libtoolize calls since on FC5 x86_64 the shared library
  isn't build otherwise.
- Add API-adds patch (submitted upstream), required for the only project known
  to use SDL_Pango, so it does makes kind of sense...

* Tue Sep 26 2006 Matthias Saou <http://freshrpms.net/> 0.1.2-3
- Use dos2unix to convert all DOS encoded files.
- Replace the corrupt doxygen.png file with a proper one.

* Tue Sep 26 2006 Matthias Saou <http://freshrpms.net/> 0.1.2-2
- Change %%makeinstall to using DESTDIR, according to the guidelines.
- Include patch from Mamoru Tasaka to remove all compilation warnings.

* Fri Sep 22 2006 Matthias Saou <http://freshrpms.net/> 0.1.2-1
- Initial RPM release.

