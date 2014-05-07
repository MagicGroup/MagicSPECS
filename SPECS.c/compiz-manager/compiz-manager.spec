Name:           compiz-manager
Version:        0.6.0
Release:        19%{?dist}
Summary:        A wrapper script to start compiz with proper options

Group:          Applications/System
License:        GPLv2+
URL:            http://www.compiz.org/
Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.gz
Source1:        compiz-manager.license
Source2:        README.fedora
Patch0:         compiz-manager_marco.patch
Patch1:         compiz-manager-0.6.0.diff
Patch2:         compiz-manager_add_mate-session_to_gtk-window-decorator.patch
BuildArch:      noarch

Requires:       compiz
Requires:       xorg-x11-utils
Requires:       pciutils
Requires:       glx-utils
Requires:       libcompizconfig


%description
This script will detect what options we need to pass to compiz to get it 
started, and start a default plugin and possibly window decorator.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cp -p %{SOURCE1} COPYING
cp -p %{SOURCE2} README.fedora

%build
#no build needed

%install
mkdir -p %{buildroot}/%{_bindir}/
cp -p compiz-manager %{buildroot}/%{_bindir}/


%files
%doc COPYING README.fedora
%{_bindir}/compiz-manager

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.6.0-18
- enable fglrx in script
- fix https://bugzilla.redhat.com/show_bug.cgi?id=922123

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.6.0-16
- build for fedora

* Tue Sep 20 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.6.0-15
- improve spec file

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.6.0-14
- build for mate

