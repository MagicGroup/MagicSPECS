Name:           dbench
Version:        4.0 
Release:        9%{?dist}
Summary:        Filesystem load benchmarking tool
Summary(zh_CN.UTF-8): 文件系统载入测试工具

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+
Source0:        http://samba.org/ftp/tridge/dbench/dbench-%{version}.tar.gz 
URL:            http://samba.org/ftp/tridge/dbench/README
Patch0:         dbench-4.0-destdir.patch
Patch1:         dbench-4.0-datadir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf popt-devel
  
%description
Dbench is a file system benchmark that generates load patterns similar
to those of the commercial Netbench benchmark, but without requiring a
lab of Windows load generators to run. It is now considered a de facto
standard for generating load on the Linux VFS.

%description -l zh_CN.UTF-8
文件系统载入测试工具。

%prep
%setup -q
%patch0 -p1 -b .destdir 
%patch1 -p1 -b .datadir

%build
./autogen.sh 
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}/man1 INSTALLCMD='install -p'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%dir %{_datadir}/dbench
%{_datadir}/dbench/client.txt
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 14 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 4.0-2
- Fix BR's
* Mon Apr 14 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 4.0-1
- Fix patch
* Mon Apr 14 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 4.0-0
- New upstream release 4.0
* Sat Feb 9 2008 Rahul Sundaram <sundaram@fedoraproject.org> - 3.04-7
- Rebuild for GCC 4.3
* Tue Sep 11 2007 Rahul Sundaram<sundaram@redhat.com> - 3.04-6
- Drop redundant version macro
* Tue Sep 11 2007 Rahul Sundaram<sundaram@redhat.com> - 3.04-5
- Fix version. Dropped BR on glibc-headers
* Tue Sep 11 2007 Rahul Sundaram<sundaram@redhat.com> - 3.04-4
- Fixed docs
* Tue Sep 11 2007 Rahul Sundaram<sundaram@redhat.com> - 3.04-3
- Fixed description, man page location, timestamps, BR and license tag
* Wed Jul 11 2007 John (J5) Palmieri <johnp@redhat.com> - 3.04-2
- add patch to move client.txt to %%{_datadir}/dbench and have the app look
  there for the file
* Wed Jun 20 2007 John (J5) Palmieri <johnp@redhat.com> - 3.04-1
- add patch to respect DESTDIR
- realy make and make install dbench
- place client.txt file in a sane location
* Wed Jun 20 2007 Rahul Sundaram <sundaram@redhat.com>
- split from olpc-utils as suggested in review. Based on the spec from J5
