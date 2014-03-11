Name:           systemd-ui
Url:            http://www.freedesktop.org/wiki/Software/systemd
Version:        1
Release:        3%{?dist}
License:        GPLv2+
Group:          Applications/System
Summary:        Graphical front-end for systemd
Source0:        http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
BuildRequires:  vala >= 0.11
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  glib2-devel
BuildRequires:  libgee06-devel
BuildRequires:  libnotify-devel >= 0.7
BuildRequires:  desktop-file-utils
Requires:       desktop-notification-daemon
Obsoletes:      systemd-gtk < 45

%description
Graphical front-end for systemd. It provides a simple user interface to manage
services, and a graphical agent to request passwords from the user.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

desktop-file-install --delete-original  \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/systemadm.desktop

magic_rpm_clean.sh

%files
%{_bindir}/systemadm
%{_bindir}/systemd-gnome-ask-password-agent
%{_datadir}/applications/systemadm.desktop
%{_mandir}/man1/systemadm.*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1-3
- 为 Magic 3.0 重建

* Tue Mar 20 2012 Michal Schmidt <mschmidt@redhat.com> - 1-2
- Providing systemd-gtk is not necessary, because no package Requires it.
- Bump the Obsoletes to cover F17 builds of systemd-gtk. If we rebase F17 to v45
  and keep systemd-gtk, we'll need to bump yet more.

* Sun Mar 18 2012 Kay Sievers <kay@redhat.com> - 1-1
- initial release after split-off from systemd package
