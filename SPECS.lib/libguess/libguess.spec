Name: libguess
Version: 1.1
Release: 5%{?dist}

Summary: High-speed character set detection library
Summary(zh_CN.UTF-8): 高速的字符集检测库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: BSD
URL: http://www.atheme.org/project/libguess
Source0: http://distfiles.atheme.org/libguess-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: libmowgli-devel >= 0.9.50

%description
libguess employs discrete-finite automata to deduce the character set of
the input buffer. The advantage of this is that all character sets can be
checked in parallel, and quickly. Right now, libguess passes a byte to
each DFA on the same pass, meaning that the winning character set can be
deduced as efficiently as possible.

libguess is fully reentrant, using only local stack memory for DFA
operations.

%description -l zh_CN.UTF-8
高速的字符集检测库。

%package devel
Summary: Files needed for developing with %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the files that are needed when building
software that uses %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
sed -i '\,^.SILENT:,d' buildsys.mk.in


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
magic_rpm_clean.sh

%check
cd src/tests/testbench
LD_LIBRARY_PATH=${RPM_BUILD_ROOT}%{_libdir} make


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.1.*

%files devel
%{_libdir}/%{name}.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.1-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1-4
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-2
- rebuild for GCC 4.7 as requested

* Sat Dec  3 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-1
- Upgrade to 1.1 with added %%check section.

* Fri Sep 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-3
- Use %%_isa in -devel package dependency.
- Drop %%defattr lines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-1
- Use fresh 1.0 release tarball, which only adds the makerelease.sh script.
- Drop unneeded BuildRoot stuff.

* Tue Jul 13 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.1.20100713
- Initial RPM packaging.
