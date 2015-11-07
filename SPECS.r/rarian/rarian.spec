### Abstract ###

Name: rarian
Version: 0.8.1
Release: 7%{?dist}
License: LGPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Summary: Rarian is a documentation meta-data library
Summary(zh_CN.UTF-8):	Rarian 是一个文档元数据库
URL: http://ftp.gnome.org/pub/gnome/sources/rarian
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://ftp.gnome.org/pub/gnome/sources/rarian/%{majorver}/rarian-%{version}.tar.bz2
Source1: scrollkeeper-omf.dtd
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

### Dependencies ###

Requires(post): libxml2
Requires(postun): libxml2
# for /usr/bin/xmlcatalog

Requires: libxslt
# for /usr/bin/xsltproc
Requires: coreutils, util-linux, gawk
# for basename, getopt, awk, etc

### Build Dependencies ###

BuildRequires: libxslt-devel

%description
Rarian is a documentation meta-data library that allows access to documents,
man pages and info pages.  It was designed as a replacement for scrollkeeper.

%description -l zh_CN.UTF-8
Rarian 是一个文档元数据库，可以用来访问文档，手册页和信息页。
它被用来替代 scrollkeeper。

%package compat
License: GPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Summary: Extra files for compatibility with scrollkeeper
Summary(zh_CN.UTF-8): 兼容 scrollkeeper 的额外文件
Requires: rarian = %{version}-%{release}
Requires(post): rarian
# The scrollkeeper version is arbitrary.  It just
# needs to be greater than what we're obsoleting.
Provides: scrollkeeper = 0.4
Obsoletes: scrollkeeper <= 0.3.14

%description compat
This package contains files needed to maintain backward-compatibility with
scrollkeeper.

%description compat -l zh_CN.UTF-8
这个包包含了与 scrollkeeper 向后兼容的文件。

%package devel
Group: Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Summary: Development files for Rarian
Summary(zh_CN.UTF-8): Rarian 的开发文件
Requires: rarian = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains files required to develop applications that use the
Rarian library ("librarian").

%description devel -l zh_CN.UTF-8
Rarian 的开发文件。

%prep
%setup -q

%build

%configure --disable-skdb-update
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/xml/scrollkeeper/dtds
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xml/scrollkeeper/dtds

rm -rf $RPM_BUILD_ROOT%{_libdir}/librarian.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/librarian.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post compat
%{_bindir}/rarian-sk-update

# Add OMF DTD to XML catalog.
CATALOG=/etc/xml/catalog
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :

%postun -p /sbin/ldconfig

%postun compat

# Delete OMF DTD from XML catalog.
if [ $1 = 0 ]; then
  CATALOG=/etc/xml/catalog
  /usr/bin/xmlcatalog --noout --del \
    "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc README COPYING COPYING.LIB COPYING.UTILS ChangeLog NEWS AUTHORS
%{_bindir}/rarian-example
%{_libdir}/librarian.so.*
%{_datadir}/librarian
%{_datadir}/help

%files compat
%defattr(-,root,root,-)
%{_bindir}/rarian-sk-*
%{_bindir}/scrollkeeper-*
%{_datadir}/xml/scrollkeeper

%files devel
%defattr(644,root,root,755)
%{_includedir}/rarian
%{_libdir}/librarian.so
%{_libdir}/pkgconfig/rarian.pc

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.1-7
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 0.8.1-6
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.8.1-5
- 为 Magic 3.0 重建

* Fri Oct 26 2012 Liu Di <liudidi@gmail.com> - 0.8.1-4
- 为 Magic 3.0 重建

* Wed Feb 01 2012 Liu Di <liudidi@gmail.com> - 0.8.1-3
- 为 Magic 3.0 重建

* Thu Jun 06 2008 Liu Di <liudidi@gmail.com> - 0.8.0-1mgc
- 为 Magic 重建
