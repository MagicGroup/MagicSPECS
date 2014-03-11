# Upstream uses weird versioning convention
%global upstreamver 2.6_1-opensource

Summary:	Qt library to start applications only once per user
Name:		qtsingleapplication
Version:	2.6.1
Release:	8%{?dist}
Group:		System Environment/Libraries
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsingleapplication
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtsingleapplication-%{upstreamver}.tar.gz
# The following source and 2 patches are sent upstream:
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-119
# To add qmake support for convenience for packages using this library:
Source1:	qtsingleapplication.prf
Source2:	qtsinglecoreapplication.prf
# Don't build examples, Include qtsinglecoreapplication library in the build:
Patch0:		qtsingleapplication-build.diff
# The library includes a duplicate of qtlockedfile. We link to it dynamically instead:
Patch1:		qtsingleapplication-dont-bundle-external-libs.patch
# Additional API for building clementine
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-133
Patch2:		qtsingleapplication-add-api.patch
# gcc-4.7 compilation fix
Patch3:		qtsingleapplication-gcc47.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	qt4-devel
BuildRequires:	qtlockedfile-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use QtSingleApplication.

%package -n qtsinglecoreapplication
Summary:	Qt library to start applications only once per user
Group:		System Environment/Libraries
Obsoletes:	%{name} < 2.6.1-3

%description -n qtsinglecoreapplication
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

%package -n qtsinglecoreapplication-devel
Summary:	Development files for qtsinglecoreapplication
Group:		Development/Libraries
Obsoletes:	%{name}-devel < 2.6.1-3
Requires:	qtsinglecoreapplication = %{version}-%{release}
Requires:	qt4-devel

%description -n qtsinglecoreapplication-devel
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.

%prep
%setup -q -n %{name}-%{upstreamver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# We already disabled bundling this extrenal library.
# But just to make sure:
rm src/{QtLocked,qtlocked}*


%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
%{_qt4_qmake}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

# libraries
mkdir -p $RPM_BUILD_ROOT%{_qt4_libdir}
cp -a lib/* $RPM_BUILD_ROOT%{_qt4_libdir}
chmod 755 $RPM_BUILD_ROOT%{_qt4_libdir}/*.so.*.*.*

# headers
mkdir -p $RPM_BUILD_ROOT%{_qt4_headerdir}/QtSolutions
cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    $RPM_BUILD_ROOT%{_qt4_headerdir}/QtSolutions

mkdir -p $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n qtsinglecoreapplication -p /sbin/ldconfig

%postun -n qtsinglecoreapplication -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%{_qt4_libdir}/lib*SingleApplication*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc examples
%{_qt4_libdir}/lib*SingleApplication*.so
%dir %{_qt4_headerdir}/QtSolutions/
%{_qt4_headerdir}/QtSolutions/QtSingleApplication
%{_qt4_headerdir}/QtSolutions/%{name}.h
%{_qt4_datadir}/mkspecs/features/%{name}.prf

%files -n qtsinglecoreapplication
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.*
%{_qt4_libdir}/lib*SingleCoreApplication*.so.*

%files -n qtsinglecoreapplication-devel
%defattr(-,root,root,-)
%{_qt4_libdir}/lib*SingleCoreApplication*.so
%dir %{_qt4_headerdir}/QtSolutions/
%{_qt4_headerdir}/QtSolutions/QtSingleCoreApplication
%{_qt4_headerdir}/QtSolutions/qtsinglecoreapplication.h
%{_qt4_datadir}/mkspecs/features/qtsinglecoreapplication.prf

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 11 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6.1-6
- gcc-4.7 compilation fix

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6.1-4
- Make the additional API patch backwards compatible

* Wed Jul 21 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6.1-3
- Split the qtsinglecoreapplication bits into their own subpackages

* Fri Jul 16 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6.1-2
- Add additional API to support clementine.

* Sun Jun 04 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6.1-1
- Change version to 2.6.1. Upstream uses weird version convention 2.6_1
- Own the directory %%{_qt4_headerdir}/QtSolutions/

* Sat May 01 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6-3
- Add comments to the extra source and patches
- Add a chmod 755 to make sure that the library gets the right permission

* Thu Apr 15 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6-2
- Include .prf file
- Don't bundle external qtlockedfile library
- Fix typo in the description

* Sun Apr 11 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.6-1
- Initial Fedora package. Specfile partly borrowed from opensuse

* Thu Dec  3 2009 Todor Prokopov <koprok@nand.bg>
- Initial package.
