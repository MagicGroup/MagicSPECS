%global         _hardened_build 1

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           uriparser
Version:	0.8.4
Release:	3%{?dist}
Summary:        URI parsing library - RFC 3986
Summary(zh_CN.UTF-8): URI 解析库 - RFC 3986

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  doxygen, graphviz, cpptest-devel
Requires:       cpptest

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

%description -l zh_CN.UTF-8
URI 解析库。

%package	devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
sed -i 's/\r//' THANKS
sed -i 's/\r//' COPYING
iconv -f iso-8859-1 -t utf-8 -o THANKS{.utf8,}
mv THANKS{.utf8,}

%build

# Remove qhelpgenerator dependency by commenting Doxygen.in:
# sed -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' Doxyfile.in
sed -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' doc/Doxyfile.in

%configure --disable-static 

# disable rpath 
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Generate docs first
cd doc;
make %{?_smp_mflags}
cd ..
# Build
make %{?_smp_mflags}

%check
LD_LIBRARY_PATH=".libs" make check

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -delete

# fcami - update for https://fedoraproject.org/wiki/Changes/UnversionedDocdirs
if [ ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name} != ${RPM_BUILD_ROOT}%{_pkgdocdir} ]
  then mv ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}/html ${RPM_BUILD_ROOT}%{_pkgdocdir}
fi


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc THANKS AUTHORS COPYING ChangeLog
%{_bindir}/uriparse
%{_libdir}/*.so.*

%files devel
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_docdir}/%{name}-%{version}/*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.8.4-3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.8.4-2
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 0.8.4-1
- 更新到 0.8.4

* Thu Feb 12 2015 Liu Di <liudidi@gmail.com> - 0.8.1-5
- 为 Magic 3.0 重建

* Thu Jan 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-4
- Modernise spec

* Wed Jan 28 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-3
- Make uriCompareRangeA() return -1/0/1 like tests assume it does
  so package will build on aarch64.

* Fri Jan 09 2015 François Cami <fcami@fedoraproject.org> - 0.8.1-2
- Use PIC. 

* Mon Jan 05 2015 François Cami <fcami@fedoraproject.org> - 0.8.1-1
- Update to latest upstream.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 06 2013 François Cami <fcami@fedoraproject.org> - 0.8.0-1
- Update to latest upstream.

* Fri Sep 06 2013 François Cami <fcami@fedoraproject.org> - 0.7.9-1
- Update to latest upstream.

* Tue Aug 06 2013 François Cami <fcami@fedoraproject.org> - 0.7.8-2
- Fix FTBS due to https://fedoraproject.org/wiki/Changes/UnversionedDocdirs

* Tue Jul 30 2013 François Cami <fcami@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-3
- Fixed FTBFS

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-1
- Upgrade to 0.7.5:
-  Improved docs
-  Test suite
- 0.7.4
-  Cleaned up code and fixed memory leaks
- 0.7.3
-  Builds for Cygwin, minor bug fix
-  Changes in build system.
-  Added: Qt Assistant documentation output
- 0.7.2
-  Improved and cleaned API 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-6
- changed document file handling in spec, used better method - %%doc

* Fri Sep 05 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-5
- fixed group, removed redundant args for %%setup
- included ChangeLog, fixed html folder path in %%files
- fixed automated autotool calls

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-4
- changed name according to naming guidelines

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-3
- fixed buildrequires tag

* Sun Aug 10 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-2
- added documentation

* Sat Aug 9 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-1
- Initial build
