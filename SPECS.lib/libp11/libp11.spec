Name:           libp11
Version:        0.2.8
Release:        5%{?dist}
Summary:        Library for using PKCS#11 modules
Summary(zh_CN.UTF-8): 使用 PCS#11 模块的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.opensc-project.org/libp11
Source0:        http://www.opensc-project.org/files/libp11/libp11-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  doxygen graphviz
BuildRequires:  libtool-ltdl-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig

%description
Libp11 is a library implementing a small layer on top of PKCS#11 API to
make using PKCS#11 implementations easier.

%description -l zh_CN.UTF-8
使用 PCS#11 模块的库。

%package devel
Summary:        Files for developing with %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static --enable-api-doc
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Use %%doc to install documentation in a standard location
mkdir __docdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ __docdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_libdir}/libp11.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/ __docdir/api/
%{_libdir}/libp11.so
%{_libdir}/pkgconfig/libp11.pc
%{_includedir}/libp11.h

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.2.8-5
- 为 Magic 3.0 重建

* Fri Jul 25 2014 Liu Di <liudidi@gmail.com> - 0.2.8-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.8-3
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 0.2.8-2
- 为 Magic 3.0 重建

* Fri Apr 15 2011 Kalev Lember <kalev@smartlink.ee> - 0.2.8-1
- Update to 0.2.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.2.7-2
- Spec file cleanup
- Don't install html docs with main library package
- Removed R: pkgconfig from -devel as it is now automatically added

* Wed Nov 25 2009 Kalev Lember <kalev@smartlink.ee> - 0.2.7-1
- Update to 0.2.7

* Sat Aug 22 2009 Kalev Lember <kalev@smartlink.ee> - 0.2.6-1
- Update to 0.2.6
- Enable building documentation with doxygen
- Use INSTALL="install -p" to preserve timestamps

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.2.3-8
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.2.3-5
- rebuild with new openssl

* Fri Nov 28 2008 Adam Tkac <atkac redhat com> - 0.2.3-4
- rebuild against new libltdl

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.3-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.3-2
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Matt Anderson <mra@hp.com> - 0.2.3-1
- Update to latest upstream sources

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.2.2-7
- Rebuild for deps

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.2.2-6
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Matt Anderson <mra@hp.com> - 0.2.2-5
- Additional suggestions by tibbs@math.uh.edu, Source0 URL and license in docs

* Wed Jun 27 2007 Matt Anderson <mra@hp.com> - 0.2.2-4
- Merged in changes suggested by michael@gmx.net

* Thu Jun 21 2007 Matt Anderson <mra@hp.com> - 0.2.2-3
- Rebuilt .spec file based on rpmdev-newspec template
- Added --disable-static to comply with Fedora Packaging/Guidelines

* Thu Jun 21 2007 Matt Anderson <mra@hp.com> - 0.2.2-2
- Merged in changes suggested by tibbs@math.uh.edu

* Wed Jun 20 2007 Matt Anderson <mra@hp.com> - 0.2.2-1
- Initial RPM packaging
