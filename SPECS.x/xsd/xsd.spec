Name:           xsd
Version:        4.0.0
Release:        12%{?dist}
Summary:        W3C XML schema to C++ data binding compiler
Summary(zh_CN.UTF-8): W3C XML schema 到 C++ 数据绑定的编译器
# Exceptions permit otherwise GPLv2 incompatible combination with ASL 2.0
License:        GPLv2 with exceptions and ASL 2.0  
URL:            http://www.codesynthesis.com/products/xsd/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://www.codesynthesis.com/download/xsd/%{majorver}/xsd-%{version}+dep.tar.bz2

Obsoletes:      xsd-devel <= 0:4.0.0-9

# Sent suggestion to upstream via e-mail 20090707
# http://anonscm.debian.org/cgit/collab-maint/xsd.git/tree/debian/patches/0001-xsd_xsdcxx-rename.patch
Patch0:         xsd-3.3.0-xsdcxx-rename.patch
Patch1:		xsd-Fix_bug_C++_Parser_Expat_Support.patch

BuildRequires: m4, xerces-c-devel, libcutl-devel
BuildRequires: boost-devel

%description
CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema to
C++ data binding compiler. Provided with an XML instance specification
(XML Schema), it generates C++ classes that represent the given
vocabulary as well as parsing and serialization code.
You can then access the data stored in XML using types and functions
that semantically correspond to your application domain rather than
dealing with intricacies of reading and writing XML.

%description -l zh_CN.UTF-8
W3C XML schema 到 C++ 数据绑定的编译器。

%package   doc
BuildArch: noarch
Summary:   API documentation files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文档

%description    doc
This package contains API documentation for %{name}.
%description doc -l zh_CN.UTF-8
%{name} 的开发文档。


%prep
%setup -q -n xsd-%{version}+dep
%patch0 -p1 -b .xsdcxx-rename
%patch1 -p0

##Unbundle libcutl
rm -rf libcutl

%build
make verbose=1 CXX=g++ CC=gcc CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="%{__global_ldflags}" BOOST_LINK_SYSTEM=y EXTERNAL_LIBCUTL=y

%install
rm -rf apidocdir

make install DESTDIR=$RPM_BUILD_ROOT LDFLAGS="%{__global_ldflags}" install_prefix=$RPM_BUILD_ROOT%{_prefix} \
 install_bin_dir=$RPM_BUILD_ROOT%{_bindir} install_man_dir=$RPM_BUILD_ROOT%{_mandir} EXTERNAL_LIBCUTL=y BOOST_LINK_SYSTEM=y

