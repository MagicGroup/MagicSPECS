%global commit d7bc683b6eaba225f483621485035a8044634376
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# valgrind is available only on selected arches
%ifnarch s390
%global with_valgrind 1
%endif

Name:       csnappy 
Version:    0
Release:    4.20150729git%{shortcommit}%{?dist}
Summary:    Snappy compression library ported to C 
Group:      System Environment/Libraries
License:    BSD
URL:        https://github.com/zeevt/%{name}
Source0:    %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  sed
# Tests:
%if 0%{?with_valgrind}
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  valgrind
%endif

%description
This is an ANSI C port of Google's Snappy library. Snappy is a compression
library designed for speed rather than compression ratios.

%package devel
Group:      Development/Libraries
Summary:    Development files for the %{name} library
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   glibc-headers%{?_isa}

%description devel
Header files for developing applications that use the %{name} library.


%prep
%setup -qn %{name}-%{commit}

# Extract BSD license and copyright notices, bug #1152057
! test -e LICENSE
for F in $(< Makefile sed -e '/libcsnappy.so:/ s/.*:// p' -e 'd'); do
    < $F sed -e '/Copyright/,/\*\//p' -e 'd'
done > LICENSE
test -s LICENSE

%build
make %{?_smp_mflags} 'OPT_FLAGS=%{optflags}' 'LDFLAGS=%{?__global_ldflags}' \
    lib%{name}.so cl_tester

%if 0%{?with_valgrind}
%check
make %{?_smp_mflags} 'OPT_FLAGS=%{optflags}' 'LDFLAGS=%{?__global_ldflags}' lib%{name}.so test
%endif

%install
make install 'DESTDIR=%{buildroot}' 'LIBDIR=%{_libdir}'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README TODO
%{_libdir}/lib%{name}.so

%files devel
%{_includedir}/%{name}.h


%changelog
* Thu Jul 30 2015 Petr Pisar <ppisar@redhat.com> - 0-4.20150729gitd7bc683
- Rebase to d7bc683b6eaba225f483621485035a8044634376

* Wed Jul 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0-3.20150331gitcf029fa
- Fix build on aarch64 (upstream issue https://github.com/zeevt/csnappy/issues/23 got note)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-2.20150331gitcf029fa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0-1.20150331gitcf029fa
- Rebase to 20150331
- Use same make flags for tests
- Use %%license

* Fri Jan 16 2015 Dan Horák <dan[at]danny.cz> - 0-1.20141010gitb43c183
- valgrind is available only on selected arches

* Mon Oct 13 2014 Petr Pisar <ppisar@redhat.com> - 0-0.20141010gitb43c183
- b43c183fdad31be0500a5f2ae022a54a66cb1a3d snapshot

