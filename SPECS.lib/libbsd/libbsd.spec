Name:		libbsd
Version:	0.6.0
Release:	1%{?dist}
Summary:	Library providing BSD-compatible functions for portability
Summary(zh_CN.UTF-8): 提供 BSD 兼容函数的库
URL:		http://libbsd.freedesktop.org/

Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz

License:	BSD and ISC and Copyright only and Public Domain
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%description -l zh_CN.UTF-8
libbsd 提供了一个在 BSD 系统上使用的函数，使从 BSD 系统上移植程序更容易。

%package devel
Summary:	Development files for libbsd
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	libbsd = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development files for the libbsd library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

# fix encoding of flopen.3 man page
for f in man/flopen.3; do
  iconv -f iso8859-1 -t utf-8 $f >$f.conv
  touch -r $f $f.conv
  mv $f.conv $f
done

%configure

%build
make CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
make libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot} \
     install

# don't want static library or libtool archive
rm %{buildroot}%{_libdir}/%{name}*.a
rm %{buildroot}%{_libdir}/%{name}.la

magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING README TODO ChangeLog
%{_libdir}/%{name}.so.*

%files devel
%{_mandir}/man3/*.3.gz
%{_mandir}/man3/*.3bsd.gz
%{_includedir}/bsd
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-overlay.pc
%{_libdir}/pkgconfig/%{name}-ctor.pc

%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 0.6.0-1
- 更新到 0.6.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.1-2
- 为 Magic 3.0 重建

* Sun Jun 03 2012 Eric Smith <eric@brouhaha.com> - 0.4.1-1
- Update to latest upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Eric Smith <eric@brouhaha.com> - 0.3.0-1
- Update to latest upstream release.
- Removed Patch0, fixed upstream.
- Removed BuildRoot, clean, defattr.

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-3
- changes based on review by Sebastian Dziallas

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-2
- changes based on review comments by Jussi Lehtola and Ralf Corsepious

* Thu Jan 28 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-1
- initial version
