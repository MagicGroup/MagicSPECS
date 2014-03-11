%define git 1
%define gitdate 20120709

Name:		libcec
Version:	1.5
Release:	0.git%{gitdate}.1%{?dist}.1
Summary:	Pulse-Eight CEC adapter control library
License:	GPLv2+
Group:		System/Libraries
URL:		http://libcec.pulse-eight.com/
Source0:	%{name}-%{gitdate}.tar.xz
Source1:	make_libcec_git_package.sh
BuildRequires:	pkgconfig(libudev)

%description
With libcec you can access your Pulse-Eight CEC adapter.

%package -n cec-utils
Summary:	Utilities for Pulse-Eight CEC adapter control
Group:		System/Configuration/Hardware
# the binaries require the library, but automatic dependency generation doesn't
# catch that
Requires:	%{name} = %{version}

%description -n cec-utils
With libcec you can access your Pulse-Eight CEC adapter.

This package contains the command-line tools to configure and test your
Pulse-Eight CEC adapter.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}
Provides:	cec-devel = %{version}

%description devel
With libcec you can access your Pulse-Eight CEC adapter.

This package contains the files for developing applications which
will use libcec.

%prep
%setup -q -n %{name}-%{gitdate}

%build
autoreconf -ifv
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
rm %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files -n cec-utils
%defattr(-,root,root)
%{_bindir}/cec-client
%{_bindir}/cec-config

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.5-0.git20120709.1.1
- 为 Magic 3.0 重建

