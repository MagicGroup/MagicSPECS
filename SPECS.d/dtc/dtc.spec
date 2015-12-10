Name:           dtc
Version:        1.3.0
Release:        7%{?dist}
Summary:        Device Tree Compiler
Summary(zh_CN.UTF-8): 设备树编译器
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv2+
URL:            http://git.jdl.com/gitweb/?p=dtc.git;a=summary
Source:         http://www.jdl.com/software/dtc-v%{version}.tgz
Patch0:         dtc-check.patch
Patch1:         dtc-flattree.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  flex, bison

%description
The Device Tree Compiler generates flattened Open Firmware style device trees
for use with PowerPC machines that lack an Open Firmware implementation

%description -l zh_CN.UTF-8
没有开源固件实现的 PowerPC 机器使用的设备树编译器，用来生成开源固件风格的设备树。

%package -n libfdt
Summary: Device tree library
Summary(zh_CN.UTF-8): 设备树库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%description -n libfdt -l zh_CN.UTF-8
在多种架构上生成开源固件风格设备树的库。

%package -n libfdt-devel
Summary: Development headers for device tree library
Summary(zh_CN.UTF-8): libfdt 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libfdt = %{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt

%description -n libfdt-devel -l zh_CN.UTF-8
libfdt 的开发包。

%prep
%setup -q -n dtc-v%{version}
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=/usr LIBDIR=%{_libdir}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a

# we don't want or need ftdump and it conflicts with freetype-demos, so drop
# it (rhbz 797805)
rm -f $RPM_BUILD_ROOT/%{_bindir}/ftdump

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc GPL
%{_bindir}/*

%files -n libfdt
%defattr(-,root,root,-)
%doc GPL
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%defattr(-,root,root,-)
%{_libdir}/libfdt.so
%{_includedir}/*

%post -n libfdt
/sbin/ldconfig

%postun -n libfdt
/sbin/ldconfig

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.3.0-7
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.3.0-6
- 为 Magic 3.0 重建

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Josh Boyer <jwboyer@redhat.com>
- Don't package ftdump (rhbz 797805)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Fixup error during tarball upload

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Point to git tree for URL (#717217)
- Add libfdt subpackages based on patch from Paolo Bonzini (#443882)
- Update to latest release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Josh Boyer <jwboyer@gmail.com>
- Update to latest release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-2
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Josh Boyer <jwboyer@gmail.com>
- Update to 1.1.0

* Tue Aug 21 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Bump and rebuild

* Thu Aug 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to official 1.0.0 release

* Fri Aug 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update license field

* Mon Jul 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot

* Tue Jul 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot
- Drop upstreamed install patch

* Fri Jun 29 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Fix packaging errors

* Thu Jun 28 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Initial packaging
