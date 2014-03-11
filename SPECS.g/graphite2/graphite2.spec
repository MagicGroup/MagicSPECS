Name:           graphite2
Version:        1.2.0
Release:        4%{?dist}
Summary:        Font rendering capabilities for complex non-Roman writing systems
Group:          Development/Tools

License:        LGPLv2+ and (Netscape or GPLv2 or LGPLv2)
URL:            http://sourceforge.net/projects/silgraphite/
Source0:        http://downloads.sourceforge.net/silgraphite/graphite2-%{version}.tgz
Patch0:         graphite-arm-nodefaultlibs.patch
Patch1:         graphite2-1.2.0-cmakepath.patch

BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  doxygen asciidoc
BuildRequires:  texlive-collection-latexextra
BuildRequires:  texlive-helvetic

Obsoletes:      silgraphite < 2.3.1-5

%description
Graphite2 is a project within SIL’s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create “smart fonts” capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with graphite2
Group: Development/Libraries

Obsoletes: silgraphite-devel < 2.3.1-5

%description devel
Includes and definitions for developing with graphite2.

%prep
%setup -q
%patch0 -p1 -b .arm
%patch1 -p1 -b .cmake

%build
%cmake -DGRAPHITE2_COMPARE_RENDERER=OFF .
make %{?_smp_mflags}
make docs
sed -i -e 's!<a id="id[a-z]*[0-9]*"></a>!!g' doc/manual.html

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%check
ctest

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE COPYING ChangeLog
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3.0.1

%files devel
%doc doc/manual.html
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/graphite2-release.cmake
%{_libdir}/%{name}/graphite2.cmake
%{_includedir}/%{name}
%{_libdir}/libgraphite2.so
%{_libdir}/libgraphite2.so.3
%{_libdir}/pkgconfig/graphite2.pc

%changelog
* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-4
- Drop refman.pdf as its same as manual.html
- patch install path for cmake files as they are arch dependent

* Tue Jan 29 2013 Kalev Lember <kalevlember@gmail.com> - 1.2.0-3
- Move manual.html to -devel subpackage

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-2
- revert the wrongly committed f18 spec to f19
- spec file cleanup
- thanks to jnovy for finding me minimum texlive BR
- partial multilib fix for manual.html

* Fri Nov 9 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.0-1
- New upstream release
* Wed Oct 3 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.1-4
- expand license field to cover tri-licenced GrUtfTextSrc test
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.1-2
- Fix FTBFS on ARM
* Mon Feb 27 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.1-1
- New upstream release
* Wed Feb 8 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.0-1
- New upstream release
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 23 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.3-1
- New upstream release
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-3
- Obsolete silgraphite
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-2
- Removed dependency on silgraphite-devel
- Stopped building comparerenderer - the only thing that depended on silgraphite
* Fri Aug 19 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-1
- Rebase to new release
- SPEC Cleanup
- Documentation is now properly installed
* Wed Aug 17 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-2
- Added some necessary requires
* Wed Aug 10 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-1
- Initial build of graphite2
