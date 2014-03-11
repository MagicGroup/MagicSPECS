Summary:	QFile extension with advisory locking functions
Name:		qtlockedfile
Version:	2.4
Release:	5%{?dist}
Group:		System Environment/Libraries
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtlockedfile
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/%{name}-%{version}_1-opensource.tar.gz
Source1:	qtlockedfile.prf
Patch0:		qtlockedfile-dont-build-example.patch
# Remove unnecessary linkage to libQtGui
Patch1:		qtlockedfile-dont-link-qtgui.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	qt4-devel
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use QtLockedFile.

%prep
%setup -q -n %{name}-%{version}_1-opensource
%patch0 -p1 -b .no-example
%patch1 -p1 -b .dont-link-qtgui


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

# headers
mkdir -p $RPM_BUILD_ROOT%{_qt4_headerdir}/QtSolutions
cp -a \
    src/qtlockedfile.h \
    src/QtLockedFile \
    $RPM_BUILD_ROOT%{_qt4_headerdir}/QtSolutions

mkdir -p $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%{_qt4_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc example
%{_qt4_libdir}/lib*.so
%{_qt4_headerdir}/QtSolutions/
%{_qt4_datadir}/mkspecs/features/%{name}.prf

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.4-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 16 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.4-2
- Remove unnecessary linkage to libQtGui

* Thu Apr 15 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.4-1
- Initial Fedora package.
