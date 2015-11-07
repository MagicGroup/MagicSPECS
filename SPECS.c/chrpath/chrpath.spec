Summary: Modify rpath of compiled programs
Summary(zh_CN.UTF-8): 修改 rpath 以编译程序
Name: chrpath
Version: 0.13
Release: 11%{?dist}
License: GPL+
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
URL: ftp://ftp.hungry.com/pub/hungry/chrpath/
Patch0: chrpath-0.13-NULL-entry.patch
Source0: ftp://ftp.hungry.com/pub/hungry/chrpath/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
chrpath allows you to modify the dynamic library load path (rpath) of
compiled programs.  Currently, only removing and modifying the rpath
is supported.

%description -l zh_CN.UTF-8
chrpath 允许你修改编译程序动态库的载入路径 (rpath) 。
当前，它只支持移除和修改 rpath。

%prep
%setup -q
%patch0 -p1 -b .NULL

%build
%configure
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/usr/doc

magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS ChangeLog*
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.13-11
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.13-10
- 为 Magic 3.0 重建

* Wed Jul 25 2012 Liu Di <liudidi@gmail.com> - 0.13-9
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.13-5
- Fix last entry in .dynamic (by Christian Krause <chkr@plauener.de>).

* Sat Sep  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.13-2
- License: GPL+

* Sun Mar 12 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.13-1
- Initial build.

