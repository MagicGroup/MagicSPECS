%define real_name libdvbpsi

Summary: 	Library for MPEG TS and DVB PSI tables decoding and generation
Summary(zh_CN.UTF-8): MPEG TS 和 DVB PSI 表解码和生成库
Name: 		libdvbpsi
Version:	1.3.0
Release: 	3%{?dist}
License: 	GPLv2+
Group: 		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: 		http://www.videolan.org/developers/libdvbpsi.html
Source0: 	http://download.videolan.org/pub/libdvbpsi/%{version}/%{real_name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	graphviz doxygen

%package devel
Summary: 	Development package for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: 		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: 	%{name} = %{version}-%{release}

# -----------------------------------------------------------------------------

%description
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.

%description -l zh_CN.UTF-8
MPEG TS 和 DVB PSI 表解码和生成库。

%description devel
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.
This package contains development files for %{name}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{real_name}-%{version}

# -----------------------------------------------------------------------------

%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}
make doc

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
magic_rpm_clean.sh

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html
%{_includedir}/dvbpsi/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libdvbpsi.pc

# -----------------------------------------------------------------------------

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 1.3.0-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 更新到 1.3.0

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.2.0-1
- 更新到 1.2.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1.6-7
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Liu Di <liudidi@gmail.com> - 0.1.6-6
- 为 Magic 3.0 重建

* Sun Apr  5 2009 kwizart < kwizart at gmail.com > - 0.1.6-5
- Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.1.6-4
- rebuild for new F11 features

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.6-3
- rebuild

* Tue Feb 26 2008 kwizart < kwizart at gmail.com > - 0.1.6-2
- Rebuild for gcc43

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 0.1.6-1
- Update to 0.1.6

* Sun Oct 14 2007 kwizart < kwizart at gmail.com > - 0.1.5-3
- Rpmfusion Merge Review

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.1.5-2
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Jul 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.5-0.lvn.1
- 0.1.5.
- Build with dependency tracking disabled.
- Miscellaneous specfile cleanups.

* Mon May 17 2004 Dams <anvil[AT]livna.org> - 0:0.1.3-0.lvn.4
- Added url in Source0

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.3
- Removed comment after scriptlets

* Mon Aug 18 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.2
- Moved some doc to devel package

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.1
- Added post/postun scriptlets
- Using RPM_OPT_FLAGS
- Updated to 0.1.3

* Sun Jun 29 2003 Dams <anvil[AT]livna.org> 
- Initial build.
