
# Fedora Review: http://bugzilla.redhat.com/204954

Summary: 	Open Fingerprint Architecture library	
Summary(zh_CN.UTF-8): 音频的开放体系指纹库
Name:		libofa	
Version:	0.9.3	
Release:	21%{?dist}

License:	GPLv2
Url:		http://code.google.com/p/musicip-libofa/
Source0:	http://musicip-libofa.googlecode.com/files/libofa-%{version}.tar.gz	
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: libofa-0.9.3-gcc41.patch
# Use Libs.private
Patch2: libofa-0.9.3-pkgconfig.patch
Patch3: libofa-0.9.3-gcc44.patch
Patch4: libofa-0.9.3-curl.patch
Patch5: libofa-0.9.3-gcc47.patch

BuildRequires:	findutils
BuildRequires:	pkgconfig sed
BuildRequires:	fftw3-devel 
# these are used only in the examples.
BuildRequires:	curl-devel
BuildRequires:	expat-devel

%description
Currently, MusicDNS and the Open Fingerprint Architecture are being used to:
* identify duplicate tracks, even when the metadata is different, MusicIP
  identifies the master recording.
* fix metadata
* find out more about tracks by connecting to MusicBrainz

%description -l zh_CN.UTF-8
音频的开放体系指纹库。

%package devel
Summary: Development headers and libraries for %{name}	
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
# removed by patch2
#Requires: expat-devel fftw3-devel 
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

find . -name README -or -name \*.cpp -or -name \*.h | xargs --no-run-if-empty sed -i -e 's|\r||'  ||:

%patch1 -p1 -b .gcc41
%patch2 -p1 -b .pkgconfig
%patch3 -p1 -b .gcc43
%patch4 -p1 -b .curl
%patch5 -p1 -b .gcc47

## pkg-config < 0.20.0 (apparently?) doesn't grok URL
%if "%(pkg-config --version 2>/dev/null)" < "0.20.0"
#if 0%{?fedora} < 4 && 0%{?rhel} < 5
#if 0%{?rhel} == 4
sed -i -e "s|^URL:|#URL:|" *.pc.in ||:
%endif


%build
%configure --disable-static

make %{?smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

# prepare docs
make -C examples clean
rm -rf examples/.deps examples/Makefile examples/*.gcc43
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc AUTHORS README COPYING
%{_libdir}/libofa.so.0*

%files devel
%defattr(-,root,root,-)
%doc examples/
%{_includedir}/ofa1/
%{_libdir}/pkgconfig/libofa.pc
%{_libdir}/libofa.so


%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-20
- fix build against gcc47
- tighten %%files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Than Ngo <than@redhat.com> - 0.9.3-18
- fix build failure against curl >= 7.21

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-15
- update Url, Source
- gcc44 patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-13
- multiarch conflicts (#342271)
- tweak gcc43

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-12 
- gcc43 patch

* Sat Sep 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-11
- -devel: fix summary
- fix pkgconfig, URL-patching logic

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-10
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-9
- License: GPLv2

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-8
- better pkgconfig patch, using Libs.private

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-7
- fix rpmdoc handling

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-6
- de-DOS'ify .cpp, .h files too

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-5
- use sed instead of dos2unix
- omit examples/.deps

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-4
- remove extrenous entries from libofa.pc
- dos2unix README
- fix url in Source0
- -devel: %%doc examples/

* Mon Sep 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-3
- use gcc41 patch extracted from debian's patchset

* Mon Sep 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-2
- gcc41 patch

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-1
- first try
