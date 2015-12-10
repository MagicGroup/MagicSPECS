Name:           libquvi
Version: 0.9.4
Release: 3%{?dist}
Summary:        A cross-platform library for parsing flash media stream
Summary(zh_CN.UTF-8): 解析 flash 媒体流的跨平台库

Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
License:        LGPLv2+
URL:            http://quvi.sourceforge.net/
Source0:        http://downloads.sourceforge.net/quvi/%{name}-%{version}.tar.xz

BuildRequires:  libquvi-scripts >= 0.9 
BuildRequires:	libcurl-devel lua-devel
Requires:       libquvi-scripts >= 0.9

%description
Libquvi is a cross-platform library for parsing flash media stream
URLs with C API.

%description -l zh_CN.UTF-8
解析 flash 媒体流的跨平台库。

%package devel
Summary: Files needed for building applications with libquvi
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Obsoletes: quvi-devel <= 0.2.19
Provides:  quvi-devel = %{version}-%{release}

%description devel
Files needed for building applications with libquvi

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --enable-static=no

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING README 
%{_libdir}/%{name}-0.9-%{version}.so
%{_mandir}/man3/%{name}.3*

%files devel
%{_includedir}/quvi-0.9
%{_libdir}/%{name}-0.9.so
%{_libdir}/pkgconfig/%{name}-0.9.pc
%{_mandir}/man7/quvi-object.7*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.9.4-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.9.4-2
- 为 Magic 3.0 重建

* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 0.9.4-1
- 更新到 0.9.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.1-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.1-1
- Update to 0.4.1

* Sun Dec 11 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-5
- Fix Obsoletes version

* Wed Oct 19 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-4
- Remove the pkgconfig require for the devel package

* Tue Oct 11 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-3
- Fix BuilRequires

* Sun Oct  9 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-2
- Fix requires

* Sat Oct  8 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-1
- Initial build
