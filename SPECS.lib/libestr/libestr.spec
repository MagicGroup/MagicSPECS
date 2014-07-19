Name:           libestr
Version:        0.1.9
Release:        3%{?dist}
Summary:        String handling essentials library
Summary(zh_CN.UTF-8): 字符串处理要素库

License:        LGPLv2+
URL:            http://libestr.adiscon.com/
Source0:        http://libestr.adiscon.com/files/download/libestr-%{version}.tar.gz

%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%description -l zh_CN.UTF-8
这是 Rsyslog 服务使用的字条串处理库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use libestr.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --with-pic
V=1 make %{?_smp_mflags}

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README COPYING AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libestr.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libestr.pc

%changelog
* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 0.1.9-3
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 0.1.9-2
- 为 Magic 3.0 重建

* Tue Jan 07 2014 Tomas Heinrich <theinric@redhat.com> - 0.1.9-1
- rebase to 0.1.9
- remove patch 0; doesn't seem to be necessary anymore

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Tomas Heinrich <theinric@redhat.com> - 0.1.5-1
- rebase to 0.1.5

* Wed Dec 12 2012 Mahaveer Darade <mdarade@redhat.com> - 0.1.4-1
- upgrade to upstream version 0.1.4
- correct an impossible timestamp in an older changelog entry

* Thu Sep 20 2012 mdarade <mdarade@redhat.com> - 0.1.3-3
- Fixed broken configure script

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.1.3-2
- Removed unnecessary macros in spec file.

* Tue Aug 7 2012 Mahaveer Darade <mdarade@redhat.com> - 0.1.3-1
- Initial port libestr-0.1.3
