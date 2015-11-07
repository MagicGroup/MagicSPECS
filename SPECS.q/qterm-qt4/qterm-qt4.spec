%define realver 0.5.12
%define realname qterm

Summary:   BBS client based on Qt library in Linux
Summary(zh_CN.UTF-8): Linux下基于Qt库的BBS客户端
Name:      qterm-qt
Version:   0.5.12
Release:   3%{?dist}
License: GPL
URL:       http://qterm.sourceforge.net
Packager:  yourfeng<yourfeng@eyou.com>
Group:     Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source:    qterm-%{realver}.tar.bz2
# Use the new find_package syntax introduced in CMake 2.6 to workaround a problem with Find_Qt4 shipped with KDE.
# applied in upstream svn1311
Patch0:     qterm-0.5.12-cmake.patch
# Fix build with gcc 4.7, include the missed unistd.h include
# https://sourceforge.net/tracker/?func=detail&aid=3474368&group_id=79581&atid=557094
Patch1:     qterm-0.5.12-gcc-4.7.patch
BuildRoot: %{_tmppath}/%{name}-root

%description
QTerm is a BBS client in Linux

%description -l zh_CN.UTF-8
QTerm是一个Linux下的BBS客户端。

%prep
%setup -q -n %{realname}-%{realver}
%patch0 -p2
%patch1 -p0

%build
mkdir build
cd build 
%{cmake} ..

# Setup for parallel builds
numprocs=`egrep -c ^cpu[0-9]+ /proc/stat || :`
if [ "$numprocs" = "0" ]; then
  numprocs=1
fi

make -j$numprocs

%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# rename the executable to QTerm to prevent conflict with torque-client
mv %buildroot%{_bindir}/{qterm,QTerm}
sed -i 's/Exec=qterm/Exec=QTerm/' %buildroot%{_datadir}/applications/%{realname}.desktop

%clean
rm -rf $RPM_BUILD_ROOT/*

%files
%defattr(-,root,root,-)
%{_bindir}/QTerm
%{_datadir}/%{realname}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/%{realname}.desktop

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.12-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.5.12-2
- 为 Magic 3.0 重建

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 0.4.0-1mgc
- update to 0.4.0

* Mon Jan 9 2006 KanKer <kanker@163.com>
- 0.4.0pre3
* Sat Sep 18 2004 baif (baifcc@hotmail.com)
- 0.3.9
* Thu  Aug 25 2004 baif (baifcc@hotmail.com)
- 0.3.8
* Fri Aug 20 2004 baif (baifcc@hotmail.com)
- 0.3.7
