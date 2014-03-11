# Review at https://bugzilla.redhat.com/show_bug.cgi?id=579171

Name:           lxpolkit
Version:        0.1.0
Release:        4%{?dist}
Summary:        Simple PolicyKit authentication agent

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://lxde.org/
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/lxpolkit
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  polkit-devel
BuildRequires:  desktop-file-utils
Requires:       polkit >= 0.95
# required to replace polkit-gnome and polkit-kde
Provides:       PolicyKit-authentication-agent

%description
LXPolKit is a simple PolicyKit authentication agent developed for LXDE, the 
Lightweight X11 Desktop Environment.


%prep
%setup -q
# Don't start in Xfce to avoid bugs like
# https://bugzilla.redhat.com/show_bug.cgi?id=616730
sed -i 's/^NotShowIn=GNOME;KDE;/NotShowIn=GNOME;KDE;XFCE;/g' data/lxpolkit.desktop.in.in


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
%find_lang %{name}
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}.desktop


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
# FIXME add ChangeLog and NEWS if not empty
%doc AUTHORS COPYING README
%config %{_sysconfdir}/xdg/autostart/lxpolkit.desktop
%{_libexecdir}/%{name}
%{_datadir}/%{name}/


%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1.0-2
- Rebuild for new libpng

* Sun Aug 28 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0
- Do not start lxpolkit in Xfce (#616730)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-0.2.20100402git5087383
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 02 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20100402git5087383
- Update to git version 5087383
- Install binary to %%{_libexecdir}

* Mon Mar 29 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-0.1.20100329git93555fa
- Initial package

