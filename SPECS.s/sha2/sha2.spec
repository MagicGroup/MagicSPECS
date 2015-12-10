Name:		sha2
Version:	1.0.1
Release:	6%{?dist}
Summary:	SHA Implementation Library
Summary(zh_CN.UTF-8): SHA 实现库
License:	BSD
URL:		http://www.aarongifford.com/computers/sha.html
Source0:	http://www.aarongifford.com/computers/%{name}-%{version}.tgz
# Makefile to build the binaries. Sent upstream via email
Source1:	%{name}-Makefile

%description
The library implements the SHA-256, SHA-384, and SHA-512 hash algorithms. The
interface is similar to the interface to SHA-1 found in the OpenSSL library.

sha2 is a simple program that accepts input from either STDIN or reads one or
more files specified on the command line, and then generates the specified hash
(either SHA-256, SHA-384, SHA-512, or any combination thereof, including all
three at once).
%description -l zh_CN.UTF-8
SHA 算法实现库.

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
cp -a %{SOURCE1} Makefile

%build
make %{?_smp_mflags} \
	OPTFLAGS="%{optflags}"

%install
make install \
	DESTDIR=%{buildroot} \
	LIBDIR=%{_libdir} \
	INCLUDEDIR=%{_includedir} \
	BINDIR=%{_bindir} \
	OPTFLAGS="%{optflags}"
magic_rpm_clean.sh

%check
LD_PRELOAD=./libsha2.so ./sha2test.pl

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc README
%{_libdir}/libsha2.so.*
%{_bindir}/sha2*


%files devel
%{_includedir}/sha2.h
%{_libdir}/libsha2.so


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.1-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.1-5
- 为 Magic 3.0 重建

* Sun Sep 27 2015 Liu Di <liudidi@gmail.com> - 1.0.1-4
- 为 Magic 3.0 重建

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 16 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-1
- Initial build
