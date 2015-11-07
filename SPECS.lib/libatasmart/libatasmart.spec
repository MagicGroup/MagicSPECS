Name: libatasmart
Version: 匹配到二进制文件
Release: 5%{?dist}
Summary: ATA S.M.A.R.T. Disk Health Monitoring Library
Summary(zh_CN.UTF-8): ATA S.M.A.R.T. 磁盘健康监视库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://0pointer.de/public/libatasmart-%{version}.tar.xz
License: LGPLv2+
Url: http://git.0pointer.de/?p=libatasmart.git;a=summary
BuildRequires: systemd-devel

%description
A small and lightweight parser library for ATA S.M.A.R.T. hard disk
health monitoring.

%description -l zh_CN.UTF-8
轻量的解析 ATA S.M.A.R.T. 硬盘健康监视信息的库。

%package devel
Summary: Development Files for libatasmart Client Development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: vala

%description devel
Development Files for libatasmart Client Development

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm $RPM_BUILD_ROOT%{_docdir}/libatasmart/README
magic_rpm_clean.sh

%files
%defattr(-,root,root)
%doc README LGPL
%{_libdir}/libatasmart.so.*
%{_sbindir}/skdump
%{_sbindir}/sktest

%files devel
%defattr(-,root,root)
%{_includedir}/atasmart.h
%{_libdir}/libatasmart.so
%{_libdir}/pkgconfig/libatasmart.pc
%{_datadir}/vala/vapi/atasmart.vapi
%doc blob-examples/SAMSUNG* blob-examples/ST* blob-examples/Maxtor* blob-examples/WDC* blob-examples/FUJITSU* blob-examples/INTEL* blob-examples/TOSHIBA* blob-examples/MCC*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com>
- 更新到 匹配到二进制文件 index.html

* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.19-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.19-3
- 为 Magic 3.0 重建

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 0.19-2
- rebuild for libudev1

* Sun May 20 2012 Lennart Poettering <lpoetter@redhat.com> - 0.19-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Lennart Poettering <lpoetter@redhat.com> - 0.18-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  9 2009 Matthias Clasen <mclasen@redhat.com> - 0.17-2
- Fix an unitialized variable that causes problems in udisks

* Tue Oct 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.17-1
- New upstream release
- Fixes bug 491552

* Tue Sep 29 2009 Lennart Poettering <lpoetter@redhat.com> 0.16-1
- New upstream release
- Second try at fixing #515881

* Fri Sep 18 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-1
- New upstream release
- Fixes #515881

* Thu Aug 6 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Lennart Poettering <lpoetter@redhat.com> 0.13-1
- New upstream release

* Wed Apr 15 2009 Lennart Poettering <lpoetter@redhat.com> 0.12-1
- New upstream release

* Tue Apr 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-1
- New upstream release

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.10-1
- New upstream release

* Sun Apr 12 2009 Lennart Poettering <lpoetter@redhat.com> 0.9-1
- New upstream release

* Fri Apr 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.8-1
- New upstream release

* Tue Apr 7 2009 Lennart Poettering <lpoetter@redhat.com> 0.7-1
- New upstream release

* Sat Apr 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New upstream release

* Fri Apr 3 2009 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New upstream release

* Thu Apr 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.4-1
- New upstream release

* Tue Mar 24 2009 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- New upstream release

* Thu Mar 19 2009 Lennart Poettering <lpoetter@redhat.com> 0.2-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 25 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-1
- Initial version
