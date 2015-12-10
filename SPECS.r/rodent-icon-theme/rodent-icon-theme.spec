Name:  rodent-icon-theme
Summary:    SVG scalable icon theme by Rodent
Summary(zh_CN.UTF-8): Rodent 提供的可缩放 SVG 图标
Version:    5.0
Release:    9%{?dist}

## This package replaces xfce4-icon-theme in Fedora >= 20
Provides: xfce4-icon-theme = %{version}-%{release}
Obsoletes: xfce4-icon-theme < 4.4.3-10

License:    GPLv2+
URL:        http://sourceforge.net/projects/xffm/files/%{name}/
Source0:    http://sourceforge.net/projects/xffm/files/%{name}/%{name}-%{version}.tar.gz
BuildArch:  noarch 

%description
Rodent-icon-theme (was xfce4-icon-theme) is a free-desktop 
compatible svg (scalable) icon theme which can work with 
most mayor Linux desktop environments.

%description -l zh_CN.UTF-8
Rodent 提供的可缩放 SVG 图标。

%prep
%setup -q

## Fix file-not-utf8 warning
iconv --from=ISO-8859-1 --to=UTF-8 AUTHORS > AUTHORS.new && \
touch -r AUTHORS AUTHORS.new && \
mv AUTHORS.new AUTHORS


%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%post
touch --no-create %{_datadir}/icons/Rodent &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/Rodent &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/Rodent &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/Rodent &>/dev/null || :

%files
%doc README AUTHORS
%license COPYING
%{_datadir}/icons/Rodent/
%ghost %{_datadir}/icons/Rodent/icon-theme.cache

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 5.0-9
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.0-8
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 5.0-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-5
- Use %%license tag

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 05 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0-3
- Added Provides/Obsoletes tags
- Changed %%install section to preserve timestamps
- Package now owns all %%{_datadir}/icons/Rodent/ directory
- Added %%ghost line to own the 'icon-theme.cache' file

* Sat Oct 12 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0-2
- Main directory renamed 'rodent' to avoid conflicts with 
  'xfce4-icon-theme' package
- %%description and %%setup improved

* Tue Oct 08 2013 Antonio Trande <sagitter@fedoraproject.org> 5.0-1
- First package

