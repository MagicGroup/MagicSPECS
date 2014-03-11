%define beta 3

Name:       qca-gnupg
Version:    2.0.0
Release:    0.8.beta%{beta}%{?dist}

Summary:    GnuPG plugin for the Qt Cryptographic Architecture v2
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        http://delta.affinix.com/qca/
Source0:    http://delta.affinix.com/download/qca/2.0/plugins/qca-gnupg-%{version}-beta%{beta}.tar.bz2
Patch0:     qca-gnupg-keyringmonitoring.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: qt4-devel, qca2-devel >= 2.0.0-1
# FIXME/TODO: can we make gnupg2 work here?  -- Rex
Requires:   gnupg

Provides:   qca2-gnupg = %{version}-%{release}


%description
This is a plugin to provide GnuPG capability to programs that use the Qt
Cryptographic Architecture (QCA).  QCA is a library providing an easy API
for several cryptographic algorithms to Qt programs.  This package only
contains the GnuPG plugin.

%prep
%setup -q -n %{name}-%{version}-beta%{beta}
%patch0 -p0 -b .keyringmonitoring


%build
unset QTDIR
./configure \
  --no-separate-debug-info \
  --verbose
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

export INSTALL_ROOT=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_qt4_plugindir}/crypto
make install


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_qt4_plugindir}/crypto/


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.0-0.8.beta3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.0.0-0.7.beta3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.6.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 29 2010 <rdieter@fedoraproject.org> - 2.0.0-0.5.beta3
- Provides: qca2-gnupg (#512000)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.4.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 5 2009 Sven Lankes <sven@lank.es> - 2.0.0-0.3.beta3
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.0-0.2.beta1
- Autorebuild for GCC 4.3

* Tue Nov 06 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.1.beta1
- initial package
