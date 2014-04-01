Name:		fcitx-fbterm
Version:	0.2.0
Release:	3%{?dist}
Summary:	Fbterm Support for Fcitx
Group:		System Environment/Libraries
License:	GPLv2+
URL:		http://code.google.com/p/fcitx/
Source0:	http://fcitx.googlecode.com/files/%{name}-%{version}.tar.xz

BuildRequires:	cmake, fcitx-devel, gettext, intltool, libxml2-devel
BuildRequires:	dbus-glib-devel, pkgconfig
Requires:	fcitx

%description
Fcitx-fbterm is a Wrapper for Fcitx in fbterm, 
a fast Framebuffer based terminal emulator.


%prep
%setup -q -n %{name}-%{version}


%build
mkdir -pv build
pushd build
%cmake ..
make %{?_smp_mflags} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%doc AUTHORS README COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}-helper


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.2.0-1
- Upstream to fcitx-fbterm-0.2.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.1.4-1
- Upstream to fcitx-fbterm-0.1.4

* Sun Feb 26 2012 Liang Suilong <liangsuilong@gmail.com> - 0.1.2-1
- Initial Package
