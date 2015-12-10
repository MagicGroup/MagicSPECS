Summary:	A modern implementation of a DBM
Summary(zh_CN.UTF-8): DBM 的一个现代实现
Name:		tokyocabinet
Version:	1.4.48
Release:	3%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://fallabs.com/tokyocabinet/
Source:		http://fallabs.com/%{name}/%{name}-%{version}.tar.gz
Patch0:		tokyocabinet-fedora.patch
BuildRequires:	pkgconfig zlib-devel bzip2-devel autoconf

%description
Tokyo Cabinet is a library of routines for managing a database. It is the 
successor of QDBM. Tokyo Cabinet runs very fast. For example, the time required
to store 1 million records is 1.5 seconds for a hash database and 2.2 seconds
for a B+ tree database. Moreover, the database size is very small and can be up
to 8EB. Furthermore, the scalability of Tokyo Cabinet is great.

%description -l zh_CN.UTF-8
DBM 的一个现代实现。

%package devel
Summary:	Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the libraries and header files needed for
developing with %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package devel-doc
Summary:	Documentation files for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
BuildArch:	noarch

%description devel-doc
This package contains documentation files for the libraries and header files
needed for developing with %{name}.

%description devel-doc -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q
%patch0 -p0 -b .fedora

%build
autoconf
%configure --enable-off64 CFLAGS="$CFLAGS"
make %{?_smp_mflags}
										
%install
make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_libdir}/lib%{name}.a
magic_rpm_clean.sh

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog COPYING README
%{_bindir}/tc*
%{_libdir}/libtokyocabinet.so.*
%{_libexecdir}/tcawmgr.cgi
%{_mandir}/man1/tc*.gz

%files devel
%{_includedir}/tc*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/t*.gz

%files devel-doc
%doc doc/*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.4.48-3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.4.48-2
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 1.4.48-1
- 更新到 1.4.48

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.4.47-6
- 为 Magic 3.0 重建

* Tue Sep 18 2012 Honza Horak <hhorak@redhat.com> - 1.4.47-5
- Split devel documentation files into new sub-package tokyocabinet-devel-doc

* Tue Sep 18 2012 Honza Horak <hhorak@redhat.com> - 1.4.47-4
- Minor spec file fixes

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 14 2011 Honza Horak <hhorak@redhat.com> - 1.4.47-1
- Update to 1.4.47

* Wed Jul 13 2011 Honza Horak <hhorak@redhat.com> - 1.4.46-3
- change project URL and source URL to actual destination

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 06 2010 Deji Akingunola <dakingun@gmail.com> - 1.4.46-1
- Update to 1.4.46

* Thu Apr 22 2010 Deji Akingunola <dakingun@gmail.com> - 1.4.43-2
- Enable 64-bit file offset support (Fix Fedora bug #514383)

* Thu Mar 11 2010 Deji Akingunola <dakingun@gmail.com> - 1.4.43-1
- Update to 1.4.43 (Fix Fedora bug #572594)

* Thu Mar 04 2010 Deji Akingunola <dakingun@gmail.com> - 1.4.42-1
- Update to 1.4.42

* Thu Dec 17 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.41-1
- Update to 1.4.41

* Wed Sep 30 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.33-1
- Update to 1.4.33

* Fri Aug 28 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.32-1
- Update to 1.4.32

* Mon Aug 10 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.30-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.23-1
- Update to version 1.4.23

* Tue Mar 03 2009 Deji Akingunola <dakingun@gmail.com> - 1.4.9-1
- Update to version 1.4.9

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Deji Akingunola <dakingun@gmail.com> - 1.3.27-1
- Update to version 1.3.27

* Mon Aug 25 2008 Deji Akingunola <dakingun@gmail.com> - 1.3.4-1
- Update to 1.3.4

* Sun May 25 2008 Masahiro Hasegawa <masahase@gmail.com> - 1.2.6-1
- Update to 1.2.6

* Mon Apr 28 2008 Deji Akingunola <dakingun@gmail.com> - 1.2.5-1
- Update to 1.2.5

* Fri Feb 08 2008 Deji Akingunola <dakingun@gmail.com> - 1.1.14-1
- Update to 1.1.14

* Fri Jan 11 2008 Deji Akingunola <dakingun@gmail.com> - 1.1.7-1
- Update to 1.1.7

* Tue Dec 18 2007 Deji Akingunola <dakingun@gmail.com> - 1.1.4-1
- Update to 1.1.4

* Sat Nov 24 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.8-1
- Update to 1.0.8

* Sat Nov 24 2007 Deji Akingunola <dakingun@gmail.com> - 1.0.6-1
- Initial package
