Name:           libcacard
Version:        0.1.2
Release:        4%{?dist}
Summary:        Common Access Card (CAC) Emulation
Summary(zh_CN.UTF-8): 通用访问卡片 (CAC) 仿真
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.spice-space.org/download
Source0:        http://www.spice-space.org/download/libcacard/libcacard-%{version}.tar.bz2
BuildRequires:  nss-devel >= 3.12.8-2

%description
Common Access Card (CAC) emulation library.

%description -l zh_CN.UTF-8
通用访问卡片 (CAC) 仿真库。

%package tools
Summary:        CAC Emulation tools
Summary(zh_CN.UTF-8): CAC 仿真工具
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description tools
CAC emulation tools.

%description tools -l zh_CN.UTF-8
CAC 仿真工具。

%package devel
Summary:        CAC Emulation devel
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
CAC emulation development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libcacard.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/cacard
%{_libdir}/pkgconfig/libcacard.pc
%{_libdir}/libcacard.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/vscclient

%changelog
* Fri Jul 11 2014 Liu Di <liudidi@gmail.com> - 0.1.2-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1.2-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 09 2011 Alon Levy <alevy@redhat.com> - 0.1.2-1
- upstream update
 - upstream updated to 0.1.2 (no rpm was done for this version)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Alon Levy <alevy@redhat.com> - 0.1.0-4
- address review issues:
 - Group for main and devel and tools
 - Requires for devel and tools
- fix changelog for previous entry (day was wrong, and macro quoting)
* Sat Dec 11 2010 Alon Levy <alevy@redhat.com> - 0.1.0-3
- address review issues: defattr typo, %%doc at %%files, remove .*a from install
* Thu Dec 9 2010 Alon Levy <alevy@redhat.com> - 0.1.0-2
- address prereview issues.
* Thu Dec 9 2010 Alon Levy <alevy@redhat.com> - 0.1.0-1
- initial package.

