# spec file for mcpp / compiler-independent-library-build on fedora

Summary:    Alternative C/C++ preprocessor
Name:       mcpp
Version:    2.7.2
Release:    7%{?dist}
License:    BSD
Group:      Development/Languages
Source:     http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL:        http://mcpp.sourceforge.net/
Patch0:     mcpp-manual.html.patch
# From http://www.zeroc.com/forums/patches/4445-patch-1-mcpp-2-7-2-a.html
Patch1:     patch.mcpp.2.7.2.txt
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%description
C/C++ preprocessor defines and expands macros and processes '#if',
'#include' and some other directives.

MCPP is an alternative C/C++ preprocessor with the highest conformance.
It supports multiple standards: K&R, ISO C90, ISO C99, and ISO C++98.
MCPP is especially useful for debugging a source program which uses
complicated macros and also useful for checking portability of a source.

Though mcpp could be built as a replacement of GCC's resident
preprocessor or as a stand-alone program without using library build of
mcpp, this package installs only a program named 'mcpp' which links
shared library of mcpp and behaves independent from GCC.

%prep
%setup -q
%patch0 -p0 -b -z.euc-jp
%patch1 -p1

%build
%configure --enable-mcpplib --disable-static
make CFLAGS="%{optflags}"

%install
iconv -f euc-jp -t utf-8 doc-jp/mcpp-manual.html > doc-jp/mcpp-manual-jp.html
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
rm -f $RPM_BUILD_ROOT%{_libdir}/libmcpp.la

%files
%defattr(-,root,root,-)
%doc    ChangeLog ChangeLog.old NEWS README
%{_datadir}/man/man1/%{name}.1.gz
%{_bindir}/%{name}

%package -n libmcpp

Summary:    Alternative C/C++ preprocessor (library build)
Group:      Development/Languages

%description -n libmcpp
This package provides a library build of mcpp.

%files -n libmcpp
%defattr(-,root,root,-)
%doc    LICENSE
%{_libdir}/libmcpp.so.*

%post -n libmcpp -p /sbin/ldconfig
%postun -n libmcpp -p /sbin/ldconfig

%package -n libmcpp-devel

Summary:    Alternative C/C++ preprocessor (development package for library build)
Group:      Development/Languages
Requires:   libmcpp = %{version}

%description -n libmcpp-devel
Development package for libmcpp.

%files -n libmcpp-devel
%defattr(-,root,root,-)
%{_libdir}/libmcpp.so
%{_includedir}/mcpp_lib.h
%{_includedir}/mcpp_out.h

%package doc

Summary:    Alternative C/C++ preprocessor (manual for library build)
Group:      Documentation

%description doc
This package provides an html manual for mcpp.

%files doc
%defattr(-,root,root,-)
%doc    LICENSE doc/mcpp-manual.html
%lang(ja) %doc  doc-jp/mcpp-manual-jp.html

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.7.2-7
- 为 Magic 3.0 重建

* Sun Jan 15 2012 Liu Di <liudidi@gmail.com> - 2.7.2-6
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.2-4
- Make subpackages to include LICENSE.

* Tue Oct 13 2009 Mary Ellen Foster <mefoster at gmail.com>
- Incorporate patch from Ice upstream project

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.2-1
- Upstream new release.

* Tue May 20 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7.1-1
- Upstream new release.
- Change to library build.
- Devide to 4 packages: mcpp, libmcpp, libmcpp-devel and mcpp-doc.
- Thanks to Mary Ellen Foster for correcting this spec file.

* Sun Mar 24 2008 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.7-2
- Upstream new release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.6.4-2
- Rebuild for selinux ppc32 issue.

* Thu May 19 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.4-1
- Upstream new release.

* Fri Apr 27 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-5
- Apply the new patch (patch1) for mcpp.

* Wed Apr 25 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-4
- Change installation of doc/mcpp-manual.html and doc-jp/mcpp-manual.html.

* Tue Apr 24 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-3
- Revise many points to adapt to the guideline of Fedora (thanks to
        the review by Mamoru Tasaka):
    use %%dist, %%configure, %%optflags, %%{_datadir}, %%lang(ja),
    convert encoding of mcpp-manual.html to utf-8,
    and others.

* Sat Apr 21 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-2
- Replace some variables with macros.
- Rename this spec file.

* Sat Apr 07 2007 Kiyoshi Matsui <kmatsui@t3.rim.or.jp> 2.6.3-1
- First release for V.2.6.3 on sourceforge.
