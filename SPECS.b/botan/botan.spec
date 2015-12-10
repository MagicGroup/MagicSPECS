%global major_version 1.10

Name:           botan
Version:	1.10.10
Release:	3%{?dist}
Summary:        Crypto library written in C++
Summary(zh_CN.UTF-8): C++ 编写的加密库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://botan.randombit.net/
# tarfile is stripped using repack.sh. original tarfile to be found
# here: http://files.randombit.net/botan/Botan-%%{version}.tbz
#Source0:        Botan-%{version}.stripped.tbz
Source0:	http://botan.randombit.net/releases/Botan-%{version}.tgz
Source1:        README.fedora
Patch0:         botan-aarch64.patch
Patch1:         botan-1.10-add-ppc64le.patch
# Enable only cleared ECC algorithms
Patch2:         botan-1.10.5-ecc-fix.patch

BuildRequires:  gcc-c++
BuildRequires:  python
BuildRequires:  python-sphinx
BuildRequires:  python-devel
BuildRequires:  boost-python-devel

BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel

# do not check .so files in the python_sitelib directory
%global __provides_exclude_from ^(%{python_sitearch}/.*\\.so)$

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%description
Botan is a BSD-licensed crypto library written in C++. It provides a
wide variety of basic cryptographic algorithms, X.509 certificates and
CRLs, PKCS \#10 certificate requests, a filter/pipe message processing
system, and a wide variety of other features, all written in portable
C++. The API reference, tutorial, and examples may help impart the
flavor of the library.

%description -l zh_CN.UTF-8
C++ 编写的加密库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       bzip2-devel
Requires:       zlib-devel
Requires:       openssl-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch

%description    doc
%{summary}

This package contains HTML documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%package        python
Summary:        Python bindings for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description    python
%{summary}

This package contains the Python binding for %{name}.

Note: The Python binding should be considered alpha software, and the
interfaces may change in the future.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q -n Botan-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .eccfix

# These tests will fail.
rm -rf checks/ec_tests.cpp

%build
# we have the necessary prerequisites, so enable optional modules
%define enable_modules bzip2,zlib,openssl

# fixme: maybe disable unix_procs, very slow.
%define disable_modules gnump

./configure.py \
        --prefix=%{_prefix} \
        --libdir=%{_lib} \
        --cc=gcc \
        --os=linux \
        --cpu=%{_arch} \
        --enable-modules=%{enable_modules} \
        --disable-modules=%{disable_modules} \
        --with-boost-python \
        --with-python-version=%{python_version} \
        --with-sphinx

# (ab)using CXX as an easy way to inject our CXXFLAGS
make CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags}
make -f Makefile.python \
  CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags}


%install
make install \
     DESTDIR=%{buildroot}%{_prefix} \
     DOCDIR=%{buildroot}%{_pkgdocdir} \
     INSTALL_CMD_EXEC="install -p -m 755" \
     INSTALL_CMD_DATA="install -p -m 644"

make -f Makefile.python install \
     PYTHON_SITE_PACKAGE_DIR=%{buildroot}%{python_sitearch}

# fixups
find doc/examples -type f -exec chmod -x {} \;
mv doc/examples/python doc/python-examples
cp -a doc/{examples,python-examples,license.txt} \
   %{buildroot}%{_pkgdocdir}
cp -a %{SOURCE1} %{buildroot}%{_pkgdocdir}
rm -r %{buildroot}%{_pkgdocdir}/manual/{.doctrees,.buildinfo}
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%dir %{_pkgdocdir}
%{_pkgdocdir}/readme.txt
%{_pkgdocdir}/license.txt
%{_pkgdocdir}/README.fedora
%{_libdir}/libbotan-%{major_version}.so.*


