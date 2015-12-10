Summary: OpenFabrics Alliance InfiniBand MAD library
Summary(zh_CN.UTF-8): 开放结构联盟的 InfiniBand MAD 库
Name: libibmad
Version: 1.3.12
Release: 5%{?dist}
License: GPLv2 or BSD
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: https://www.openfabrics.org/downloads/management/%{name}-%{version}.tar.gz
Url: http://openfabrics.org/
BuildRequires: libibumad-devel = 1.3.7, libtool, glibc-static
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
ExcludeArch: s390 s390x

%description
libibmad provides low layer IB functions for use by the IB diagnostic
and management programs. These include MAD, SA, SMP, and other basic
IB functions. 

%description -l zh_CN.UTF-8
开放结构联盟的 InfiniBand MAD 库。

%package devel
Summary: Development files for the libibmad library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}, libibumad-devel

%description devel
Development files for the libibmad library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary: Static version of the libibmad library
Summary(zh_CN.UTF-8): %{name} 的静态库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-devel = %{version}-%{release}

%description static
Static version of the libibmad library

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libibmad*.so.*
%doc AUTHORS COPYING ChangeLog

%files devel
%defattr(-,root,root)
%{_libdir}/libibmad.so
%{_includedir}/infiniband/*.h

%files static
%defattr(-,root,root)
%{_libdir}/libibmad.a

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.3.12-5
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.3.12-4
- 更新到 1.3.12

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.3.11-3
- 更新到 1.3.11

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3.8-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.3.8-1
- Update to latest upstream version

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.3.7-1
- Update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 27 2010 Doug Ledford <dledford@redhat.com> - 1.3.4-1
- New upstream version

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.3.3-2
- ExcludeArch s390(x) as there's no hardware support there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 1.3.3-1
- Update to latest upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Doug Ledford <dledford@redhat.com> - 1.3.2-1
- Update to latest upstream version
- Require the same version of libibumad as our version

* Wed Apr 22 2009 Doug Ledford <dledford@redhat.com> - 1.3.1-1
- Update to latest upstream version

* Sat Mar 21 2009 Robert Scheck <robert@fedoraproject.org> - 1.2.0-3
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.2.0-1
- Initial package for Fedora review process
