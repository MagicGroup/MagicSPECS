Name:           libquvi
Version:        0.4.1 
Release:        3%{?dist}
Summary:        A cross-platform library for parsing flash media stream

Group:          Applications/Internet
License:        LGPLv2+
URL:            http://quvi.sourceforge.net/
Source0:        http://downloads.sourceforge.net/quvi/%{name}-%{version}.tar.gz

BuildRequires:  libquvi-scripts libcurl-devel lua-devel
Requires:       libquvi-scripts

%description
Libquvi is a cross-platform library for parsing flash media stream
URLs with C API.

%package devel
Summary: Files needed for building applications with libquvi
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: quvi-devel <= 0.2.19
Provides:  quvi-devel = %{version}-%{release}

%description devel
Files needed for building applications with libquvi


%prep
%setup -q

%build
%configure --enable-static=no

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{name}.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc ChangeLog COPYING README 
%{_libdir}/%{name}.so.*
%{_mandir}/man3/%{name}.3.*

%files devel
%doc examples/simple.c 
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/quvi/

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.1-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.1-1
- Update to 0.4.1

* Sun Dec 11 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-5
- Fix Obsoletes version

* Wed Oct 19 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-4
- Remove the pkgconfig require for the devel package

* Tue Oct 11 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-3
- Fix BuilRequires

* Sun Oct  9 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-2
- Fix requires

* Sat Oct  8 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-1
- Initial build
