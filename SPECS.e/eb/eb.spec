Name:           eb
Version:        4.4.3
Release:        1%{?dist}
Summary:        Library for accessing Japanese CD-ROM electronic books
Summary(ja):    CD-ROM 書籍にアクセスするためのライブラリ

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.sra.co.jp/people/m-kasahr/eb/
Source0:        ftp://ftp.sra.co.jp/pub/misc/eb/%{name}-%{version}.tar.bz2
Patch1:         eb-aclocal-conf-libdir.patch

BuildRequires:  zlib-devel
%ifarch aarch64
BuildRequires:	autoconf
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
EB Library is a C library for accessing CD-ROM books.  
EB Library supports to access CD-ROM books of 
EB, EBG, EBXA, EBXA-C, S-EBXA and EPWING formats.  

%description -l ja
EB ライブラリは CD-ROM 書籍にアクセスするための C のライブラリです。
EB, EBG, EBXA, EBXA-C, S-EBXA および EPWING 形式の 
CD-ROM 書籍に対応しています。


%package devel
Summary:        Development files for eb
Group:          Development/Libraries
Requires:       eb = %{version}
Requires:       zlib-devel

%description devel
This package contains development files needs to use eb in programs.


%prep
%setup -q
%patch1 -p1 -b .1-etc~


%build
%ifarch aarch64
autoconf
%endif
%configure --disable-static --sysconfdir=%{_libdir}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libeb.la

rm -rf tmp
mkdir -p tmp
mv $RPM_BUILD_ROOT%{_datadir}/eb/doc tmp/html

%find_lang %{name}
%find_lang %{name}utils
cat %{name}utils.lang >> %{name}.lang


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/*
%{_libdir}/libeb.so.*
%{_datadir}/eb


%files devel
%doc tmp/html
%{_includedir}/eb
%{_libdir}/eb.conf
%{_libdir}/libeb.so
%{_datadir}/aclocal/*


%changelog
* Mon Sep  2 2013 Jens Petersen <petersen@redhat.com> - 4.4.3-1
- update to 4.4.3

* Mon Sep  2 2013 Jens Petersen <petersen@redhat.com> - 4.4.1-9
- run autoconf for aarch64 (#926499)
- cleanup buildroot and defattr lines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.4.1-7
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-3
- Rebuilt for glibc bug#747377

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 31 2009 Jens Petersen <petersen@redhat.com> - 4.4.1-1
- update to 4.4.1 (Mamoru Tasaka, #518072)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 14 2008 Jens Petersen <petersen@redhat.com> - 4.3.2-1
- update to 4.3.2

* Wed Feb 14 2007 Jens Petersen <petersen@redhat.com> - 4.3-2
- eb-devel requires zlib-devel (#228243)
- move eb.conf build config file to eb-devel and libdir
- add eb-aclocal-conf-libdir.patch to update eb.conf location

* Mon Feb 12 2007 Jens Petersen <petersen@redhat.com> - 4.3-1
- initial packaging for Fedora (#228241)
