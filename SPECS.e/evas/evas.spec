Name:           evas
Version:	1.7.10
Release:        1%{?dist}
Summary:        Hardware-accelerated state-aware canvas API
Summary(zh_CN.UTF-8): 支持硬件加速和状态感知的画布 API
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://web.enlightenment.org/p.php?p=about/efl&l=en
Source0:        http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2

BuildRequires:  chrpath
BuildRequires:  eet-devel 
BuildRequires:  libeina-devel
BuildRequires:  freetype-devel libX11-devel libXext-devel
BuildRequires:  libXrender-devel fontconfig-devel libjpeg-devel libpng-devel
BuildRequires:  librsvg2-devel libtiff-devel giflib-devel fribidi-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel doxygen

%description
Evas is a clean display canvas API for several target display systems
that can draw anti-aliased text, smooth super and sub-sampled scaled
images, alpha-blend objects and much more.

%description -l zh_CN.UTF-8
支持硬件加速和状态感知的画布 API。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       pkgconfig 
Requires:       libX11-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static -enable-fb
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
cd doc; make doc %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
chrpath --delete %{buildroot}%{_libdir}/%{name}/modules/*/*/*/*.so
# chrpath --delete %%{buildroot}%%{_bindir}/evas*
# chrpath --delete %%{buildroot}%%{_libdir}/libevas-ver-svn*
find %{buildroot} -name '*.la' -delete

# remove unfinished manpages
find doc/man/man3 -size -100c -delete

for l in todo %{name}.dox
do
 rm -f doc/man/man3/$l.3
done 

chmod -x doc/html/*

mkdir -p %{buildroot}%{_mandir}/man3
install -Dpm0644 doc/man/man3/* %{buildroot}%{_mandir}/man3
mv %{buildroot}%{_mandir}/man3/authors.3 %{buildroot}%{_mandir}/man3/%{name}-authors.3
mv %{buildroot}%{_mandir}/man3/deprecated.3 %{buildroot}%{_mandir}/man3/%{name}-deprecated.3
mv %{buildroot}%{_mandir}/man3/Examples.3 %{buildroot}%{_mandir}/man3/%{name}-Examples.3
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/*.so.*
%{_libdir}/%{name}
%{_bindir}/%{name}*
%{_datadir}/%{name}
%{_libexecdir}/dummy_slave
%{_libexecdir}/evas_cserve2
%{_libexecdir}/evas_cserve2_slave

%files devel
%doc doc/html/*
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Mar 28 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Mon Sep 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Bump release version for rawhide

* Sat Aug 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8
- Tighten BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun  4 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.7-1
- update to 1.7.7

* Fri Apr 19 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.6.1-1
- update to 1.7.6.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.7.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1
- update to 1.7.4

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.2.1-3
- rebuild against new libjpeg

* Wed Aug  8 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-2
- rename "Examples.3" to something non-conflicting

* Thu Aug  2 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.0-2
- rename authors.3 and deprecated.3 manpages to avoid conflict

* Mon May  7 2012 Tom Callaway <spot@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.1-2
- Rebuild for new libpng

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.1-1
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
- evas 0.9.9.49898 snapshot release

* Fri Jun 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.49539-1
- evas 0.9.9.49539 snapshot release

* Wed Apr 07 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-2
- Testbuild for emotion

* Mon Feb 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.9.9.063-1
- New upstream source 0.9.9.063

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.050-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.050-1
- New upstream snapshot

* Fri Aug 29 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.043-2
- Fix unowned /usr/lib/evas

* Mon May 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.043-1
- New upstream snapshot
- Removed DirectFB backend, it's unmaintained upstream

* Fri May 02 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-3
- Fixed documentation for multilib

* Sat Apr 19 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-2
- Fixed timestamp of source tarball
- Preserve timestamps of installed files
- Beautified summary
- Added html docs
- Added missing dependencies for evas-devel

* Mon Apr 14 2008 Pavel "Stalwart" Shevchuk <stlwrt@gmail.com> - 0.9.9.042-1
- Initial specfile for Evas
