Summary: Rendering of internationalized text for SDL (Simple DirectMedia Layer)
Summary(zh_CN.UTF-8): SDL 渲染国际化文本的库
Name: SDL_Pango
Version: 0.1.2
Release: 23%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://sdlpango.sourceforge.net/

Source0: http://downloads.sf.net/sdlpango/SDL_Pango-%{version}.tar.gz
Source1: doxygen.png
Patch0: SDL_Pango-0.1.2-suppress-warning.patch
Patch1: SDL_Pango-0.1.2-API-adds.patch
Patch2: SDL_Pango-0.1.2-matrix_declarations.patch

BuildRequires: pango-devel, SDL-devel, dos2unix
BuildRequires: autoconf, automake, libtool

%description
Pango is the text rendering engine of GNOME 2. SDL_Pango connects that engine
to SDL, the Simple DirectMedia Layer.
%description -l zh_CN.UTF-8
SDL 渲染国际化文本的库。

%package devel
Summary: Development files for SDL_pango
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pango-devel, SDL-devel, pkgconfig

%description devel
Development files for SDL_pango.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .suppress-warning
%patch1 -p1 -b .API-adds
%patch2 -p1 -b .matrix_declarations
# Clean up, we include the entire "docs/html" content for the devel package
rm -rf docs/html/CVS/
# Replace the corrupt doxygen.png file with a proper one
install -m 0644 -p %{SOURCE1} docs/html/doxygen.png
# Fix the (many) DOS encoded files, not *.png since they get corrupt
find . -not -name \*.png -type f -exec dos2unix -k {} \;
# For FC-5 x86_64 this is required, or the shared library doesn't get built
autoreconf -i
libtoolize --copy --force


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

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
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.1.2-23
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 0.1.2-22
- 为 Magic 3.0 重建

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Jaromir Capik <jcapik@redhat.com> - 0.1.2-18
- Fixing FTBFS

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.1.2-15
- Add disttag, cleanup spec

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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

