Name:           libsmi
Version:        0.4.8
Release:        10%{?dist}
Summary:        A library to access SMI MIB information
Summary(zh_CN.UTF-8): 访问 SMI MIB 信息的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.ibr.cs.tu-bs.de/projects/libsmi/index.html
Source0:        ftp://ftp.ibr.cs.tu-bs.de/pub/local/libsmi/%{name}-%{version}.tar.gz
Source1:        smi.conf
Patch0:		libsmi-0.4.8-wget111.patch
Patch1:		libsmi-0.4.8-CVE-2010-2891.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool
BuildRequires:  flex, bison
Requires:       gawk, wget

%description
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains tools to check, dump, and convert MIB
definitions and a steadily maintained and revised archive
of all IETF and IANA maintained standard MIB modules.

%description -l zh_CN.UTF-8
访问 SMI MIB 信息的库。

%package devel
Summary:        Development environment for libsmi library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %name = %version-%release
Requires:       pkgconfig

%description devel
Libsmi is a C library to access MIB module information through
a well defined API that hides the nasty details of locating
and parsing SMIv1/v2 MIB modules.

This package contains development files needed to develop
libsmi-based applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .wget111
%patch1 -p1 -b .CVE-2010-2891

%build
%configure \
    --enable-smi \
    --enable-sming \
    --enable-shared \
    --disable-static
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

iconv -f latin1 -t utf-8 <COPYING >COPYING.utf8
mv COPYING.utf8 COPYING

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/smi.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%check
# fails a couple of tests (2 in {0.4.4, 0.4.5})
make check ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE ChangeLog COPYING README THANKS TODO
%doc doc/draft-irtf-nmrg-sming-02.txt smi.conf-example
%config(noreplace) %{_sysconfdir}/smi.conf
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/mibs/
%{_datadir}/pibs/
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%{_datadir}/aclocal/libsmi.m4
%{_libdir}/pkgconfig/libsmi.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 0.4.8-10
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.4.8-9
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.8-8
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.8-5
- fix CVE-2010-2891

* Thu Feb 25 2010 Radek Vokal <rvokal@redhat.com> - 0.4.8-4
- fix lincese field, based on the tarball project is now GPL+

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.4.8-1
- update to 0.4.8
- patch fix for bz 441944

* Tue Feb 12 2008 Adam Jackson <ajax@redhat.com> 0.4.5-4
- Add %%defattr. (#430298)

* Thu Jan 10 2008 Stepan Kasal <skasal@redhat.com> - 0.4.5-3
- libsmi-devel should not require automake
- convert COPYING to utf-8

* Fri Oct  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.5-2
- Handle rpath problems in 64-bit systems (#209522).

* Mon May 29 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.5-1
- Update to 0.4.5.

* Wed May 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.4-1
- Update to 0.4.4.

* Fri Apr  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.4.3-1
- First build.

# vim:set ai ts=4 sw=4 sts=4 et:
