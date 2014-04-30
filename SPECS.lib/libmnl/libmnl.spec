Name:           libmnl
Version:        1.0.3
Release:        7%{?dist}
Summary:        A minimalistic Netlink library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://netfilter.org/projects/libmnl
Source0:        http://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2

%description
libmnl is a minimalistic user-space library oriented to Netlink developers.
There are a lot of common tasks in parsing, validating, constructing of both
the Netlink header and TLVs that are repetitive and easy to get wrong.
This library aims to provide simple helpers that allows you to re-use code and
to avoid re-inventing the wheel.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}

%package 	static
Summary: 	Static development files for %{name}
Group:          Development/Libraries
Requires: %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description 	static
The %{name}-static package contains static libraries for devleoping applications that use %{name}.


%prep
%setup -q


%build
%configure --enable-static
make CFLAGS="%{optflags}" %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find examples '(' -name 'Makefile.am' -o -name 'Makefile.in' ')' -exec rm -f {} ';'
find examples -type d -name '.deps' -prune -exec rm -rf {} ';'
mv examples examples-%{_arch}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%doc COPYING
%doc examples-%{_arch}
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%changelog
* Fri Apr 18 2014 Liu Di <liudidi@gmail.com> - 1.0.3-7
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 12 2012 Hushan Jia <hushan.jia@gmail.com> - 1.0.3-4
- use %doc for each arch to avoid multilib conflict (rhbz 831413)

* Sat Aug 04 2012 Philip Prindeville <philipp@fedoraproject.org> - 1.0.3-3
- Add .a to devel package (rhbz 845793)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Hushan Jia <hushan.jia@gmail.com> 1.0.3-1
- Update to 1.0.3.

* Sat Feb 04 2012 Hushan Jia <hushan.jia@gmail.com> 1.0.2-1
- Update to 1.0.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-4
- fix require of devel package
- add example source files to docs

* Wed Aug 24 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-3
- remove unnecessary buildroot and defattr tags
- remove unnecessary build requires

* Sat Aug 20 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-2
- use upstream released source tarball

* Sat Aug 20 2011 Hushan Jia <hushan.jia@gmail.com> 1.0.1-1
- initial packaging

