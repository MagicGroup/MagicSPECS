Summary:       FreeBoB firewire audio driver library
Name:          libfreebob
Version:       1.0.11
Release:       10%{?dist}
License:       GPLv2+
Group:         System Environment/Libraries
Source0:       http://surfnet.dl.sourceforge.net/sourceforge/freebob/libfreebob-%{version}.tar.gz
Patch1:	       libfreebob-1.0.11-includes.patch
Patch2:        libfreebob-gcc46.patch
Patch3:		libfreebob-1.0.11-gcc4.patch
URL:           http://freebob.sourceforge.net
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libavc1394-devel >= 0.5.3, libiec61883-devel, libraw1394-devel
BuildRequires: alsa-lib-devel libxml2-devel autoconf
ExcludeArch:   s390 s390x

%description
libfreebob implements a userland driver for BeBoB-based fireware audio
devices.

%package devel
Summary: Libraries, includes etc to develop with libfreebob
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Libraries, includes etc to develop with libfreebob.

%prep
%setup -q
%patch1 -p1
%patch2 -p1 
%patch3 -p1

# Tweak libiec61883 build requirements.
perl -pi -e 's/1.1.0/1.0.0/' configure

%build
%configure --disable-static
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libfreebob.pc
%{_includedir}/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.11-10
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 1.0.11-9
- 为 Magic 3.0 重建

