Summary:        Standards handling for freedesktop.org standards
Name:           efreet
Version:        1.7.9
Release:        1%{?dist}
Group:          System Environment/Libraries
License:        BSD and GPLv2+
URL:            http://enlightenment.org
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  ecore-devel
BuildRequires:  eet-devel
BuildRequires:  libeina-devel
BuildRequires:  evas-devel
BuildRequires:  libeina

%description
An implementation of several specifications from freedesktop.org intended for
use in Enlightenment DR17 (e17) and other applications using the Enlightenment
Foundation Libraries (EFL). Currently, the following specifications are
included:
  * Base Directory
  * Desktop Entry
  * Icon Theme
  * Menu
  * Trash
  * Mime

%package        devel
Summary:        Efreet headers, documentation and test programs
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Libraries and header files for efreet

%prep
%setup -q

%build
%configure --disable-static --disable-doc -disable-rpath
make %{?_smp_mflags} V=1

%install
%make_install

find %{buildroot} -name '*.la' -delete

#Remove tests
rm %{buildroot}%{_bindir}/%{name}_*
rm -r %{buildroot}%{_datadir}/%{name}

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libdir}/lib*.so.*
%{_libdir}/%{name}

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Tue Aug 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Add evas

* Tue Aug 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8
- Update space as per package review

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7
- Clean up spec

* Sun Dec 30 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- initial spec
