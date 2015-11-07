%global commit0	   5a07df503a6f01280f493cbcc2aace462b9dee57
%global commitdate 20150629

Summary:	QFile extension with advisory locking functions
Summary(zh_CN.UTF-8): 带有锁定功能的 QFile 扩展
Name:		qtlockedfile
Version:	2.4
Release:	7%{?dist}
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://doc.qt.digia.com/solutions/4/qtlockedfile/qtlockedfile.html
Source0:	https://github.com/qtproject/qt-solutions/archive/%{commit0}.tar.gz#/%{name}-%{commit0}.tar.gz
Source1:	qtlockedfile.prf
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	qt4-devel
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.
%description -l zh_CN.UTF-8
带有锁定功能的 QFile 扩展。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel

%description	devel
This package contains libraries and header files for developing applications
that use QtLockedFile.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package qt5
Summary:	QFile extension with advisory locking functions (Qt5)
Summary(zh_CN.UTF-8): 带有锁定功能的 QFile 扩展（Qt5）
Requires:	qt5-qtbase

%description qt5
This class extends the QFile class with inter-process file locking capabilities.
If an application requires that several processes should access the same file,
QtLockedFile can be used to easily ensure that only one process at a time is
writing to the file, and that no process is writing to it while others are
reading it.
This is a special build against Qt5.
%description qt5 -l zh_CN.UTF-8
带有锁定功能的 QFile 扩展（Qt5）。

%package qt5-devel
Summary:	Development files for %{name}-qt5
Summary(zh_CN.UTF-8): %{name}-qt5 的开发包
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	qt5-qtbase-devel

%description qt5-devel
This package contains libraries and header files for developing applications
that use QtLockedFile with Qt5.
%description qt5-devel -l zh_CN.UTF-8
%{name}-qt5 的开发包。

%prep
%setup -qn qt-solutions-%{commit0}/%{name}
# use versioned soname
sed -i s,head,%{version}, common.pri
# do not build example source
sed -i /example/d %{name}.pro

%build
# Does not use GNU configure
./configure -library
%{_qt4_qmake}
make %{?_smp_mflags}
mkdir qt5
pushd qt5
%{qmake_qt5} ..
make %{?_smp_mflags}
popd

%install
# libraries
mkdir -p %{buildroot}%{_libdir}
cp -ap lib/* %{buildroot}%{_libdir}

# headers
mkdir -p %{buildroot}%{_qt4_headerdir}/QtSolutions %{buildroot}%{_qt5_headerdir}
cp -ap src/qtlockedfile.h src/QtLockedFile %{buildroot}%{_qt4_headerdir}/QtSolutions
cp -ap %{buildroot}%{_qt4_headerdir}/QtSolutions %{buildroot}%{_qt5_headerdir}

install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt4_datadir}/mkspecs/features/qtlockedfile.prf
install -p -D -m644 %{SOURCE1} %{buildroot}%{_qt5_archdatadir}/mkspecs/features/qtlockedfile.prf


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README.TXT
# Caution! do not include any unversioned .so symlink (belongs to -devel)
%{_libdir}/libQtSolutions_LockedFile*.so.*

%files devel
%doc doc/html/ example/
%{_qt4_headerdir}/QtSolutions/
%{_libdir}/libQtSolutions_LockedFile*.so
%{_qt4_datadir}/mkspecs/features/qtlockedfile.prf

%files qt5
%doc README.TXT
# Caution! do not include any unversioned .so symlink (belongs to -devel)
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so.*

%files qt5-devel
%doc doc/html/ example/
%{_qt5_headerdir}/QtSolutions/
%{_qt5_libdir}/libQt5Solutions_LockedFile*.so
%{_qt5_archdatadir}/mkspecs/features/qtlockedfile.prf


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.4-7
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.4-6
- 为 Magic 3.0 重建

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
