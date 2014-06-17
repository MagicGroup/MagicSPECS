Name:           belle-sip
Version:        1.3.0
Release:        11%{?dist}
Summary:        Linphone SIP stack
Summary(zh_CN.UTF-8): Linphone SIP 
License:        GPLv2+
URL:            http://www.linphone.org/
Source0:        http://download.savannah.gnu.org/releases/linphone/belle-sip/%{name}-%{version}.tar.gz
#Source1:	https://github.com/antlr/website-antlr3/blob/gh-pages/download/antlr-3.4-complete.jar?raw=true"
Source1:	antlr.jar

BuildRequires:  polarssl-devel
BuildRequires:  CUnit-devel
BuildRequires:  libtool
BuildRequires:	jdk

%description
Belle-sip is an object oriented C written SIP stack used by Linphone.

%description -l zh_CN.UTF-8
这是 Linphone 使用的面向对象的 C 写的 SIP 栈。

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

sed -i "s#antlr_java_prefixes=.*#antlr_java_prefixes=$RPM_SOURCE_DIR#" configure{,.ac}

autoreconf -ifv

%build
%configure --without-antlr --disable-tests --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/libbellesip.so.0*

%files devel
%{_includedir}/belle-sip
%{_libdir}/libbellesip.so
%{_libdir}/pkgconfig/belle-sip.pc

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-11
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-10
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-9
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-8
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-7
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-6
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-5
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-3
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 1.3.0-2
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
