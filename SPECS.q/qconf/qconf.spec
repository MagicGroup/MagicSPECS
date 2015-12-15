Summary:        Tool for generating configure script for qmake-based projects
Name:           qconf
Version:        2.0
Release:        1%{?dist}
Epoch:          1

License:        GPLv2+ with exceptions
URL:            http://delta.affinix.com/qconf/
Source0:        http://delta.affinix.com/download/qconf-%{version}.tar.bz2

# Fedora has gridengine package with /usr/bin/qconf
# So I need to use another name
Patch1:         qconf-1.4-rename-binary.patch

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Xml)

%description
QConf allows you to have a nice configure script for your
qmake-based project. It is intended for developers who don't need
(or want) to use the more complex GNU autotools. With qconf/qmake,
it is easy to maintain a cross-platform project that uses a
familiar configuration interface on unix.


%prep
%setup -q
%patch1 -p1

%build
%{_qt5_qmake} PREFIX=%{_prefix}    \
              BINDIR=%{_bindir}    \
              DATADIR=%{_datadir}  \
              QTDIR=%{_libdir}/qt5 \
              CXXFLAGS="%{optflags}"
              
make %{?_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install


%files
%license COPYING
%doc README.md TODO AUTHORS
%{_bindir}/qconf-qt4
%{_datadir}/%{name}


%changelog
* Wed Dec  9 2015 Ivan Romanov <drizt@land.ru> - 1:2.0-1
- New upstream version 2.0
- Use pkgconfig() style
- Drop qconf-2.0-optflags patch (went to upstream)
- Clean .spec file
- Link to Qt5

* Sun Oct 25 2015 Ivan Romanov <drizt@land.ru> - 1:1.4-2
- bump release

* Tue Sep 15 2015 Ivan Romanov <drizt@land.ru> - 1:1.4-1
- Use epoch after wrong 1.5 version in Koji

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4-11
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 01 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4-4
- BR: qt4-devel (#751249)

* Sun Jan 1 2012 Ivan Romanov <drizt@land.ru> - 1.4-3
- Added qt epoch to ruquires. Resolved #751249
- Two minutes before New Year holiday ;)

* Sat Apr 9 2011 Ivan Romanov <drizt@land.ru> - 1.4-2
- added patch to support optflags
- used qmake for build stage instead configure
- changed summary
- corrected codestyle
- fix build requires (thanks to Alexey Panov)
- binary renamed to qconf-qt4

* Thu Nov 12 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 1.4-1
- initial build for Fedora
