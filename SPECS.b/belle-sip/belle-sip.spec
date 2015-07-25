Name:           belle-sip
Version:	1.4.1
Release:	2%{?dist}
Summary:        Linphone SIP stack
Summary(zh_CN.UTF-8): Linphone 的 SIP 协议栈
License:        GPLv2+
URL:            http://www.linphone.org/
Source0:        http://download.savannah.gnu.org/releases/linphone/belle-sip/%{name}-%{version}.tar.gz
Source1:	antlr-3.4-complete.jar
Patch1:		belle-sip-1.4.0-disable-systembin.patch
Patch2:		belle-sip-1.4.1-mbedtls.patch
BuildRequires:  antlr3-C-devel
BuildRequires:  antlr3-tool
BuildRequires:  polarssl-devel
BuildRequires:  CUnit-devel
BuildRequires:  libtool

%description
Belle-sip is an object oriented C written SIP stack used by Linphone.

%description -l zh_CN.UTF-8
Linphone 的 SIP 协议栈。

%package devel
Summary:       Development libraries for belle-sip
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description    devel
Libraries and headers required to develop software with belle-sip.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1
%patch2 -p1

mkdir -p share/java
cp %{SOURCE1} share/java/antlr3.jar

autoreconf -ifv

%build
#这是一个临时性的措施，后续需要修改。
%configure --disable-tests --disable-silent-rules --with-antlr=%{_builddir}/%{?buildsubdir}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/libbellesip.so.0*

%files devel
%{_includedir}/belle-sip
%{_libdir}/libbellesip.so
%{_libdir}/libbellesip.a
%{_libdir}/pkgconfig/belle-sip.pc

%changelog
* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.4.1-2
- 为 Magic 3.0 重建

* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 1.4.1-1
- 更新到 1.4.1

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-7
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-6
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-5
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-4
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-3
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.4.0-1
- 为 Magic 3.0 重建

* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 1.3.1-3
- 为 Magic 3.0 重建

* Mon Mar 30 2015 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 为 Magic 3.0 重建

* Fri Feb 21 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.3.0-1
- belle-sip-1.3.0
- revert fix FSF address in COPYING

* Sat Jan 18 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-3
- License: GPLv2+
- fix FSF address in COPYING

* Sun Jan 12 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-2
- add %%{?_isa} in -devel Requires
- add verbose option to autoreconf
- verbose build output

* Thu Jan  9 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-1
- Initial RPM release
