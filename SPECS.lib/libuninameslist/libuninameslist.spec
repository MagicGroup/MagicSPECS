Name:           libuninameslist
Version:        20091231
Release:        7%{?dist}

Summary:        A library providing Unicode character names and annotations
Summary(zh_CN.UTF-8): 提供 Unicode 字符名称和说明的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        BSD
URL:            http://libuninameslist.sourceforge.net
Source0:        http://downloads.sourceforge.net/libuninameslist/libuninameslist-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libuninameslist provides applications with access to Unicode name and
annotation data from the official Unicode Character Database.

%description -l zh_CN.UTF-8
提供 Unicode 字符名称和说明的库，数据从官方 Unicode 字符数据库中获得。

%package        devel
Summary:        Header files and static libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and static libraries for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libuninameslist


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall incdir=$RPM_BUILD_ROOT%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 20091231-7
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 20091231-6
- 为 Magic 3.0 重建

* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 20091231-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 20091231-4
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 20091231-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 16 2010 Kevin Fenzi <kevin@tummy.com> - 20091231-1
- Update to 20091231
- Do not ship static libs - bug #556078

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080409-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080409-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Roozbeh Pournader <roozbeh@gmail.com> - 20080409-1
- Update to upstream 20080409: Unicode 5.1 support
- Change package versioning scheme
- Update summary and description
- Add DistTag
- Remove copy of GPL from RPM: the only file it applies to is not shipped

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.0-8.20060907
- Rebuild for gcc43

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.0-7.20060907
- Rebuild for BuildID

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.0-6.20060907
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Kevin Fenzi <kevin@tummy.com> - 0.0-5.20060907
- Take over maintainership. 
- Update to 20060907

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.0-4.040707
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040707
- Updated to 040707.

* Fri Jul  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040701
- Updated to 040701.

* Mon Oct 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.0-0.fdr.2.030713
- Enable static libs, add -devel subpackage.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.030713
- Initial RPM release.
