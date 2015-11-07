Name:          libisf-qt
Version:       0.1
Release:       5%{?dist}
Summary:       library to handle handwriting data in Microsoft’s Ink Serialized Format (ISF)
Summary(zh_CN.UTF-8): 处理微软 ISF 格式手写数据的库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Vendor:        openmamba
Distribution:  openmamba
Packager:      gil <puntogil@libero.it>
URL:           http://kmess.org/projects/isf-qt/
# http://gitorious.org/kmess/libisf-qt/trees/master
Source:        kmess-libisf-qt-master.tar.gz
Patch0:       libisf-qt-lib64-dir.patch
License:       LGPL
BuildRequires: cmake
## AUTOBUILDREQ-BEGIN
BuildRequires: glibc-devel
BuildRequires: libgcc
BuildRequires: qt4-devel
BuildRequires: libstdc++-devel
BuildRequires: libungif-devel
## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
ISF-Qt is a library, written in C++ with the Qt 4 toolkit, which
is capable of reading and writing the ISF format. ISF stands
for "Ink Serialized Format", and is the disk serialization format
used by the Windows.Ink C# library and by the TabletPC platform,
but also by applications like Windows Live Messenger - which
uses ISF to transfer handwriting messages. 

%description -l zh_CN.UTF-8
处理微软 ISF 格式手写数据的库。

%package devel
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:       Static libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
Library to handle handwriting data in Microsoft’s Ink Serialized Format (ISF)

This package contains static libraries and header files need for development.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n kmess-%{name}
%ifarch mips64el x86_64
%patch0 -p1
%endif

%build
mkdir build
pushd build
%cmake_kde4 ..
%__make
popd

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
pushd build
make install DESTDIR=%{buildroot}
popd
magic_rpm_clean.sh

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_kde4_libdir}/libisf-qt.so.*
%doc AUTHORS COPYING ChangeLog README TODO

%files devel
%defattr(-,root,root)
%dir %{_kde4_includedir}/isf-qt
%{_kde4_includedir}/isf-qt/Isf*
%{_kde4_includedir}/isf-qt/*.h
%dir %{_kde4_libdir}/isfqt
%{_kde4_libdir}/isfqt/IsfQtConfig.cmake
%{_kde4_libdir}/libisf-qt.so
%{_datadir}/cmake/Modules/FindIsfQt.cmake

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.1-5
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.1-4
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.1-3
- 为 Magic 3.0 重建

* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 0.1-2
- 为 Magic 3.0 重建

* Sun Dec 12 2010 gil <puntogil@libero.it> 0.1-1mamba
- package created by autospec
