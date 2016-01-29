Name:           libconfuse
Version:        2.7
Release:        9%{?dist}
Summary:        A configuration file parser library
Summary(zh_CN.UTF-8): 一个配置文件解析库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        ISC
URL:            http://www.nongnu.org/confuse/
Source0:        http://savannah.nongnu.org/download/confuse/confuse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  check-devel, pkgconfig

%description
libConfuse is a configuration file parser library, licensed under
the terms of the ISC license, and written in C. It supports
sections and (lists of) values (strings, integers, floats,
booleans or other sections), as well as some other features (such
as single/double-quoted strings, environment variable expansion,
functions and nested include statements). It makes it very
easy to add configuration file capability to a program using
a simple API.

The goal of libConfuse is not to be the configuration file parser
library with a gazillion of features. Instead, it aims to be
easy to use and quick to integrate with your code.

%description -l zh_CN.UTF-8
一个配置文件解析库，以 C 编写并按 ISC 协议授权使用。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n confuse-%{version}
perl -pi.orig -e 's|confuse.h|../src/confuse.h|g' tests/check_confuse.c

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags} AM_CFLAGS="-Wall -Wextra"

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# Nuke libtool archive(s)
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Install man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
cp -p doc/man/man3/*.3 $RPM_BUILD_ROOT%{_mandir}/man3/
# Extract the example sources
mkdir -p ex2/examples
cp -p examples/{ftpconf.c,ftp.conf,simple.c,simple.conf,reread.c,reread.conf} \
    ex2/examples/
magic_rpm_clean.sh
%find_lang confuse || :

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%doc doc/html
%{_libdir}/libconfuse.so.*
%{_mandir}/man?/*.*

%files devel
%defattr(-,root,root,-)
%doc ex2/examples
%{_includedir}/confuse.h
%{_libdir}/libconfuse.so
%{_libdir}/pkgconfig/libconfuse.pc


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.7-9
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 2.7-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Jon Ciesla <limb@jcomserv.net> - 2.7-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 04 2008 Jarod Wilson <jwilson@redhat.com> 2.6-1
- New upstream release
- Switch from LGPL to ISC license
- Build fix from Hans Ulrich Niedermann

* Tue Sep 05 2006 Jarod Wilson <jwilson@redaht.com> 2.5-3
- Rebuild for new glibc

* Wed Aug 16 2006 Jarod Wilson <jwilson@redhat.com> 2.5-2
- Put -devel package in the right Group
- Add defattr for -devel files

* Wed Aug 16 2006 Jarod Wilson <jwilson@redhat.com> 2.5-1
- Initial build
