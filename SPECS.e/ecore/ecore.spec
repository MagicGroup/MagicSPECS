Name:           ecore
Version:	1.7.10
Release:        1%{?dist}
Summary:        Event/X abstraction layer
Summary(zh_CN.UTF-8): Event/X 抽象层
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://web.enlightenment.org/p.php?p=about/efl&l=en
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
BuildRequires:  eet-devel
BuildRequires:  evas-devel
BuildRequires:  libX11-devel libXext-devel libeina-devel
BuildRequires:  libXcursor-devel libXrender-devel libxcb-devel 
BuildRequires:  libXinerama-devel libXrandr-devel libXScrnSaver-devel 
BuildRequires:  libXcomposite-devel libXfixes-devel libXdamage-devel 
BuildRequires:  xorg-x11-proto-devel SDL-devel
BuildRequires:  openssl-devel libcurl-devel doxygen
BuildRequires:  c-ares-devel tslib-devel

%description
Ecore is the event/X abstraction layer that makes doing selections,
Xdnd, general X stuff, event loops, timeouts and idle handlers fast,
optimized, and convenient.

%description -l zh_CN.UTF-8
Event/X 抽象层。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release} 

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
%configure                                    \
           --disable-static                   \
           --enable-ecore-fb                  \
           --enable-ecore-evas-fb             \
           --enable-ecore-sdl                 \
           --disable-ecore-evas-directfb      \
           --disable-rpath --enable-openssl   \
           --disable-gnutls                   \
           --enable-doc                       \
           --enable-cares                     \
           --disable-xim                      \
           --enable-ecore-evas                \
           --enable-ecore-input-evas          \
           --enable-ecore-evas-software-x11

make %{?_smp_mflags} V=1
#cd doc; make doc %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
#chrpath --delete %{buildroot}%{_libdir}/lib%{name}_*.so*
#chrpath --delete %{buildroot}%{_libdir}/ecore/immodules/xim.so

find %{buildroot} -name '*.la' -delete
magic_rpm_clean.sh
%find_lang %{name}

# remove unfinished manpages
#find doc/man/man3 -size -100c -delete

#for l in todo %{name}.dox
#3do
# rm -f doc/man/man3/$l.3
#done 

#chmod -x doc/html/*

#mkdir -p %{buildroot}%{_mandir}/man3
#install -Dpm0644 doc/man/man3/* %{buildroot}%{_mandir}/man3

# rename generic and conflicting manpages
#mv %{buildroot}%{_mandir}/man3/Examples.3 %{buildroot}%{_mandir}/man3/ecore-Examples.3

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libecore_*.so.*
%{_libdir}/libecore.so.*
%{_libdir}/ecore

%files devel
#%doc doc/html/*
#%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Mar 26 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.9-1
- Update to 1.7.9

* Mon Sep 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-3
- Bump release for rawhide

* Mon Aug 19 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-2
- Bump release

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8
- Clean up spec file
- Clean up BRs

* Sat Aug 17 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.7.7-3
- tighten build deps to ensure ecore-evas component builds
- -devel drop explicit deps, automatic pkgconfig deps catch those already
- %%build: --disable-silent-rules

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.7-1
- update to 1.7.7 and enable ecore-evas-software-x11

* Sat Apr 20 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.6-1
- update to 1.7.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-2
- enable ecore-evas and ecore-input-evas. edje depends on these options

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- update to 1.7.4
- drop obsolete patch, disable and remove xim module for rpath

* Wed Aug  8 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-2
- rename generic and conflicting manpages

* Thu Aug  2 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> 1.0.1-2
- enable c-ares support

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> 1.0.1-1
- update to 1.0.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-1
- final 1.0.0 release

* Wed Dec 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta3
- beta 3 release

* Tue Nov 16 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta2
- beta 2 release

* Fri Nov 05 2010 Thomas Janssen <thomasj@fedoraproject.org> 1.0.0-0.1.beta1
- beta 1 release

* Fri Jul 02 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49898-1
- ecore 0.9.9.49898 snapshot release

* Fri Jun 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49539-1
- ecore 0.9.9.49539 snapshot release

* Mon Feb 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-1
- New upstream source 0.9.9.063

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.9.050-7
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.9.050-4
- rebuild with new openssl

* Wed Dec 17 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-3
- rebuilt

* Wed Dec 17 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-2
- Rebuilt

* Sat Nov 29 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-1
- New upstream snapshot

* Mon May 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.043-1
- New upstream snapshot
- Removed DirectFB backend, it's unmaintained upstream

* Wed May 14 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-4
- Added pkgconfig to buildrequires and ecore-devel requires

* Sun May 04 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-3
- Fixed ecore-devel dependencies once again

* Fri May 02 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-2
- Fixed ecore-devel dependencies
- Fixed timestamp of source tarball
- Preserve timestamps of installed files
- Added html docs

* Mon Apr 14 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-1
- Initial specfile for Ecore