%files devel
%{_pkgdocdir}/examples
%{_bindir}/botan-config-%{major_version}
%{_includedir}/*
%exclude %{_libdir}/libbotan-%{major_version}.a
%{_libdir}/libbotan-%{major_version}.so
%{_libdir}/pkgconfig/botan-%{major_version}.pc


%files doc
%dir %{_pkgdocdir}
%{_pkgdocdir}/manual
# next files duplicated on purpose, because -doc doesn't depend on the
# main package
%{_pkgdocdir}/readme.txt
%{_pkgdocdir}/license.txt
%{_pkgdocdir}/README.fedora


%files python
%{_pkgdocdir}/python-examples
%exclude %{_pkgdocdir}/python-examples/*.pyc
%exclude %{_pkgdocdir}/python-examples/*.pyo
%{python_sitearch}/%{name}


%check
make CXX="g++ ${CXXFLAGS:-%{optflags}}" %{?_smp_mflags} check

# these checks would fail
mv checks/validate.dat{,.orig}
awk '/\[.*\]/{f=0} /\[(RC5.*|RC6)\]/{f=1} (f && !/^#/){sub(/^/,"#")} {print}' \
    checks/validate.dat.orig > checks/validate.dat
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./check --validate


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.10.10-3
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.10.10-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 1.10.10-1
- 更新到 1.10.10

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.10.9-8
- Rebuilt for Boost 1.59

* Fri Jul 24 2015 David Tardon <dtardon@redhat.com> - 1.10.9-7
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.9-5
- Rebuild for gcc5.

* Fri Feb  6 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.9-4
- Re-enable cleared ECC. Patch by Tom Callaway <spot@fedoraproject.org>.

* Thu Feb  5 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.9-3
- Disable gmp engine (see bug 1116406).
- Use _pkgdocdir.

* Thu Feb  5 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.9-2
- Remove workaround for bug 1186014.

* Sat Jan 31 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.9-1
- Update to 1.10.9.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Björn Esser <bjoern.esser@gmail.com> - 1.10.8-5
- rebuild for boost 1.55.0 (libboost_python.so.1.55.0)

* Sun May 25 2014 Brent Baude <baude@us.ibm.com> - 1.10.8-4
- Added ppc64le arch support

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 1.10.8-3
- rebuild for boost 1.55.0

* Mon May 12 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.10.8-2
- Added AArch64 architecture support

* Sat May 10 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.8-1
- Update to 1.10.8.

* Tue Sep  3 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.5-4
- Re-enable IDEA (rhbz#1003052) and SRP-6.

* Sat Jul 27 2013 Petr Machata <pmachata@redhat.com> - 1.10.5-3
- Rebuild for boost 1.54.0

* Fri Jul 26 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.5-2
- Rename the subpackage for the Python binding.

* Fri Jul 26 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.5-1
- Update to 1.10.5.
- Modernize spec file.
- New -doc subpackage containing HTML documentation.
- Package Python binding.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.14-1
- Update to 1.8.14.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-4.2
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8.13-2.2
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 1.8.13-2.1
- rebuild with new gmp

* Thu Jul 21 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.13-2
- Patch to revert the soname change.

* Wed Jul 20 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.13-1
- Update to 1.8.13.

* Sat Jul  2 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.12-1
- Update to 1.8.12.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov  6 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.11-1
- Update to 1.8.11.

* Sat Sep  4 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.10-1
- Update to 1.8.10.

* Sun Aug 29 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-4
- Update README.fedora.

* Fri Aug 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-3
- Also remove RC5 from the tarfile.
- Comment out RC5, RC6 and IDEA validation tests.

* Wed Aug  4 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-2
- Remove IDEA, RC6, and ECC-related modules from the tarfile,
  see bz 615372.

* Wed Jun 16 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-1
- Update to 1.8.9.
- Drop patch applied upstream.

* Thu Nov 19 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-2
- Add patch from upstream to build with binutils-2.20.51.0.2.
  Fixes bz 538949 (ftbfs).

* Thu Nov  5 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-1
- Update to 1.8.8, a bugfix release.

* Thu Sep 10 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.7-1
- Update to 1.8.7. This is mainly a bugfix release.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.6-2
- rebuilt with new openssl

* Thu Aug 13 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.6-1
- Update to 1.8.6, which contains new features as well as bugfixes,
  e.g. concerning the /proc-walking entropy source.

* Wed Aug 12 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.5-2
- Fix changelog.

* Wed Aug 12 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.5-1
- Update to 1.8.5.
- Use .tbz source file.
- Configuration script uses python now.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.2-1
- Update to 1.8.2.

* Mon Mar 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.1-4
- Add missing requirements to -devel package.

* Fri Feb 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.1-3
- Rebuilt again after failed attempt in mass rebuild.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.1-1
- Update to 1.8.1. This is a bugfix release, see
  http://botan.randombit.net/news/releases/1_8_1.html for changes.
- No need to explicitly enable modules that will be enabled by
  configure.pl anyway.

* Mon Jan 19 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.0-2
- Move api* and tutorial* doc files to -devel package.

* Sat Jan 17 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.0-1
- New package.
