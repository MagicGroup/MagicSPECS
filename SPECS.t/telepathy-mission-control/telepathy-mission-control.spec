%define tp_glib_ver 0.17.5

Name:           telepathy-mission-control
Version:	5.16.3
Release:	2%{?dist}
Epoch:          1
Summary:        Central control for Telepathy connection manager
Summary(zh_CN.UTF-8): Telepathy 连接管理器的中央控制

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2
URL:            http://telepathy.freedesktop.org/wiki/Mission_Control
Source0:        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

## upstream patches
# fix failing avatar test, https://bugs.freedesktop.org/show_bug.cgi?id=71001
Patch0049: 0049-account-manager-avatar.py-fix-race-condition-by-comb.patch

BuildRequires:  chrpath
BuildRequires:  dbus-python
BuildRequires:  glib2-devel
BuildRequires:  libxslt-devel
BuildRequires:  NetworkManager-glib-devel
BuildRequires:  pygobject2
BuildRequires:  python-twisted-core
BuildRequires:  telepathy-glib-devel >= %{tp_glib_ver}
BuildRequires:  gtk-doc


%description
Mission Control, or MC, is a Telepathy component providing a way for
"end-user" applications to abstract some of the details of connection
managers, to provide a simple way to manipulate a bunch of connection
managers at once, and to remove the need to have in each program the
account definitions and credentials.

%description -l zh_CN.UTF-8d
Telepathy 连接管理器的中央控制。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       dbus-devel
Requires:       dbus-glib-devel
Requires:       telepathy-glib-devel >= %{tp_glib_ver}


%description    devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。
%prep
%setup -q
%patch0049 -p1 -b .0049


%build
%configure --disable-static --enable-gtk-doc --enable-mcd-plugins --with-connectivity=nm --disable-upower

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Remove lib64 rpaths
chrpath --delete %{buildroot}%{_libexecdir}/mission-control-5

# Remove .la files
find %{buildroot} -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%check
make check


%post -p /sbin/ldconfig


%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS NEWS COPYING
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/im.telepathy.MissionControl.FromEmpathy.gschema.xml
%{_libdir}/libmission-control-plugins.so.*
%{_libexecdir}/mission-control-5
%{_mandir}/man*/*.gz


%files devel
%doc %{_datadir}/gtk-doc/html/mission-control-plugins
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmission-control-plugins.so


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1:5.16.3-2
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 1:5.16.3-1
- 更新到 5.16.3

* Mon Jan 27 2014 Brian Pepple <bpepple@fedoraproject.org> - 1:5.16.1-1
- Update to 5.16.1.

* Wed Oct 30 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:5.16.0-2
- --disable-upower

* Thu Oct  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:5.16.0-1
- Update to 5.16.0.

* Thu Sep 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.15.1-1
- Update to 5.15.1

* Thu Sep 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.15.0-4
- Enable the Python tests

* Thu Sep 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.15.0-3
- Add %%check to run the upstream test suite on each build

* Mon Aug 26 2013 Kalev Lember <kalevlember@gmail.com> - 1:5.15.0-2
- Fix the build

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:5.15.0-1
- Update to 5.15.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Debarshi Ray <rishi@fedoraproject.org> - 1:5.14.1-3
- Remove rpath and omit some unused direct shared library dependencies.

* Thu Jun 20 2013 Matthias Clasen <mclasen@redhat.com> - 1:5.14.1-2
- Install NEWS instead of ChangeLog

* Fri May  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:5.14.1-1
- Update to 5.14.1.
- Drop defattr. No longer needed.
- Drop ignore gnome keyring patch. Fixed upstream.

* Thu Jan 24 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:5.14.0-2
- Add patch for upstream b.fd.o # 59468

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.14.0-1
- Update to 5.14.0

* Thu Sep 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.2-1
- Update to 5.13.2.

* Thu Sep  6 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.1-1
- Update to 5.13.1.

* Mon Jul 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.13.0-1
- Update to 5.13.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.12.1-1
- Update to 5.12.1.

* Mon Apr  2 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.12.0-1
- Update to 5.12.0.

* Wed Feb 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:5.11.0-1
- Update to 5.11.0
- Bump minimum version of tp-glib.
