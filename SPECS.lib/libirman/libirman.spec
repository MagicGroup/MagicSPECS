Name:           libirman
Version:        0.4.5
Release:        7%{?dist}
Summary:        Library for IRMAN hardware

Group:          System Environment/Libraries
#The files which make up the library are covered under the GNU Library
#General Public License, which is in the file COPYING.lib.
#The files which make up the test programs and the documentation are covered
#under the GNU General Public License, which is in the file COPYING.
License:        GPLv2+ and LGPLv2+
URL:            http://lirc.sourceforge.net/software/snapshots/
Source0:        http://downloads.sourceforge.net/lirc/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf, automake, libtool

%description
A library for accessing the IRMAN hardware from Linux and other Unix systems.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
libtoolize --force --copy
autoreconf
%configure --disable-static --disable-rpath \
  --prefix=%{_prefix} \
  --mandir=%{_mandir} \
  --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING* README TODO NEWS
%config(noreplace) %{_sysconfdir}/irman.conf
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc TECHNICAL
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.5-7
- 为 Magic 3.0 重建

* Sat Jan 07 2012 Liu Di <liudidi@gmail.com> - 0.4.5-6
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.5-3
- added libtoolize to fix build for f11

* Sat Apr 18 2009 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.5-2
- added autoreconf and --disable-rpath

* Fri Apr 10 2009 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.5-1
- new upstream
- updated Source0 to sourceforge
- removed autoconf things

* Thu Apr 02 2009 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.4-5.20090314cvs
- removed cvs patch, added instructions to create cvs snapshot tar package,
  which is now defined as Source0

* Sat Mar 14 2009 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.4-4.20090314cvs
- applied cvs patch, which fixed dynamic library build and IRMAN restart
- added BuildRequires: autoconf, automake, libtool

* Sat Dec  6 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.4.4-3
- initial release
