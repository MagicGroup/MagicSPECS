%global source_dir  %{_datadir}/%{name}-source
%global inst_srcdir %{buildroot}/%{source_dir}

Name:		libev
Summary:	High-performance event loop/event model with lots of features
Version:	4.11
Release:	2%{?dist}
Group:		System Environment/Libraries
License:	BSD or GPLv2+
URL:		http://software.schmorp.de/pkg/libev.html
Source0:	http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz
Source1:	%{name}.pc.in
BuildRequires:	automake libtool

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.


%package 	devel
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description 	devel
This package contains the development headers and libraries for libev.


%package	source
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
%if 0%{?fedora} >= 12 || 0%{?rhel} > 5
BuildArch:     noarch
%endif

%description	source
This package contains the source code for libev.


%prep
%setup -q

# Add pkgconfig support
cp -p %{SOURCE1} .
sed -i.pkgconfig -e 's|Makefile|Makefile libev.pc|' configure.ac configure
sed -i.pkgconfig -e 's|lib_LTLIBRARIES|pkgconfigdir = $(libdir)/pkgconfig\n\npkgconfig_DATA = libev.pc\n\nlib_LTLIBRARIES|' Makefile.am Makefile.in
aclocal
automake


%build
%configure --disable-static --with-pic --includedir=%{_includedir}/%{name}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

rm -rf %{buildroot}%{_libdir}/%{name}.la

# Make the source package
mkdir -p %{inst_srcdir}

find . -type f | grep -E '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' | xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
install -p -m 0644 Changes ev.pod LICENSE README %{inst_srcdir}

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc Changes LICENSE README
%{_libdir}/%{name}.so.4
%{_libdir}/%{name}.so.4.0.0

%files devel
%{_libdir}/%{name}.so
%{_includedir}/libev/
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man?/*

%files source
%{source_dir}


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.11-2
- 为 Magic 3.0 重建

* Fri Sep 28 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-1
- Update to 4.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 4.04-1
- move man page
- cleanup spec
- update to 4.04

* Mon Jun 13 2011 Matěj Cepl <mcepl@redhat.com> - 4.03-2
- EL5 cannot have noarch subpackages.

* Sat Feb  5 2011 Michal Nowak <mnowak@redhat.com> - 4.03-1
- 4.03; RHBZ#674022
- add a -source subpackage (Mathieu Bridon); RHBZ#672153

* Mon Jan 10 2011 Michal Nowak <mnowak@redhat.com> - 4.01-1
- 4.01
- fix grammar in %%description

* Sat Jan  2 2010 Michal Nowak <mnowak@redhat.com> - 3.90-1
- 3.9

* Fri Aug 10 2009 Michal Nowak <mnowak@redhat.com> - 3.80-1
- 3.8
- always use the most recent automake
- BuildRequires now libtool

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-2
- spec file change, which prevented uploading most recent tarball
  so the RPM was "3.70" but tarball was from 3.60

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-1
- v3.7
- list libev soname explicitly

* Mon Jun 29 2009 Michal Nowak <mnowak@redhat.com> - 3.60-1
- previous version was called "3.6" but this is broken update
  path wrt version "3.53" -- thus bumping to "3.60"

* Thu Apr 30 2009 Michal Nowak <mnowak@redhat.com> - 3.6-1
- 3.60
- fixed few mixed-use-of-spaces-and-tabs warnings in spec file

* Thu Mar 19 2009 Michal Nowak <mnowak@redhat.com> - 3.53-1
- 3.53

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Michal Nowak <mnowak@redhat.com> - 3.52-1
- 3.52

* Wed Dec 24 2008 Michal Nowak <mnowak@redhat.com> - 3.51-1
- 3.51

* Thu Nov 20 2008 Michal Nowak <mnowak@redhat.com> - 3.49-1
- version bump: 3.49

* Sun Nov  9 2008 Michal Nowak <mnowak@redhat.com> - 3.48-1
- version bump: 3.48

* Mon Oct  6 2008 kwizart <kwizart at gmail.com> - 3.44-1
- bump to 3.44

* Tue Sep  2 2008 kwizart <kwizart at gmail.com> - 3.43-4
- Fix pkgconfig support

* Mon Aug 12 2008 Michal Nowak <mnowak@redhat.com> - 3.43-2
- removed libev.a
- installing with "-p"
- event.h is removed intentionaly, because is there only for 
  backward compatibility with libevent

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 3.43-1
- initial package

