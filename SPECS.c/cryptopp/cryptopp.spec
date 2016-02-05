Name:           cryptopp
Version:        5.6.3
Release:        2%{?dist}
Summary:        C++ class library of cryptographic schemes
Summary(zh_CN.UTF-8): 密码方案的 C++ 类库
License:        Boost
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://www.cryptopp.com/
Source0:        http://www.cryptopp.com/cryptopp563.zip
Source1:        cryptopp.pc
Patch0:         cryptopp-autotools.patch
# Debian patch installs TestVectors and TestData in /usr/share/cryptopp/
# http://groups.google.com/group/cryptopp-users/browse_thread/thread/6fe2192340f07e5d
Patch1:         cryptopp-data-files-location.patch
BuildRequires:  doxygen, autoconf, libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Crypto++ Library is a free C++ class library of cryptographic schemes.
See http://www.cryptopp.com/ for a list of supported algorithms.

One purpose of Crypto++ is to act as a repository of public domain
(not copyrighted) source code. Although the library is copyrighted as a
compilation, the individual files in it are in the public domain.

%description -l zh_CN.UTF-8
密码方案的 C++ 类库。

%package devel
Summary:        Header files and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
%description devel
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains the header files and development documentation
for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch

%description doc
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package progs
Summary:        Programs for manipulating %{name} routines
Summary(zh_CN.UTF-8): %{name} 的相关程序
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires:       %{name} = %{version}-%{release}

%description progs
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains programs for manipulating %{name} routines.

%description progs -l zh_CN.UTF-8
%{name} 的相关程序。

%prep
%setup -q -c
rm -f GNUmakefile
%patch0 -p1
%patch1 -p1
autoreconf --verbose --force --install
perl -pi -e 's/\r$//g' License.txt Readme.txt

%build
%configure --disable-static

make %{?_smp_mflags}
doxygen

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c "
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install the pkg-config file
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/cryptopp.pc
# Fill in the variables
sed -i "s|@PREFIX@|%{_prefix}|g" $RPM_BUILD_ROOT%{_libdir}/pkgconfig/cryptopp.pc
sed -i "s|@LIBDIR@|%{_libdir}|g" $RPM_BUILD_ROOT%{_libdir}/pkgconfig/cryptopp.pc

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/TestVectors
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/TestData
install -m644 TestVectors/* $RPM_BUILD_ROOT%{_datadir}/%{name}/TestVectors
install -m644 TestData/* $RPM_BUILD_ROOT%{_datadir}/%{name}/TestData

rm -f $RPM_BUILD_ROOT%{_bindir}/cryptestcwd

%check
./cryptestcwd v

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc License.txt Readme.txt
%defattr(-,root,root,0755)
%{_libdir}/libcryptopp.so.6*

%files devel
%defattr(0644,root,root,0755)
%{_includedir}/cryptopp
%defattr(-,root,root,0755)
%{_libdir}/libcryptopp.so
%{_libdir}/pkgconfig/cryptopp.pc

%files progs
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/cryptest
%{_datadir}/%{name}


%changelog
* Thu Feb 04 2016 Liu Di <liudidi@gmail.com> - 5.6.3-2
- 为 Magic 3.0 重建

* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 5.6.2-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 5.6.2-4
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.2-2
- cryptopp.pc cleanup

* Wed Apr  3 2013 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.2-1
- Crypto++ 5.6.2
- License: Boost

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-7
- Rebuilt for c++ ABI breakage

* Thu Jan  5 2012 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-6
- fix build with gcc-4.7.0

* Mon Oct 17 2011 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-5
- remove includedir in cryptopp.pc (rhbz#732208)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-3
- patch config.h for enable SSE2 only on x86_64

* Thu Oct 21 2010 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-2
- add -DCRYPTOPP_DISABLE_SSE2 to CXXFLAGS instead of config.h for non-x86_64 (rhbz#645169)
- install TestVectors and TestData in cryptopp-progs
- patch cryptest for using data files in /usr/share/cryptopp
- build cryptestcwd for build time test only
- fix check section

* Wed Sep  1 2010 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-1
- Crypto++ 5.6.1
- fixed pkgconfig file installation
- build cryptopp-doc as noarch subpkg

* Thu Nov 26 2009 Alexey Kurov <nucleo@fedoraproject.org> - 5.6.1-0.1.svn479
- svn r479. MARS placed in the public domain by Wei Dai
- Fixes rhbz#539227

* Fri Oct 30 2009 Rahul Sundaram <sundaram@fedoraproject.org> 5.6.0-5
- Fix source

* Wed Oct 28 2009 Rahul Sundaram <sundaram@fedoraproject.org> 5.6.0-4
- Add pkgconfig file. Fixes rhbz#512761

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Dan Horak <dan[at]dannu.cz> 5.6.0-2
- add support for s390/s390x

* Sun Mar 15 2009 Aurelien Bompard <abompard@fedoraproject.org> 5.6.0-1
- version 5.6.0
- rediff patches

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 30 2008 Aurelien Bompard <abompard@fedoraproject.org> 5.5.2-3
- purge source archive from patented code
- use SSE2 on x86_64
- preserve timestamps on install

* Mon Sep 22 2008 Aurelien Bompard <abompard@fedoraproject.org> 5.5.2-2
- rediff gcc 4.3 patch

* Wed Aug 27 2008 Aurelien Bompard <abompard@fedoraproject.org> 5.5.2-1
- adapt to fedora, from Mandriva
