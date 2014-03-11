Name:		liblognorm
Version:	0.3.4
Release:	4%{?dist}
Summary:	Fast samples-based log normalization library

License:	LGPLv2+
URL:		http://www.liblognorm.com
Source0:	http://www.liblognorm.com/files/download/%{name}-%{version}.tar.gz
Patch0:		liblognorm-0.3.4-rename-to-lognormalizer.patch
Patch1:		liblognorm-0.3.4-pc-file.patch

BuildRequires:	libestr-devel, libee-devel, chrpath

%description
Briefly described, liblognorm is a tool to normalize log data. 

People who need to take a look at logs often have a common problem. Logs from
different machines (from different vendors) usually have different formats for 
their logs. Even if it is the same type of log (e.g. from firewalls), the log 
entries are so different, that it is pretty hard to read these. This is where
liblognorm comes into the game. With this tool you can normalize all your logs.
All you need is liblognorm and its dependencies and a sample database that fits
the logs you want to normalize.

%package devel
Summary:	Development tools for programs using liblognorm library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libee-devel%{?_isa} libestr-devel%{?_isa}

%description devel
The liblognorm-devel package includes header files, libraries necessary for
developing programs which use liblognorm library.

%package utils
Summary:	Lognormalizer utility for normalizing log files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
The lognormalizer is the core of liblognorm, it is a utility for normalizing
log files.

%prep
%setup -q
%patch0 -p1 -b .rename-to-lognormalizer.patch
%patch1 -p1 -b .pc-file.patch

%build
%configure
V=1 make

%install
make install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
chrpath -d %{buildroot}/%{_bindir}/lognormalizer
chrpath -d %{buildroot}/%{_libdir}/liblognorm.so.0.0.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc

%files utils
%{_bindir}/lognormalizer


%changelog
* Fri Oct 05 2012 mdarade <mdarade@redhat.com> - 0.3.4-4
- Modified description of main & util package 

* Thu Sep 20 2012 Mahaveer Darade <mdarade@redhat.com> - 0.3.4-3
- Renamed normalizer binary to lognormalizer
- Updated pc file to exclude lee and lestr

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.3.4-2
- Updated BuildRequires to contain libestr-devel

* Wed Aug  1 2012 Milan Bartos <mbartos@redhat.com> - 0.3.4-1
- initial port
