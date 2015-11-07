# Upstream uses weird versioning convention
%global upstreamver 2.3_1-opensource

Summary:	QIODevice that compresses data streams
Summary(zh_CN.UTF-8): 可以压缩数据流的 QIODevice
Name:		qtiocompressor
Version:	2.3.1
Release:	7%{?dist}
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtiocompressor/
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtiocompressor-%{upstreamver}.tar.gz
# To add qmake support for convenience for packages using this library:
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-119
Source1:	qtiocompressor.prf
# Don't build examples:
Patch0:		qtiocompressor-build.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
The class works on top of a QIODevice subclass, compressing data before it is
written and decompressing it when it is read. Since QtIOCompressor works on
streams, it does not have to see the entire data set before compressing or
decompressing it. This can reduce the memory requirements when working on large
data sets.

%description -l zh_CN.UTF-8
可以压缩数据流的 QIODevic。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use QtIOCompressor.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{upstreamver}
%patch0 -p1

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
    src/qtiocompressor.h \
    src/QtIOCompressor \
    $RPM_BUILD_ROOT%{_qt4_headerdir}/QtSolutions

mkdir -p $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features/
magic_rpm_clean.sh

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
%doc doc examples
%{_qt4_libdir}/lib*.so
%{_qt4_headerdir}/QtSolutions/
%{_qt4_datadir}/mkspecs/features/%{name}.prf

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.3.1-7
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.3.1-6
- 为 Magic 3.0 重建

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 2.3.1-1
- Initial build. Spec file based on qtsingleapplication.
