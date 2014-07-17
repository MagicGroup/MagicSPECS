Name: libibcm
Version: 1.0.5
Release: 7%{?dist}
Summary: Userspace InfiniBand Connection Manager
Summary(zh_CN.UTF-8): 用户空间的 InfiniBand 连接管理器
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibverbs-devel > 1.1.4
ExcludeArch: s390 s390x
%description
libibcm provides a userspace library that handles the majority of the low
level work required to open an RDMA connection between two machines.

%description -l zh_CN.UTF-8
用户空间的 InfiniBand 连接管理器。

%package devel
Summary: Development files for the libibcm library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, libibverbs-devel >= 1.1
%description devel
Development files for the libibcm library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static version of libibcm libraries
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-devel = %{version}-%{release}
%description static
Static version of libibcm library.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libibcm*.so.*
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.5-7
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.5-4
- Bump and rebuild against latest libibverbs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.5-2
- Switch from ExclusiveArch with a big list to ExcludeArch with a small list

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 1.0.5-1
- Update to latest upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Initial package for submission to Fedora review process
