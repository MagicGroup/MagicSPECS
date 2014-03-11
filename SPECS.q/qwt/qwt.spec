
Name:	 qwt
Summary: Qt Widgets for Technical Applications
Version: 5.2.2
Release: 3%{?dist}

License: LGPLv2 with exceptions
URL:     http://qwt.sourceforge.net
Group:   System Environment/Libraries
Source:  http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# add install-qt config to use system paths
# needs work to fix the doc install for non install-qt case
Patch50: qwt-5.2.2-install_qt.patch

BuildRequires: qt4-devel

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
The Qwt library contains GUI Components and utility classes which are primarily
useful for programs with a technical background.
Besides a 2D plot widget it provides scales, sliders, dials, compasses,
thermometers, wheels and knobs to control or display values, arrays
or ranges of type double.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
%description devel
%{summary}.

%package doc
Summary: Extra Developer documentation for %{name}
Group:   Documentation
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.



%prep
%setup -q

%patch50 -p1 -b .install_qt


%build
%{?_qt4_qmake} \
  CONFIG+=QwtSVGItem \
  CONFIG+=install-qt

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# fixup docs bogosity
mv $RPM_BUILD_ROOT%{_qt4_docdir}/html/html \
   $RPM_BUILD_ROOT%{_qt4_docdir}/html/qwt


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES
%doc COPYING
%doc README
%{_qt4_libdir}/libqwt.so.5*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*
%{_qt4_headerdir}/qwt/
%{_qt4_libdir}/libqwt.so
%{?_qt4_plugindir}/designer/libqwt_designer_plugin.so

%files doc
%defattr(-,root,root,-)
# own these to avoid needless dep on qt/qt-doc
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%{_qt4_docdir}/html/qwt/


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 5.2.2-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 07 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-1
- 5.2.2

* Thu Jul 14 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- .spec cosmetics
- use %%_qt4_ macros
- -doc subpkg here (instead of separately built)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 16 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.1-1
- update to 5.2.1 

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-1
- fix wrong lib names

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-0
- update to 5.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-2
 - modify path patch

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-1
 -update to 5.1.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.2-6
- Autorebuild for GCC 4.3

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-5
 - add EPEL support

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-4
- remove parallel build, because it will fail sometimes

* Fri Sep 28 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-3
- fix some errors in the spec file

* Fri Jul 06 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-2
- fix some errors in the spec file

* Mon Jun 11 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-1
- update to 5.0.2
- split doc

* Thu May 15 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.1-1
 - start

