Name:           hiredis
Version:        0.11.0
Release:        2%{?dist}
Summary:        A minimalistic C client library for Redis
Summary(zh_CN.UTF-8): Redis 的简约 C 客户端库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            https://github.com/antirez/hiredis
Source0:        antirez-%{name}-v%{version}-0-g0fff0f1.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description 
Hiredis is a minimalistic C client library for the Redis database.

%description -l zh_CN.UTF-8
Redis 数据库的简约 C 客户端库。

%package devel
Summary:        Header files and libraries for hiredis C development
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files and 
libraries to develop applications using a Redis database.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n antirez-%{name}-0fff0f1

%build
make %{?_smp_mflags} OPTIMIZATION="%{optflags}"

%install
rm -rf %{buildroot}

make install PREFIX=%{buildroot}/%{_prefix} INSTALL_LIBRARY_PATH=%{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_bindir}
cp hiredis-example %{buildroot}%{_bindir}
cp hiredis-test    %{buildroot}%{_bindir}

rm -f `find %{buildroot} -name *.a`
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/hiredis-example
%{_bindir}/hiredis-test
%{_libdir}/libhiredis.so.0.10
%{_libdir}/libhiredis.so.0

%files devel
%defattr(-,root,root,-)
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/libhiredis.so

%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 0.11.0-2
- 为 Magic 3.0 重建

* Sat Sep 29 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.11.0-1
- Updated to 0.11.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 20 2012 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.10.1-3
- Removed Requires redis.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.10.1-1
- Updated to upstream 0.10.1-28-gd5d8843.

* Mon May 16 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.10.0-3
- Removed INSTALL_LIB from install target as we use INSTALL_LIBRARY_PATH.
- Use 'client library' in Summary.

* Wed May 11 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.10.0-2
- Updated devel sub-package description.
- Added optimization flags.
- Remove manual installation of shared objects.
- Use upstream .tar.gz sources.

* Tue May 10 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.10.0-1.gitdf203bc328
- Updated to upstream gitdf203bc328.
- Added TODO to the files.
- Updated to use libhiredis.so.0, libhiredis.so.0.10.

* Tue Apr 29 2011 Shakthi Kannan <shakthimaan [AT] fedoraproject dot org> 0.9.2-1
- First release.
