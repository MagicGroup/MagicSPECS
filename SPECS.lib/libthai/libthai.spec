%define datrie_version 0.2.8

Summary:  Thai language support routines
Summary(zh_CN.UTF-8): 泰语支持例程
Name: libthai
Version: 0.1.18
Release: 3%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source: ftp://linux.thai.net/pub/thailinux/software/libthai/libthai-%{version}.tar.gz
Source1: ftp://linux.thai.net/pub/thailinux/software/libthai/libdatrie-%{datrie_version}.tar.xz
Patch: libthai-libdatrie-static-build.patch
Patch1: libthai-0.1.9-doxygen-segfault.patch
Patch2: libthai-0.1.9-multilib.patch
URL: http://linux.thai.net
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig
BuildRequires: doxygen
# we edit the Makefile.am's
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

%description
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their applications.
It includes important Thai-specific functions e.g. word breaking, input and
output methods as well as basic character and string supports.

%description -l zh_CN.UTF-8
泰语支持例程。

%package devel
Summary:  Thai language support routines
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libthai-devel package includes the header files and developer docs 
for the libthai package.

Install libthai-devel if you want to develop programs which will use
libthai.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version} -a 1
mv libdatrie-%{datrie_version} libdatrie
%patch -p1 -b .static-build
%patch1 -p1 -b .doxygen-segfault
%patch2 -p1 -b .multilib

%build

# libthai depends on this library called libdatrie.  libdatrie is a
# data-structure implementaiton that the author of libthai ripped out of it.
# However, since libthai is the only user of that code, there's no reason to
# 1) package it separately, 2) use it as a shared library.
# So, we compile it as a libtool convenience library and include in libthai.so,
# and use symbol hiding to hide them (and other internal symbols).
#
# The patch takes care of making datrie into a convenience lib and making sure
# libthai will include it (and hide its symbols), and the exports make sure
# libthai finds the uninstalled libdatrie.  We need to call automake, since
# the patch modifies a few Makefile.am's.

{
  pushd libdatrie
  autoreconf -i -f
  %configure
  make
  popd
}

export DATRIE_CFLAGS="-I$PWD/libdatrie"
export DATRIE_LIBS="$PWD/libdatrie/datrie/libdatrie.la"
export PATH="$PWD/libdatrie/tools:$PATH"

autoreconf -i -f

%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# move installed doc files back to build directory to package them
# in the right place
mkdir installed-docs
mv $RPM_BUILD_ROOT%{_docdir}/libthai/* installed-docs
rmdir $RPM_BUILD_ROOT%{_docdir}/libthai

rm $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING ChangeLog
%{_libdir}/lib*.so.*
%{_datadir}/libthai

%files devel
%defattr(-, root, root)
%doc installed-docs/*
%{_includedir}/thai
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
#%{_mandir}/man3/*

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.1.18-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.1.18-2
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.1.18-1
- 更新到 0.1.18

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1.14-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.1.14-5
- 为 Magic 3.0 重建

