%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Last updated for 1.8.8
%define cairo_version 1.8.6

### Abstract ###

Name: pycairo
Version: 1.8.8
Release: 4%{?dist}
License: MPLv1.1 or LGPLv2
Group: Development/Languages
Summary: Python bindings for the cairo library
URL: http://cairographics.org/pycairo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source: http://cairographics.org/releases/pycairo-%{version}.tar.gz

### Build Dependencies ###

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig
BuildRequires: python-devel

%description
Python bindings for the cairo library.

%package devel
Summary: Libraries and headers for pycairo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: cairo-devel
Requires: pkgconfig
Requires: python-devel

%description devel
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with pycairo.

%prep
%setup -q -n pycairo-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* INSTALL NEWS README
%doc examples doc/faq.rst doc/overview.rst doc/README
%{python_sitearch}/cairo/

%files devel
%defattr(-,root,root,-)
%{_includedir}/pycairo/
%{_libdir}/pkgconfig/pycairo.pc

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.8.8-4
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 1.8.8-3
- 为 Magic 3.0 重建

