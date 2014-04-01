Name:           color-filesystem
Version:        1
Release:        11%{?dist}
Summary:        Color filesystem layout
Summary(zh_CN.UTF-8): Color 文件系统

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        Public Domain
BuildArch:      noarch

Requires:  filesystem
Requires:  rpm       

%description
This package provides some directories that are required/used to store color. 

%description -l zh_CN.UTF-8
这个提供了存储 color 需要使用的一些目录。

%prep
# Nothing to prep

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/icc
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/cmms
mkdir -p $RPM_BUILD_ROOT%{_datadir}/color/settings
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/color/icc

# rpm macros
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
cat >$RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.color<<EOF
%%_colordir %%_datadir/color
%%_syscolordir %%_colordir
%%_icccolordir %%_colordir/icc
%%_cmmscolordir %%_colordir/cmms
%%_settingscolordir %%_colordir/settings
EOF

%files
%defattr(-,root,root,-)
%dir %{_datadir}/color
%dir %{_datadir}/color/icc
%dir %{_datadir}/color/cmms
%dir %{_datadir}/color/settings
%dir %{_localstatedir}/lib/color
%dir %{_localstatedir}/lib/color/icc
%config %{_sysconfdir}/rpm/macros.color

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Richard Hughes <richard@hughsie.com> - 1-7
- Add the user-writable system-wide per-machine ICC profile directory from
  the new version of the OpenIccDirectoryProposal.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar  7 2008 kwizart < kwizart at gmail.com > - 1-4
- Bump

* Fri Mar  7 2008 kwizart < kwizart at gmail.com > - 1-3
- bump

* Tue Mar  4 2008 kwizart < kwizart at gmail.com > - 1-2
- Add settings color dir

* Sat Feb  2 2008 kwizart < kwizart at gmail.com > - 1-1
- Initial package.

