Name:		tinycdb
Summary:	Utility and library for manipulating constant databases
Summary(zh_CN.UTF-8): 处理常数据库的工具和库
Version:	0.78
Release:	5%{?dist}
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	Public Domain
URL:		http://www.corpit.ru/mjt/tinycdb.html
Source0:	http://www.corpit.ru/mjt/%{name}/%{name}-%{version}.tar.gz
# taken from the 0.77 tarball
Source1:	libcdb.pc

%description
tinycdb is a small, fast and reliable utility and subroutine library for 
creating and reading constant databases. The database structure is tuned
for fast reading.

This package contains tinycdb utility and shared library.

%description -l zh_CN.UTF-8
处理常数据库的工具和库。

%package devel
Summary:	Development files for tinycdb
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases.

This package contains tinycdb development library and header file for 
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
cp %{SOURCE1} debian/
# Fix libdir pathing in pkgconfig file.
sed -i -e 's\/lib\/%{_lib}\g' debian/libcdb.pc

%build
make %{?_smp_mflags} staticlib sharedlib cdb-shared CFLAGS="%{optflags}" 

%install
mkdir -p %{buildroot}%{_libdir}
make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} \
	install install-sharedlib INSTALLPROG=cdb-shared CP="cp -p"
chmod +x %{buildroot}%{_libdir}/*.so.*
rm -f %{buildroot}%{_libdir}/lib*.a
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -p debian/libcdb.pc %{buildroot}%{_libdir}/pkgconfig/libcdb.pc
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc NEWS ChangeLog
%{_bindir}/cdb
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_mandir}/man3/*.3*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 0.78-5
- 为 Magic 3.0 重建

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 0.78-4
- 为 Magic 3.0 重建

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tom Callaway <spot@fedoraproject.org> - 0.78-1
- update to 0.78

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.77-4
- revive

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Chen Lei <supercyper@163.com> - 0.77-2
- add pkgconfig file

* Wed Jul 07 2010 Chen Lei <supercyper@163.com> - 0.77-1
- initial rpm build
