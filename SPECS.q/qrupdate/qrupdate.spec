Name:		qrupdate
Version:	1.1.2
Release:	2%{?dist}
Summary:	A Fortran library for fast updates of QR and Cholesky decompositions
Group:		Development/Libraries
License:	GPLv3+
URL:		http://qrupdate.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc-gfortran

# These are needed for the test phase
BuildRequires:	blas-devel
BuildRequires:	lapack-devel

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions. 

%package devel
Summary:	Development libraries for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries for %{name}.

%prep
%setup -q
# Modify install location
sed -i 's|$(PREFIX)/lib/|$(DESTDIR)%{_libdir}/|g' src/Makefile

%build
make solib FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install-shlib LIBDIR=%{_libdir} PREFIX="%{buildroot}"
# Verify attributes
chmod 755 %{buildroot}%{_libdir}/libqrupdate.*

%clean
rm -rf %{buildroot}

%check
make test FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/libqrupdate.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqrupdate.so


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.2-2
- 为 Magic 3.0 重建

* Tue Feb 07 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 12 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1.

* Mon Jan 11 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.0-2
- Bump spec.

* Mon Jan 11 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0.1-1
- First release.
