Name:           ethumb
Version:        1.7.9
Release:        1%{?dist}
License:        LGPLv2+
Summary:        Thumbnail generation library for EFL
Url:            http://enlightenment.org/
Group:          Development/Libraries
Source:         http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen 
BuildRequires:  e_dbus-devel 
BuildRequires:  ecore-devel 
BuildRequires:  edje-devel 
BuildRequires:  emotion-devel 
BuildRequires:  evas-devel 
BuildRequires:  libeina-devel 
BuildRequires:  libexif-devel

%description
Ethumb is a thumbnail generation library.

%package devel
Summary:        Ethumb headers, documentation and test programs
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, test programs and documentation for Ethumb.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README COPYING
%{_libdir}/libethumb.so.1*
%{_libdir}/libethumb_client.so.1*
%{_bindir}/*
%{_libdir}/ethumb/
%{_datadir}/ethumb
%{_libexecdir}/ethumbd_slave
%{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so


%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Thu Sep 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-3
- Add doxygen to BRs
- Fix changelog ordering
- Make list of BRs look pretty by alphabetizing on seperate lines

* Thu Sep 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Fix isa macro in devel subpackage
- Add missing RPM changelog enry for update to 1.7.8

* Fri Aug 30 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8-2

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7
- Clean up spec

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec
