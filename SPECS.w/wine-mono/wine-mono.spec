%{?mingw_package_header}

Name:           wine-mono
Version:        4.5.2
Release:        2%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
Group:          Development/Libraries
URL:            http://wiki.winehq.org/Mono
Source0:        http://sourceforge.net/projects/wine/files/Wine%20Mono/%{version}/%{name}-%{version}.tar.gz
Patch0:         wine-mono-build-msifilename.patch

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    armv7hl ppc s390x

# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-crt
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-crt

BuildRequires:  autoconf automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  zip
BuildRequires:  wine-core wine-wow
BuildRequires:  wine-devel
BuildRequires:  mono-core
BuildRequires:  bc

Requires: wine-filesystem

%description
Windows Mono library required for Wine.

%prep
%setup -q
%patch0 -p1 -b.msifilename

%build
# make sure this builds on x86-64
if [ -x %{_bindir}/wine ] ; then
   MAKEOPTS=%{_smp_mflags} MSIFILENAME=wine-mono-%{version}.msi ./build-winemono.sh
else
   MAKEOPTS=%{_smp_mflags} WINE=%{_bindir}/wine64 MSIFILENAME=wine-mono-%{version}.msi ./build-winemono.sh
fi

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono
install -p -m 0644 wine-mono-%{version}.msi \
    %{buildroot}%{_datadir}/wine/mono/wine-mono-%{version}.msi

# prep licenses
cp mono/LICENSE mono-LICENSE
cp mono/COPYING.LIB mono-COPYING.LIB

pushd mono/mcs

sed -i 's/\r//' LICENSE.MSPL

iconv -f iso8859-1 -t utf-8 LICENSE.MSPL > LICENSE.MSPL.conv && mv -f LICENSE.MSPL.conv LICENSE.MSPL

for l in `ls LICENSE*`; do
echo $l
cp $l ../../mono-mcs-$l
done

popd

cp mono-basic/README mono-basic-README
cp mono-basic/LICENSE mono-basic-LICENSE
cp MonoGame/LICENSE.txt MonoGame-LICENSE.txt

%files
%doc COPYING README
%doc mono-LICENSE mono-COPYING.LIB mono-mcs*
%doc mono-basic-README mono-basic-LICENSE
%doc MonoGame-LICENSE.txt
%{_datadir}/wine/mono/wine-mono-%{version}.msi

%changelog
* Sat Dec 14 2013 Michael Cronenworth <mike@cchtml.com>
- 4.5.2-2
- Add ExcludeArch as Mono requires an x86 builder host

* Sun Dec 08 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 4.5.2-1
- version upgrade

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.8-3
- Fix FTBFS against latest automake
- Added BR: bc

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.8-1
- version upgrade

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-7
- add mingw-filesystem BR
- fix header macro

* Fri Jun 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-6
- rename to wine-mono

* Wed Jun 27 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-5
- add conditional so package builds on x86-64 builders as well

* Tue Jun 26 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-4
- add -e option to echo in build script to fix idt files generation

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-3
- pull some upstream patches from git

* Tue Jun 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-2
- rename msi according to what wine expects

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-1
- Initial release
