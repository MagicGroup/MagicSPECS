Name:           belle-sip
Version:        1.3.0
Release:        1%{?dist}
Summary:        Linphone SIP stack
License:        GPLv2+
URL:            http://www.linphone.org/
Source0:        http://download.savannah.gnu.org/releases/linphone/belle-sip/%{name}-%{version}.tar.gz

BuildRequires:  antlr3-C-devel
BuildRequires:  antlr3-tool
BuildRequires:  polarssl-devel
BuildRequires:  CUnit-devel
BuildRequires:  libtool

%description
Belle-sip is an object oriented C written SIP stack used by Linphone.

%package devel
Summary:       Development libraries for belle-sip
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description    devel
Libraries and headers required to develop software with belle-sip.

%prep
%setup -q

autoreconf -ifv

%build
#这是一个临时性的措施，后续需要修改。
%configure --with-antlr=/usr/share/local/java --disable-tests --disable-silent-rules
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
%{_libdir}/libbellesip.a
%{_libdir}/pkgconfig/belle-sip.pc

%changelog
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
