Name:		libgcroots
Version:	0.2.3
Release:	7%{?dist}
License:	MIT
URL:		http://code.google.com/p/sigscheme/wiki/libgcroots

Source0:	http://sigscheme.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:		%{name}-aarch64.patch


Summary:	Roots acquisition library for Garbage Collector
Summary(zh_CN.UTF-8): 垃圾回收的根采集库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description
libgcroots abstracts architecture-dependent part of garbage collector
roots acquisition such as register windows of SPARC and register stack
backing store of IA-64.
This library encourages to have own GC such as for small-footprint,
some application-specific optimizations, just learning or to test
experimental ideas.

%description -l zh_CN.UTF-8
垃圾回收的根采集库。

%package devel
Summary:	Development files for libgcroots
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
libgcroots abstracts architecture-dependent part of garbage collector
roots acquisition such as register windows of SPARC and register stack
backing store of IA-64.

This package contains a header file and development library to help you
to develop any own GC.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .0-aarch64

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove unnecessary files
rmdir $RPM_BUILD_ROOT%{_includedir}/libgcroots
rm $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING ChangeLog README
%{_libdir}/libgcroots.so.*

%files devel
%doc COPYING ChangeLog README
%{_includedir}/gcroots.h
%{_libdir}/libgcroots.so
%{_libdir}/pkgconfig/gcroots.pc

%changelog
* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 0.2.3-7
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Akira TAGOH <tagoh@redhat.com> - 0.2.3-5
- Rebuilt for aarch64 support (#925735)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 12 2011 Akira TAGOH <tagoh@redhat.com> - 0.2.3-1
- New upstream release. (#695292)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Akira TAGOH <tagoh@redhat.com> - 0.2.2-1
- New upstream release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Akira TAGOH <tagoh@redhat.com> - 0.2.1-3
- Get rid of explicit dependency of ldconfig.
- Correct License.

* Wed Feb 27 2008 Akira TAGOH <tagoh@redhat.com> - 0.2.1-2
- Add the appropriate requires.

* Thu Feb 21 2008 Akira TAGOH <tagoh@redhat.com> - 0.2.1-1
- Initial packaging.

