%define realver 0.4.1

Summary:   BBS client based on Qt library in Linux
Summary(zh_CN.UTF-8): Linux下基于Qt库的BBS客户端
Name:      qterm
Version:   0.4.1
Release:   1%{?dist}
License: GPL
URL:       http://qterm.sourceforge.net
Packager:  yourfeng<yourfeng@eyou.com>
Group:     Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
Source:    qterm-%{realver}.tar.bz2
Patch0: qterm.cfg-magic.patch
Patch1:	qterm-0.4.1-lcrypto.patch
Patch2: qterm-0.4.1-fix-Wl.patch
BuildRoot: %{_tmppath}/%{name}-root

%description
QTerm is a BBS client in Linux

%description -l zh_CN.UTF-8
QTerm是一个Linux下的BBS客户端。

%prep
%setup -q -n %{name}-%{realver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
#make -f admin/Makefile.common
%configure

# Setup for parallel builds
numprocs=`egrep -c ^cpu[0-9]+ /proc/stat || :`
if [ "$numprocs" = "0" ]; then
  numprocs=1
fi

make -j$numprocs

%install
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT
find . -type d | sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' > $RPM_BUILD_DIR/file.list.qterm
find . -type f | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.qterm
find . -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.qterm
echo "%{_datadir}/qterm/script/*" >> $RPM_BUILD_DIR/file.list.qterm

%clean
rm -rf $RPM_BUILD_ROOT/*
rm -rf $RPM_BUILD_DIR/qterm
rm -rf ../file.list.qterm


%files -f ../file.list.qterm

%changelog
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
