Name:           geoclue2
Version:        2.1.2
Release:        2%{?dist}
Summary:        Geolocation service

License:        GPLv2+
URL:            http://www.freedesktop.org/wiki/Software/GeoClue/
Source0:        http://www.freedesktop.org/software/geoclue/releases/2.1/geoclue-%{version}.tar.xz

BuildRequires:  GeoIP-devel
BuildRequires:  glib2-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  json-glib-devel
BuildRequires:  libsoup-devel
BuildRequires:  ModemManager-glib-devel
BuildRequires:  NetworkManager-glib-devel
BuildRequires:  systemd
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:       dbus

%description
Geoclue is a D-Bus service that provides location information. The primary goal
of the Geoclue project is to make creating location-aware applications as
simple as possible, while the secondary goal is to ensure that no application
can access location information without explicit permission from user.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains files for developing applications that
use %{name}.


%package        server
Summary:        Server for IP address geolocation
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    server
The %{name}-server package contains the geoip-lookup and geoip-update binaries
for running on IP address geolocation servers.


%prep
%setup -q -n geoclue-%{version}


%build
%configure --with-dbus-service-user=geoclue
make %{?_smp_mflags} V=1


%install
%make_install

# Home directory for the 'geoclue' user
mkdir -p $RPM_BUILD_ROOT/var/lib/geoclue

# Remove demo files
rm $RPM_BUILD_ROOT%{_datadir}/applications/geoclue-demo-agent.desktop
rm $RPM_BUILD_ROOT%{_datadir}/applications/geoclue-where-am-i.desktop


%pre
# Update the home directory for existing users
getent passwd geoclue >/dev/null && \
    usermod -d /var/lib/geoclue geoclue &>/dev/null
# Create a new user and group if they don't exist
getent group geoclue >/dev/null || groupadd -r geoclue
getent passwd geoclue >/dev/null || \
    useradd -r -g geoclue -d /var/lib/geoclue -s /sbin/nologin \
    -c "User for geoclue" geoclue
exit 0

%post
%systemd_post geoclue.service

%preun
%systemd_preun geoclue.service

%postun
%systemd_postun_with_restart geoclue.service


%files
%doc COPYING NEWS
%{_sysconfdir}/geoclue.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%{_libexecdir}/geoclue
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_unitdir}/geoclue.service
%{_datadir}/geoclue-2.0/
%attr(755,geoclue,geoclue) %dir /var/lib/geoclue

%files devel
%{_libdir}/pkgconfig/geoclue-2.0.pc

%files server
%doc src/geoip-server/API-Documentation.txt
%{_bindir}/geoip-lookup
%{_bindir}/geoip-update


%changelog
* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.2-2
- Add systemd rpm scripts
- Don't install the demo .desktop files

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Sun Oct 06 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.0-1
- Update to 2.0.0
- Create a home directory for the 'geoclue' user

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.4-2
- Run the service as 'geoclue' user

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.4-1
- Update to 1.99.4

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.3-1
- Update to 1.99.3

* Sun Aug 25 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-3
- Update -devel subpackage description (#999153)

* Sat Aug 24 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-2
- Review fixes (#999153)
- Drop ldconfig calls that are unnecessary now that the shared library is gone
- Drop the build dep on gobject-introspection-devel
- Include API-Documentation.txt in the -server subpackage

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.2-1
- Update to 1.99.2
- The shared library is gone in this release and all users should use the
  dbus service directly

* Wed Aug 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-3
- Include geoip-lookup in the -server subpackage as well

* Wed Aug 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-2
- Ship geoip-update in -server subpackage

* Tue Aug 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.99.1-1
- Initial Fedora packaging
