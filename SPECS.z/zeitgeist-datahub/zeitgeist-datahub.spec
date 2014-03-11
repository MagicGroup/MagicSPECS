Summary:	The zeitgeist engine data logger
Name:		zeitgeist-datahub
Version:	0.9.5
Release:	2%{?dist}
Group:		User Interface/Desktops
License:	LGPLv3+
URL:		http://launchpad.net/zeitgeist-datahub
Source0:	http://launchpad.net/%{name}/0.9/0.9.5/+download/%{name}-%{version}.tar.gz
BuildRequires:	libzeitgeist-devel
BuildRequires:	glib2-devel gtk2-devel, vala-devel
BuildRequires:	json-glib-devel, telepathy-glib-devel
BuildRequires:	gettext, perl(XML::Parser), intltool, pkgconfig

%description
The datahub provides passive plugins which insert events into Zeitgeist.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh
%find_lang %{name} || touch %{name}.lang

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_bindir}/zeitgeist-datahub
%{_mandir}/man1/zeitgeist-datahub.*
%{_sysconfdir}/xdg/autostart/zeitgeist-datahub.desktop

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9.5-2
- 为 Magic 3.0 重建

* Sun Sep 23 2012 Deji Akingunola <dakingun@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.7.0-3
- Rebuild for new libpng

* Sat Apr 30 2011 Deji Akingunola <dakingun@gmail.com> - 0.7.0-2
- Package review fixes

* Sat Apr 30 2011 Deji Akingunola <dakingun@gmail.com> - 0.7.0-1
- Initial Fedora packaging
