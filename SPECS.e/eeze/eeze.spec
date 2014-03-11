Name:           eeze
Version:        1.7.9
Release:        1%{?dist}
License:        BSD and GPLv2+
Summary:        Device abstraction library
Url:            http://enlightenment.org
Group:          System Environment/Libraries
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
BuildRequires:  ecore-devel 
BuildRequires:  libeina-devel 
BuildRequires:  systemd-devel

%description
Eeze is a library for manipulating devices through udev with a simple and fast
api. It interfaces directly with libudev, avoiding such middleman daemons as 
udisks/upower or hal, to immediately gather device information the instant it 
becomes known to the system.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
Headers, test programs and documentation for eeze

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install utildir=%{buildroot}%{_libdir}/enlightenment/utils

find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README COPYING NEWS AUTHORS
%{_libdir}/libeeze.so.1*

%files devel
%{_includedir}/eeze-1
%{_libdir}/pkgconfig/eeze.pc
%{_libdir}/libeeze.so

%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Mon Aug 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Update license to GPLv2 and BSD

* Mon Aug 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7
- Clean up spec file

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec
