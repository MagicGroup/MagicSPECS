%global major_version 0.30
%global minor_version 4

Name:       java-atk-wrapper
Version:    %{major_version}.%{minor_version}
Release:    4%{?dist}
Summary:    Java ATK Wrapper

Group:      Development/Libraries
License:    LGPLv2+
URL:        http://git.gnome.org/browse/java-atk-wrapper
Source0:    http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{major_version}/%{name}-%{version}.tar.bz2
# this is a fedora-specific file
# needed to explain how to use java-atk-wrapper with different java runtimes
Source1:    README.fedora

BuildRequires:  java-devel

BuildRequires:  atk-devel
BuildRequires:  GConf2-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk2-devel
BuildRequires:  xorg-x11-utils

Requires:   java
Requires:   xorg-x11-utils

%description
Java ATK Wrapper is a implementation of ATK by using JNI technic. It
converts Java Swing events into ATK events, and send these events to
ATK-Bridge.

JAW is part of the Bonobo deprecation project. It will replaces the
former java-access-bridge.
By talking to ATK-Bridge, it keeps itself from being affected by the
change of underlying communication mechanism.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}
cp %{SOURCE1} .

%install
# java-atk-wrapper's make install is broken by design
# it installs to the current JDK_HOME. We want to install it to a central
# location and then allow all/any JRE's/JDK's to use it.
# make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_libdir}/%{name}

mv wrapper/java-atk-wrapper.jar %{buildroot}%{_libdir}/%{name}/
mv jni/src/.libs/libatk-wrapper.so.0.0.18 %{buildroot}%{_libdir}/%{name}/
ln -s %{_libdir}/%{name}/libatk-wrapper.so.0.0.18 \
    %{buildroot}%{_libdir}/%{name}/libatk-wrapper.so.0


%files
%doc AUTHORS
%doc COPYING.LESSER
%doc NEWS
%doc README
%doc README.fedora
%{_libdir}/%{name}/


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 - Omair Majid <omajid@redhat.com> - 0.30.4-1
- Added missing requires/buildrequires on xorg-x11-utils
- Added README.fedora

* Wed May 09 2012 - Omair Majid <omajid@redhat.com> - 0.30.4-1
- Initial packaging
