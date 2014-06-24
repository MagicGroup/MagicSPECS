%global monodir /usr/lib/mono

Name:    qyoto 
Summary: .NET/Mono bindings for the Qt libraries 
Version: 4.13.2
Release: 1%{?dist}

# libqyoto LGPLv2+, mono bindings GPLv2+
License: LGPLv2+ and GPLv2+
URL:     http://techbase.kde.org/Development/Languages/Qyoto
#URL:     https://projects.kde.org/projects/kde/kdebindings/csharp/qyoto
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: pkgconfig(mono)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(qimageblitz)
BuildRequires: pkgconfig(QtCore) pkgconfig(QtScript) pkgconfig(QtTest) pkgconfig(QtUiTools)
BuildRequires: pkgconfig(QtWebKit) 
BuildRequires: qscintilla-devel
BuildRequires: qwt-devel
BuildRequires: smokeqt-devel
BuildRequires: pkgconfig(sqlite3)

# common name some other distros use
Provides: mono-qt = %{version}-%{release} 

%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
Requires: smokeqt%{?_isa} >= %{version}

#mono_arches?
#ExclusiveArch: %{mono_arches}

%description
%{summary}.

%package devel
Summary: Development libraries for %{name} 
Provides: mono-qt-devel = %{version}-%{release}
Requires: %{name}%{_isa} = %{version}-%{release}
%description devel
This package contains development files for the .NET/Mono bindings 
for the Qt libraries.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%doc AUTHORS COPYING README
# LGPLv2+
%{_libdir}/libqyoto.so.2*
# bindings GPLv2+
%{_libdir}/libqtscript-sharp.so
%{_libdir}/libphonon-sharp.so
%{_libdir}/libqttest-sharp.so
%{_libdir}/libqtuitools-sharp.so
%{_libdir}/libqtwebkit-sharp.so
%{_libdir}/libqscintilla-sharp.so
%{monodir}/gac/qt-dotnet/
%{monodir}/gac/qtscript/
%{monodir}/gac/qttest/
%{monodir}/gac/qtuitools/
%{monodir}/gac/qtwebkit/
%{monodir}/gac/phonon/
%{monodir}/gac/qscintilla/
%{monodir}/qyoto/
%dir %{_datadir}/qyoto/
%{_datadir}/qyoto/key.snk

%files devel
%{_bindir}/csrcc
%{_bindir}/uics
%{_includedir}/qyoto/
%{_libdir}/pkgconfig/qyoto.pc
%{_libdir}/pkgconfig/qtwebkit-sharp.pc
%{_libdir}/pkgconfig/qttest-sharp.pc
%{_libdir}/pkgconfig/qtuitools-sharp.pc
%{_libdir}/pkgconfig/qtscript-sharp.pc
%{_libdir}/libqyoto.so
%{_datadir}/qyoto/cmake/


%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Wed Feb 08 2012 Dan Horák <dan[at]danny.cz> - 4.8.0-2
- set EclusiveArchs

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Tue Jan 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-3
- set %%{monodir} for f17+ differences

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-2
- move lib*-sharp.so to main pkg

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-1
- 4.7.97
- devel: make %%description shorter
- update URL

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-1
- 4.7.95

* Fri Dec 09 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- first try

