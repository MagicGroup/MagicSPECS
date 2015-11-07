Summary:    Extensible Binary Meta Language library
Summary(zh_CN.UTF-8): 可扩展二进制元语言库
Name:       libebml
Version: 1.3.3
Release:    2%{?dist}
License:    LGPLv2+
Group:      System Environment/Libraries
URL:        http://www.matroska.org/
Source:     http://dl.matroska.org/downloads/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
Extensible Binary Meta Language access library A library for reading
and writing files with the Extensible Binary Meta Language, a binary
pendant to XML.

%description -l zh_CN.UTF-8
可扩展二进制元语言库。

%package    devel
Summary:    Development files for the Extensible Binary Meta Language library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name} = %{version}-%{release}

%description devel
Extensible Binary Meta Language access library A library for reading
and writing files with the Extensible Binary Meta Language, a binary
pendant to XML.

This package contains the files required to rebuild applications which
will use the Extensible Binary Meta Language library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
sed -i 's/\r//' ChangeLog LICENSE.LGPL
iconv -f ISO-8859-1 -t UTF-8 ChangeLog > ChangeLog.tmp
touch -r ChangeLog ChangeLog.tmp
mv ChangeLog.tmp ChangeLog


%build
CXXFLAGS="$RPM_OPT_FLAGS" make -C make/linux %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make -C make/linux \
  prefix=$RPM_BUILD_ROOT%{_prefix} \
  libdir=$RPM_BUILD_ROOT%{_libdir} \
  INSTALL="install -p" \
  install
rm $RPM_BUILD_ROOT%{_libdir}/%{name}.a
# Needed for proper stripping of the library (still in 0.7.6)
chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}.so.*
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,0755)
%doc ChangeLog LICENSE.LGPL
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/ebml/
%{_libdir}/%{name}.so


%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.3.3-2
- 更新到 1.3.3

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 1.3.0-1
- 更新到 1.3.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Sun Nov 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Mon Feb 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- New upstream release 1.2.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 18 2010 Hans de Goede <hdegoede@redhat.com> 1.0.0-1
- New upstream release 1.0.0 (#605571)

* Tue May 25 2010 Hans de Goede <hdegoede@redhat.com> 0.8.0-1
- New upstream release 0.8.0 (#595421)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.8-1
- New upstream release 0.7.8

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.7-5
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.7-4
- Fix building with gcc 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.7-3
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.7-2
- Taking over as maintainer since Anvil has other priorities
- Drop static lib from -devel package
- FE6 Rebuild

* Wed Apr 12 2006 Dams <anvil[AT]livna.org> - 0.7.7-1
- Updated to 0.7.7

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 0.7.6-2.fc5
- Release bump

* Tue Nov 29 2005 Matthias Saou <http://freshrpms.net/> 0.7.6-1
- Update to 0.7.6.
- Change URL to the project's one.
- Add a full description for the devel package.
- Some other minor spec file changes.

* Sun Jun  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.5-2
- Split development files into a devel subpackage.
- Run ldconfig at post (un)install time.
- Fix shared library file modes.

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.7.5-1
- update to 0.7.5 (fixes x86_64 build)
- incldue shared libs

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.7.3-3
- rebuild on all arches

* Sun Feb 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.3-2
- 0.7.3.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 0.7.2-2
- Update to 0.7.2.
- Bump release to provide Extras upgrade path.

* Sun Aug 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.1
- Update to 0.7.1.
- Honor $RPM_OPT_FLAGS.

* Mon Jul 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Improved 64-bit arch build fix.

* Wed May  19 2004 Justin M. Forbes <64bit_fedora@comcast.net> 0:0.6.5-0.fdr.2
- Change linux makefile to use lib64 ifarch x86_64 for sane build

* Sun Apr  4 2004 Dams <anvil[AT]livna.org> 0:0.6.5-0.fdr.1
- Updated to 0.6.5

* Sun Feb 29 2004 Dams <anvil[AT]livna.org> 0:0.6.4-0.fdr.2
- Added licenses file as doc

* Thu Sep  4 2003 Dams <anvil[AT]livna.org>
- Initial build.


