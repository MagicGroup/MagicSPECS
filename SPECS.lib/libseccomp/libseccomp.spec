Summary: Enhanced seccomp library
Summary(zh_CN.UTF-8): 增强的 seccomp 库
Name: libseccomp
Version: 2.1.1
Release: 5%{?dist}
ExclusiveArch: %{ix86} x86_64 %{arm}
License: LGPLv2
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: http://downloads.sf.net/project/libseccomp/%{name}-%{version}.tar.gz
URL: http://libseccomp.sourceforge.net
BuildRequires: valgrind

%description
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%description -l zh_CN.UTF-8
增强的 seccomp 库。

%package devel
Summary: Development files used to build applications with libseccomp support
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release} pkgconfig

%description devel
The libseccomp library provides an easy to use interface to the Linux Kernel's
syscall filtering mechanism, seccomp.  The libseccomp API allows an application
to specify which syscalls, and optionally which syscall arguments, the
application is allowed to execute, all of which are enforced by the Linux
Kernel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
./configure --prefix="%{_prefix}" --libdir="%{_libdir}"
CFLAGS="%{optflags}" make V=1 %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}/%{_libdir}"
mkdir -p "%{buildroot}/%{_includedir}"
mkdir -p "%{buildroot}/%{_mandir}"
make V=1 DESTDIR="%{buildroot}" install
magic_rpm_clean.sh

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc CREDITS
%doc README
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.1.1-5
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 2.1.1-4
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.1.1-3
- 为 Magic 3.0 重建

* Thu Feb 27 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-2
- Build with CFLAGS="${optflags}"
* Mon Feb 17 2014 Paul Moore <pmoore@redhat.com> - 2.1.1-1
- Removed the kernel dependency (RHBZ #1065572)
* Thu Oct 31 2013 Paul Moore <pmoore@redhat.com> - 2.1.1-0
- New upstream version
- Added a %check procedure for self-test during build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Paul Moore <pmoore@redhat.com> - 2.1.0-0
- New upstream version
- Added support for the ARM architecture
- Added the scmp_sys_resolver tool
* Mon Jan 28 2013 Paul Moore <pmoore@redhat.com> - 2.0.0-0
- New upstream version
* Tue Nov 13 2012 Paul Moore <pmoore@redhat.com> - 1.0.1-0
- New upstream version with several important fixes
* Tue Jul 31 2012 Paul Moore <pmoore@redhat.com> - 1.0.0-0
- New upstream version
- Remove verbose build patch as it is no longer needed
- Enable _smp_mflags during build stage
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Jul 10 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-1
- Limit package to x86/x86_64 platforms (RHBZ #837888)
* Tue Jun 12 2012 Paul Moore <pmoore@redhat.com> - 0.1.0-0
- Initial version

