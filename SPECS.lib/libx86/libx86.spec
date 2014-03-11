Name:           libx86
Version:        1.1
Release:        12%{?dist}
Summary:        Library for making real-mode x86 calls

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.codon.org.uk/~mjg59/libx86
Source0:        http://www.codon.org.uk/~mjg59/libx86/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# does not build on ppc, ppc64 and s390* yet, due to the lack of port i/o
# redirection and video routing
ExcludeArch:    ppc ppc64 s390 s390x %{sparc}

Patch0: libx86-add-pkgconfig.patch
Patch1: libx86-mmap-offset.patch

%description
A library to provide support for making real-mode x86 calls with an emulated
x86 processor.

%package devel
Summary:        Development tools for programs which will use libx86
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the static library and header file necessary for
development of programs that will use libx86 to make real-mode x86 calls.

%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
CFLAGS="$RPM_OPT_FLAGS" make BACKEND=x86emu LIBDIR=%{_libdir} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir}
rm $RPM_BUILD_ROOT/%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYRIGHT
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/x86.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1-12
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.1-11
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 04 2009 Dennis Gilmore <dennis@ausil.us> - 1.1-9
- Exclude sparc arches

* Tue Oct 27 2009 Adam Jackson <ajax@redhat.com> 1.1-8
- libx86-mmap-offset.patch: Attempt to make selinux happy by not mmap'ing
  the zero page.

* Thu Sep 03 2009 Karsten Hopp <karsten@redhat.com> 1.1-7
- excludearch s390, s390x where we don't have sys/io.h

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.1-6
- add pkgconfig support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 20 2008 Matthew Garrett <mjg@redhat.com> 1.1-3
- Fix bizarre provides/obsoletes thinko 

* Tue May 20 2008 Matthew Garrett <mjg@redhat.com> 1.1-2
- Ensure RPM_OPT_FLAGS are passed. Patch from Till Maas.

* Mon May 19 2008 Matthew Garrett <mjg@redhat.com> 1.1-1
- Initial packaging of libx86
