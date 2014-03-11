# $Id$
# Authority: dag

Summary: MSWord 6/7/8/9 binary file format to HTML converter
Name: wv2
Version: 0.4.2
Release: 1%{?dist}
License: GPLv2+
Group: Applications/File
URL: http://wvware.sourceforge.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/wvware/wv2-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: glib2-devel
BuildRequires: ImageMagick-devel
BuildRequires: libgsf-devel >= 1.13.0
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pkgconfig

Provides: wvware = %{version}-%{release}

%description
wv is a program that understands the Microsoft Word 6/7/8/9 binary file
format and is able to convert Word documents into HTML, which can then
be read with a browser.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

%build
%cmake -DWANT_DISTROBUILD=YES .
%{__make} %{?_smp_mflags} VERBOSE=1

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING* README RELEASE THANKS TODO
%{_libdir}/libwv2.so.*

%files devel
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING* README RELEASE THANKS TODO
%{_bindir}/wv2-config
%{_includedir}/wv2/
%{_libdir}/wvWare/
%{_libdir}/libwv2.so
%exclude %{_libdir}/libwv2.la

%changelog
* Mon Mar 17 2008 Dag Wieers <dag@wieers.com> - 0.4.2-1
- Initial package. (using DAR)
