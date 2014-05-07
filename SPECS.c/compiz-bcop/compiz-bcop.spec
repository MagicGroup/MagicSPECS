Name: compiz-bcop
Version: 0.8.8
Release: 7%{?dist}
Epoch: 1
Summary: Compiz option code generator       

Group: Development/Libraries
License: GPLv2+       
URL: http://www.compiz.org           
Source0:   http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2     

# compiz is not available on these arches due to missing libdrm
ExcludeArch: s390 s390x
BuildArch: noarch

BuildRequires: libxslt-devel
Requires: pkgconfig 
Requires: util-linux

%description
BCOP is a code generator that provides an easy way to handle
plugin options by generating parts of the plugin code directly
from the xml metadata file.
It is used for most of the Compiz Fusion plugins


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc COPYING NEWS AUTHORS
%{_bindir}/bcop
%{_datadir}/bcop/
%{_datadir}/pkgconfig/bcop.pc


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-5
- bump version

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-4
- add Epoch tag

* Wed Sep 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-3
- initial build for fedora
- fix url and source0

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- build for mate

