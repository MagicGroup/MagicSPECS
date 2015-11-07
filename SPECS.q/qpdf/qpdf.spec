Summary: Command-line tools and library for transforming PDF files
Summary(zh_CN.UTF-8): 转换 PDF 文件的命令行工具和库
Name:    qpdf
Version:	5.1.3
Release:	2%{?dist}
# MIT: e.g. libqpdf/sha2.c
License: Artistic 2.0 and MIT
URL:     http://qpdf.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/qpdf/qpdf-%{version}.tar.gz

BuildRequires: zlib-devel
BuildRequires: pcre-devel

# for fix-qdf and test suite
BuildRequires: perl
BuildRequires: perl(Digest::MD5)

# for autoreconf
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: qpdf-libs%{?_isa} = %{version}-%{release}

%package libs
Summary: QPDF library for transforming PDF files
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%package devel
Summary: Development files for QPDF library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: qpdf-libs%{?_isa} = %{version}-%{release}

%package doc
Summary: QPDF Manual
Summary(zh_CN.UTF-8): %{name} 的文档
Group:   Documentation
Group(zh_CN.UTF-8): 文档
BuildArch: noarch
Requires: qpdf-libs = %{version}-%{release}

%description
QPDF is a command-line program that does structural, content-preserving
transformations on PDF files. It could have been called something
like pdf-to-pdf. It includes support for merging and splitting PDFs
and to manipulate the list of pages in a PDF file. It is not a PDF viewer
or a program capable of converting PDF into other formats.

%description -l zh_CN.UTF-8
转换 PDF 文件的命令行工具和库。

%description libs
QPDF is a C++ library that inspect and manipulate the structure of PDF files.
It can encrypt and linearize files, expose the internals of a PDF file,
and do many other operations useful to PDF developers.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%description devel
Header files and libraries necessary
for developing programs using the QPDF library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%description doc
QPDF Manual

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q

sed -i -e '1s,^#!/usr/bin/env perl,#!/usr/bin/perl,' qpdf/fix-qdf

%build
# work-around check-rpaths errors
autoreconf --verbose --force --install

%configure --disable-static \
           --enable-show-failed-test-output

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# https://fedoraproject.org/wiki/Packaging_tricks#With_.25doc
mkdir __doc
mv  %{buildroot}%{_datadir}/doc/qpdf/* __doc
rm -rf %{buildroot}%{_datadir}/doc/qpdf

rm -f %{buildroot}%{_libdir}/libqpdf.la
magic_rpm_clean.sh

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/fix-qdf
%{_bindir}/qpdf
%{_bindir}/zlib-flate
%{_mandir}/man1/*

%files libs
%doc README TODO ChangeLog Artistic-2.0
%{_libdir}/libqpdf*.so.*

%files devel
%doc examples/*.cc examples/*.c
%{_includedir}/*
%{_libdir}/libqpdf*.so
%{_libdir}/pkgconfig/libqpdf.pc

%files doc
%doc __doc/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.1.3-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 5.1.3-1
- 更新到 5.1.3

* Wed Jan 15 2014 Jiri Popelka <jpopelka@redhat.com> - 5.1.1-1
- 5.1.1

* Wed Dec 18 2013 Jiri Popelka <jpopelka@redhat.com> - 5.1.0-1
- 5.1.0

* Mon Oct 21 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.1-1
- 5.0.1

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 5.0.0-4
- Perl 5.18 rebuild

* Mon Jul 22 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.0-3
- change shebang to absolute path (#987040)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0.0-2
- Perl 5.18 rebuild

* Thu Jul 11 2013 Jiri Popelka <jpopelka@redhat.com> - 5.0.0-1
- 5.0.0

* Mon Jul 08 2013 Jiri Popelka <jpopelka@redhat.com> - 4.2.0-1
- 4.2.0

* Thu May 23 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-3
- fix 'complete manual location' note in man pages (#966534)

* Tue May 07 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-2
- some source files are under MIT license

* Mon Apr 15 2013 Jiri Popelka <jpopelka@redhat.com> - 4.1.0-1
- 4.1.0

* Tue Mar 05 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.1-3
- work around gcc 4.8.0 issue on ppc64 (#915321)
- properly handle overridden compressed objects

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jiri Popelka <jpopelka@redhat.com> 4.0.1-1
- 4.0.1

* Wed Jan 02 2013 Jiri Popelka <jpopelka@redhat.com> 4.0.0-1
- 4.0.0

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.2-1
- 3.0.2

* Thu Aug 16 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-3
- the previously added requirement doesn't need to be arch-specific

* Thu Aug 16 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-2
- doc subpackage requires libs subpackage due to license file (#848466)

* Wed Aug 15 2012 Jiri Popelka <jpopelka@redhat.com> 3.0.1-1
- initial spec file
