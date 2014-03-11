Name:           lxde-icon-theme
Version:        0.4.2
Release:        5%{?dist}
Summary:        Default icon theme for LXDE

Group:          User Interface/Desktops
License:        LGPLv3
URL:            http://nuovext.pwsp.net/
Source0:        http://downloads.sourceforge.net/sourceforge/lxde/lxde-common-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       filesystem
BuildArch:      noarch
Provides:       nuoveXT2-icon-theme = 2.2

%description
nuoveXT2 is a very complete set of icons for several operating systems. It is 
also the default icon-theme of LXDE, the Lightweight X11 Desktop Environment.


%prep
%setup -qn lxde-common-%{version}

%build
%configure


%install
rm -rf $RPM_BUILD_ROOT
# we only install the icon theme
cd icon-theme
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
touch $RPM_BUILD_ROOT%{_datadir}/icons/nuoveXT2/icon-theme.cache


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/nuoveXT2 &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/nuoveXT2 &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/nuoveXT2 &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/nuoveXT2 &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc icon-theme/AUTHORS icon-theme/COPYING
%dir %{_datadir}/icons/nuoveXT2/
%{_datadir}/icons/nuoveXT2/*/*
%{_datadir}/icons/nuoveXT2/index.theme
%ghost %{_datadir}/icons/nuoveXT2/icon-theme.cache


%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-2
- Bump release for review

* Sat Jul 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2

* Sat Jun 13 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Mon Apr 14 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2.1-1
- Initial Fedora RPM
