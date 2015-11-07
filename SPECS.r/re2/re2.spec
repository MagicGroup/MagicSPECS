Name:           re2
Version:        20131024
Release:        7%{?dist}
Summary:        C++ fast alternative to backtracking RE engines
Group:          System Environment/Libraries
License:        BSD
URL:            http://code.google.com/p/%{name}/
Source0:        http://re2.googlecode.com/files/%{name}-%{version}.tgz
Patch0:		re2-symbols-fix.patch

%description
RE2 is a C++ library providing a fast, safe, thread-friendly alternative to
backtracking regular expression engines like those used in PCRE, Perl, and
Python.

Backtracking engines are typically full of features and convenient syntactic
sugar but can be forced into taking exponential amounts of time on even small
inputs.

In contrast, RE2 uses automata theory to guarantee that regular expression
searches run in time linear in the size of the input, at the expense of some
missing features (e.g back references and generalized assertions).

%package        devel
Summary:        C++ header files and library symbolic links for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the C++ header files and symbolic links to the shared
libraries for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .fix

%build
# The -pthread flag issue has been submitted upstream:
# http://groups.google.com/forum/?fromgroups=#!topic/re2-dev/bkUDtO5l6Lo
# The RPM macro for the linker flags does not exist on EPEL
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
CXXFLAGS="${CXXFLAGS:-%optflags} -pthread"
LDFLAGS="${LDFLAGS:-%__global_ldflags} -pthread"
make %{?_smp_mflags} CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" includedir=%{_includedir} libdir=%{_libdir}

%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT includedir=%{_includedir} libdir=%{_libdir}

# Suppress the static library
find $RPM_BUILD_ROOT -name 'lib%{name}.a' -exec rm -f {} \;

%check
make %{?_smp_mflags} shared-test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS CONTRIBUTORS LICENSE README
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 20131024-7
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 20131024-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Petr Pisar <ppisar@redhat.com> - 20131024-4
- Rebuild owing to C++ ABI change in GCC-5 (bug #1195351)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Tom Callaway <spot@fedoraproject.org> - 20131024-1
- update to 20131024
- fix symbols export to stop test from failing

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130115-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb 17 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-2
- Took into account the feedback from review request (#868578).

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-1
- The download source comes now directly from the project.

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-2
- Took into account review request (#868578) feedback.

* Sat Oct 20 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-1
- RPM release for Fedora 18

