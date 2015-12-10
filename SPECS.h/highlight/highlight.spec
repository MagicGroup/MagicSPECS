Name:           highlight
Summary:        Universal source code to formatted text converter
Summary(zh_CN.UTF-8): 通用源代码格式文本转换器

Version:	3.23
Release:        3%{?dist}

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv3

URL:            http://www.andre-simon.de/
Source0:        http://www.andre-simon.de/zip/%{name}-%{version}.tar.bz2

BuildRequires:  qt4-devel >= 4.4
BuildRequires:  lua-devel, boost-devel
BuildRequires:  desktop-file-utils

%{?filter_setup:
%filter_from_provides /^perl(/d;
%filter_from_requires /^perl(/d;
%filter_setup
}

%description
A utility that converts sourcecode to HTML, XHTML, RTF, LaTeX, TeX,
XSL-FO, XML or ANSI escape sequences with syntax highlighting.
It supports several programming and markup languages.
Language descriptions are configurable and support regular expressions.
The utility offers indentation and reformatting capabilities.
It is easily possible to create new language definitions and colour themes.

%description -l zh_CN.UTF-8
把源代码转成带有语法高亮的格式化文本，支持 HTML, XHTML, RTF, LaTeX, Tex,
XSL-FO, XML 和 ANSI序列。

%package gui
Summary:        GUI for the hihghlight source code formatter
Summary(zh_CN.UTF-8): %{name} 的图形界面
Requires:       %{name} = %{version}-%{release}

%description gui
A Qt-based GUI for the highlight source code formatter source.

%description gui -l zh_CN.UTF-8 
基于 Qt 的 %{name} 的图形界面。

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=
rm -rf src/gui-qt/moc*
make gui %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"  \
                         QMAKE="qmake-qt4" \
                         LDFLAGS=

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps

make install-gui DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/

desktop-file-install \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
   highlight.desktop

%files
%defattr(-,root,root,-)
%{_bindir}/highlight
%{_datadir}/highlight/
%{_mandir}/man1/highlight.1*

%config(noreplace) %{_sysconfdir}/highlight/

%doc ChangeLog AUTHORS README* COPYING TODO examples/

%files gui
%defattr(-,root,root,-)
%{_bindir}/highlight-gui
%{_datadir}/applications/highlight.desktop
%{_datadir}/pixmaps/highlight.xpm

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.23-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.23-2
- 更新到 3.23

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 3.18-1
- 更新到 3.18

* Tue Feb 19 2013 Jochen Schmitt <Jochen herr-schmitt de> - 3.13-1
- New upstream release
- Clean up sPEC file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct  7 2012 Jochen Schmitt <Jochen herr-schmitt de> - 3.12-1
- New upstream release

* Thu Sep  6 2012 Jochen Schmitt <Jochen herr-schmitt de> - 3.11-0.1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.9-1
- New upstream release

* Thu Mar  8 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.8-1
- New upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-2
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Jochen Schmitt <Jochen herr-schmitt de> 3.7-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.6-1
- New upstream release

* Wed Jun  8 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.5-1
- New upstream release

* Thu Mar 31 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.4-1
- New upstream release

* Sun Mar 20 2011 Jochen Schmitt <Jochen herr-schmitt de> 3.3-5
- Migrating Req./Prov. filterering to filter rpm macros

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.3-1
- New upstream release

* Tue Nov 16 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.2-1
- New upstream release

* Tue Sep  7 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-2
- Add epoche for qt-devel BR (#631442)

* Mon Aug 30 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-1
- New upstream release

* Sun Aug 15 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.3
- New upstream release

* Thu Jul 15 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.2
- New upstream release

* Sat Jun 26 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.1-0.1
- New upstream release

* Sat Jun 12 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.0-0.2
- Exclude all perl related req. caused by the examples

* Thu Jun 10 2010 Jochen Schmitt <Jochen herr-schmitt de> 3.0-0.1
- New upstream release (beta)

* Mon Apr  5 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.16-1
- New upstream release

* Sun Mar 14 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.15-2
- Add StartupNotify=true into desktop file

* Mon Mar  1 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.15-1
- New upstream release

* Thu Jan 28 2010 Jochen Schmitt <Jochen herr-schmitt de> 2.14-1
- New upstream release

* Wed Oct 14 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.13-1
- New upstream release

* Thu Sep 10 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.12-1
- New upstream release

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> 2.10-4
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.10-2
- License was changed go GPLv3 from upstream

* Mon Jun 29 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.10-1
- New upstream release

* Tue May 12 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.9-1
- New upstream release

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.8-3
- Adding GUI subpackage

* Mon Apr 20 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.8-1
- New upstream release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.7-2
- Patches for gcc-4.4

* Thu Jan 15 2009 Jochen Schmitt <Jochen herr-schmitt de> 2.7-1
- New upstream release

* Mon Nov  3 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.14-1
- New upstream release

* Tue Oct 14 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.13-2
- Fix SMP build issue

* Wed Oct  8 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.13-1
- New upstream release

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.12-2
- don't package broken examples, causes bogus perl provides/requires
- don't claim to Provide: perl(highlight_pipe)
- don't claim to Requires: perl(IPC::Open3)

* Mon Aug 18 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.12-1
- New upstream release
- Fix for gcc-4.3 issue on highlight-2.6.13

* Thu Jul 17 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.11-1
- New upstream release

* Mon May 12 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.10-1
- New upstream release

* Mon Mar 31 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.9-2
- New upstream release

* Sun Feb 10 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.8-1
- New upstream release

* Mon Jan 21 2008 Jochen Schmitt <Jochen herr-schmitt de> 2.6.7-2
- New upstream release
- Fix gcc-4.3 issues

* Tue Dec 11 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.6-1
- New upstream release

* Mon Oct 29 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.5-1
- New upstream release

* Sun Sep 16 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.4-1
- New upstream release

* Tue Sep 11 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.3-1
- New upstream release

* Thu Aug  9 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.2-1
- New upstream release

* Wed Aug  8 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.1-2
- Changing license tag

* Tue Jul 10 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.6.1-1
- New upstream release

* Tue Feb  6 2007 Jochen Schmitt <Jochen herr-schmitt de> 2.4.8-2
- fir rpmopt bug (#227292)

* Mon Oct 23 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.8-1
- New upstream release

* Sun Sep  3 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.7-2
- Rebuilt for FC-6

* Tue Jul  4 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.7-1
- New upstream release

* Wed Mar 22 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.5-2
- New upstream relase
- Add gcc41 patch

* Wed Mar 15 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.4-2
- Add fixcodegen patch from Eric Hopper #184245

* Sun Mar 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.4-1
- New upstream release
- Adapt rpmopt patch to new upstream release

* Sun Feb 12 2006 Jochen Schmitt <Jochen herr-schmitt de> 2.4.3-2
- Rebuilt for FC5

* Tue Nov  1 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.3-1
- New upstream release

* Tue Oct 11 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-3
- Fix typo in highlight-2.4-rpmoptflags.patch

* Mon Oct 10 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-2
- Use -DUSE_FN_MATCH

* Sun Oct  9 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.2-1
- New upstream release

* Wed Aug 10 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-6
- Rebuilt for FC-4/FC-3

* Tue Aug  9 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4-1-5
- Fix #165302

* Mon Aug  8 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-4
- Move extension.conf and scriptre.conf to /etc/highlight

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-3
- Remove leading 'A' from summary line

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-2
- Add rpmoptflags patch from Tom Callaway

* Wed Aug  3 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4.1-1
- Change versioning schema
- Add suggested changes from Oliver

* Sun Jul 24 2005 Jochen Schmitt <Jochen herr-schmitt de> 2.4-1
- Initial build