# Split API documentation to -doc subpackage.
mkdir -p apidocdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/*.{xhtml,css} apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/cxx/ apidocdir/
mv $RPM_BUILD_ROOT%{_datadir}/doc/xsd/ docdir/

# Convert to utf-8.
for file in docdir/NEWS; do
    mv $file timestamp
    iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
    touch -r timestamp $file
done

# Rename binary to xsdcxx to avoid conflicting with mono-web package.
# Sent suggestion to upstream via e-mail 20090707
# they will consider renaming in 4.0.0
mv $RPM_BUILD_ROOT%{_bindir}/xsd $RPM_BUILD_ROOT%{_bindir}/xsdcxx
mv $RPM_BUILD_ROOT%{_mandir}/man1/xsd.1 $RPM_BUILD_ROOT%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxsd

# Remove Microsoft Visual C++ compiler helper files.
rm -rf $RPM_BUILD_ROOT%{_includedir}/xsd/cxx/compilers

# Remove redundant PostScript files that rpmlint grunts about not being UTF8
# See: https://bugzilla.redhat.com/show_bug.cgi?id=502024#c27
# for Boris Kolpackov's explanation about those
find apidocdir -name "*.ps" | xargs rm -f
# Remove other unwanted crap
find apidocdir -name "*.doxygen" \
            -o -name "makefile" \
            -o -name "*.html2ps" | xargs rm -f

##Test failed on EPEL6 due to "bad" xerces-c
##http://codesynthesis.com/pipermail/xsd-users/2015-October/004696.html
%check
make -j 1 test EXTERNAL_LIBCUTL=y BOOST_LINK_SYSTEM=y

%files
%{!?_licensedir:%global license %doc}
%doc docdir/README docdir/NEWS docdir/FLOSSE
%license docdir/GPLv2 docdir/LICENSE
%{_bindir}/xsdcxx
%{_mandir}/man1/xsdcxx.1*
%{_includedir}/xsd/

%files doc
%{!?_licensedir:%global license %doc}
%doc docdir/README docdir/NEWS docdir/FLOSSE
%license docdir/GPLv2 docdir/LICENSE
%doc apidocdir/*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 4.0.0-12
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 4.0.0-11
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 4.0.0-10
- 为 Magic 3.0 重建

* Mon Oct 12 2015 Antonio Trande <sagitterATfedoraproject.org> - 4.0.0-9
- Header files included again in main package

* Mon Oct 12 2015 Antonio Trande <sagitterATfedoraproject.org> - 4.0.0-8
- Requires explicitely Boost148 in EPEL
- Tests not performed in EPEL6

* Thu Oct 08 2015 Antonio Trande <sagitterATfedoraproject.org> - 4.0.0-7
- Used %%license tag
- libcutl libraries unbundled
- Header files packaged apart
- Made tests

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 4.0.0-6
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 4.0.0-4
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.0.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 28 2015 Kalev Lember <kalevlember@gmail.com> - 4.0.0-1
- Update to 4.0.0

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-23
- rebuild (gcc5)

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.3.0-22
- Rebuild for boost 1.57.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.3.0-19
- Update config.* to fix FTBFS on aarch64/ppc64le

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 3.3.0-18
- Rebuild for boost 1.55.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 3.3.0-16
- Rebuild for boost 1.54.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.3.0-15
- Rebuild for Boost-1.53.0

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 3.3.0-14
- xsd-3.3.0-2+dep 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.0-12
- Update to xsd-3.3.0-1+dep upstream tarball, which includes the gcc 4.7 patch

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-11
- Rebuilt for c++ ABI breakage

* Thu Jan 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.3.0-10
- Add xsd-3.3.0-gcc47.patch (Fix mass rebuild FTBFS).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.3.0-8
- rebuild for https://fedoraproject.org/wiki/Features/F17Boost148

* Fri Jul 22 2011 Antti Andreimann <Antti.Andreimann@mail.ee> - 3.3.0-7
- Rebuilt for boost 1.47.0

* Wed Apr 06 2011 Kalev Lember <kalev@smartlink.ee> - 3.3.0-6
- Rebuilt for boost 1.46.1 soname bump

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 3.3.0-5
- Rebuilt with xerces-c 3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.3.0-3
- rebuild for new boost (thanks Petr Machata for the fix)

* Mon Aug 02 2010 Antti Andreimann <Antti.Andreimann@mail.ee> 3.3.0-2
- Rebuild for new boost

* Sun Jun 20 2010 Antti Andreimann <Antti.Andreimann@mail.ee> 3.3.0-1
- Updated to version 3.3.0
- Implemented a workaround for gcc segfault on el5

* Sun Feb 07 2010 Caolán McNamara <caolanm@redhat.com> - 3.2.0-7
- Rebuild for xerces soname bump

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.2.0-6
- Rebuild for Boost soname bump

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-4
- Removed redundant PostScript files from the doc package

* Mon Jul 06 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-3
- Added ACE homepage to SPEC file comments
- Added verbose=1 to MAKEFLAGS so compiler flags could be
  verified from build logs.

* Sat Jul 04 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-2
- Changed License tag to clarify which exceptions we are talking about

* Wed May 20 2009 Antti Andreimann <Antti.Andreimann@mail.ee> 3.2.0-1
- Initial RPM release.
