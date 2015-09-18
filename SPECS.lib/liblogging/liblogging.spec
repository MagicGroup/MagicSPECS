Name:    liblogging
Version: 1.0.4
Release: 5%{?dist}
Summary: An easy to use logging library
License: BSD
Group:   System Environment/Libraries
URL:     http://www.liblogging.org/
Source0: http://download.rsyslog.com/liblogging/liblogging-%{version}.tar.gz

%package stdlog
Summary: An easy to use logging library - stdlog component
Group:   System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: dos2unix

%package stdlog-devel
Summary: An easy to use logging library - stdlog development files
Group:   Development/Libraries
Requires: %{name}-stdlog%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.

%description stdlog
liblogging (the upstream project) is a collection of several components.
Namely: stdlog, journalemu, rfc3195.
The stdlog component of liblogging can be viewed as an enhanced version of the
syslog(3) API. It retains the easy semantics, but makes the API more
sophisticated "behind the scenes" with better support for multiple threads
and flexibility for different log destinations (e.g. syslog and systemd
journal).

%description stdlog-devel
This package contains development files for the %{name}-stdlog package.

%prep
%setup -q

%build
%configure \
  --disable-journal \
  --disable-rfc3195 \
  --disable-static \
  --enable-stdlog \

make V=1 %{?_smp_mflags}
dos2unix COPYING

%install
make DESTDIR=%{buildroot} install
# not packing stdlogctl yet
rm -f \
  %{buildroot}%{_bindir}/stdlogctl \
  %{buildroot}%{_libdir}/liblogging-stdlog.la \
  %{buildroot}%{_mandir}/man1/stdlogctl.1 \

%post stdlog -p /sbin/ldconfig

%postun stdlog -p /sbin/ldconfig

%files stdlog
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ChangeLog
%{_libdir}/liblogging-stdlog.so.*

%files stdlog-devel
%defattr(-,root,root,-)
%{_includedir}/liblogging
%{_libdir}/liblogging-stdlog.so
%{_libdir}/pkgconfig/liblogging-stdlog.pc
%{_mandir}/man3/stdlog.3.gz

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.0.4-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Tomas Heinrich <theinric@redhat.com> 1.0.4-1
- initial import
