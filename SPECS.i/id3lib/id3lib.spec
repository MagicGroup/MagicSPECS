Summary:	Library for manipulating ID3v1 and ID3v2 tags
Summary(zh_CN.UTF-8):	处理ID3v1和ID3v2标签的库
Name:		id3lib
Version:	3.8.3
Release:	14%{?dist}
License:	LGPL
Group:		System Environment/Libraries
Group(zh_CN.UTF-8):	系统环境/库
URL:		http://id3lib.sourceforge.net/
Source0:	http://dl.sf.net/sourceforge/id3lib/%{name}-%{version}.tar.gz
Patch0:		id3lib-dox.patch
Patch1:		id3lib-3.8.3-libtool-autofoo.patch.bz2
Patch2:		id3lib-3.8.3-io_helpers-163101.patch
Patch3:		id3lib-3.8.3-gcc43-1.patch 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	zlib-devel doxygen

%description
This package provides a software library for manipulating ID3v1 and
ID3v2 tags. It provides a convenient interface for software developers
to include standards-compliant ID3v1/2 tagging capabilities in their
applications. Features include identification of valid tags, automatic
size conversions, (re)synchronisation of tag frames, seamless tag
(de)compression, and optional padding facilities. Additionally, it can
tell mp3 header info, like bitrate etc.

%description -l zh_CN.UTF-8
这个包提供了一个处理ID3v1和ID3v2标签的软件库。它提供给软件开发者便于使用
的接口，可以在他们的程序中包括标准ID3v1/2标签处理能力。

%package devel
Summary:	Development tools for the id3lib library
Summary(zh_CN.UTF-8):	id3lib库的开发工具
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel

%description devel
This package provides files needed to develop with the id3lib.

%description devel -l zh_CN.UTF-8
这个提供了使用id3lib开发所需要的文件。

%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .libtool-autofoo
%patch2 -p1 -b .io_helpers-163101
%patch3 -p1 -b .gcc43
chmod -x src/*.h src/*.cpp include/id3/*.h
sed -i -e 's/\r//' doc/id3v2.3.0.*
sed -i -e 's|@DOX_DIR_HTML@|%{_docdir}/%{name}-devel-%{version}/api|' \
    doc/index.html.in


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT
make docs
mkdir -p __doc/doc ; cp -p doc/*.{gif,jpg,png,html,txt,ico,css,php}  __doc/doc
rm -f $RPM_BUILD_ROOT%{_libdir}/libid3.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog HISTORY NEWS README THANKS TODO __doc/doc/
%{_libdir}/libid3-3.8.so.*
%{_bindir}/id3convert
%{_bindir}/id3cp
%{_bindir}/id3info
%{_bindir}/id3tag

%files devel
%defattr(-,root,root,-)
%doc doc/api/
%{_includedir}/id3.h
%{_includedir}/id3/
%{_libdir}/libid3.so


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.8.3-14
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.8.3-13
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.8.3-12
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 3.8.3-11
- 为 Magic 3.0 重建

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 3.8.3-8mgc
- rebuild for Magic
