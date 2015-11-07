%global  basever 0.8.8

Name:           emerald-themes
URL:            http://www.compiz.org
License:        GPLv2
Group:          User Interface/Desktops
Version:        0.5.2
Release:        12%{?dist}
Epoch:          1 
Summary:        Themes for Emerald, a window decorator for Compiz Fusion
Source0:        http://cgit.compiz.org/fusion/decorators/emerald-themes/snapshot/%{name}-%{version}.tar.bz2

BuildArch:      noarch

Requires:       compiz >= %{basever}
Requires:       emerald >= %{basever}
BuildRequires:  libtool


%description
Emerald is themeable window decorator and compositing 
manager for Compiz Fusion.

This package contains themes for emerald.


%prep
%setup -q
autoreconf -v --install

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.bak" | xargs rm -f


%files
%doc ChangeLog COPYING README
%{_datadir}/emerald/themes/


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1:0.5.2-12
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.5.2-11
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> -  1:0.5.2-8
- own directory
- use new upstream package for rpm
- generate configure
- drop unnecessary command to remove import.sh
- remove files with 'bak' instead of '~'
- drop unnecessary 'chmod' command

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> -  1:0.5.2-7
- build for fedora
- review package
- remove %%defattr(-,root,root,-)
- remove BuildRoot
- add basever
- add Epoch tag

