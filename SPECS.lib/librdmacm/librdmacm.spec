Name: librdmacm
Version: 1.0.21
Release: 2%{?dist}
Summary: Userspace RDMA Connection Manager
Summary(zh_CN.UTF-8): 用户空间的 RDMA 连接管理器
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: https://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x
BuildRequires: libibverbs-devel > 1.1.4, chrpath

%description
librdmacm provides a userspace RDMA Communication Managment API.

%description -l zh_CN.UTF-8
用户空间的 RDMA 连接管理器。

%package devel
Summary: Development files for the librdmacm library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release} libibverbs-devel%{?_isa}

%description devel
Development files for the librdmacm library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static development files for the librdmacm library
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库

%description static
Static libraries for the librdmacm library.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%package utils
Summary: Examples for the librdmacm library
Summary(zh_CN.UTF-8): %{name} 的样例
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name} = %{version}-%{release}

%description utils
Example test programs for the librdmacm library.

%description utils -l zh_CN.UTF-8
%{name} 的样例测试程序。

%prep
%setup -q

%build
%configure LDFLAGS=-lpthread
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
# remove unpackaged files from the buildroot
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# kill rpaths
chrpath -d %{buildroot}%{_bindir}/*
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/librdmacm*.so.*
%{_libdir}/rsocket/*.so.*
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/rsocket/*.so
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/rsocket/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.21-2
- 更新到 1.0.21

* Wed Jul 30 2014 Liu Di <liudidi@gmail.com> - 1.0.19-1
- 更新到 1.0.19

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.15-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.15-1
- Update to latest upstream tarball
- Add in latest git commits as patches

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-1
- Update to latest upstream release
- Rebuild against latest libibverbs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 19 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-3
- Fix up link problem caused by change to default DSO linking (bz564870)

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-2
- ExcludeArch s390(x) as the hardware doesn't exist there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 1.0.10-1
- Update to latest upstream release
- Change Requires on -devel package (bz533937)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Mar 29 2008 Roland Dreier <rolandd@cisco.com> - 1.0.7-1
- New upstream release

* Fri Feb 22 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-2
- Spec file cleanups from Fedora review: add BuildRequires for
  libibverbs, and move the static library to -static.

* Fri Feb 15 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-1
- Initial Fedora spec file

