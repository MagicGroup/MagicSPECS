Name:		mftrace
Version:	1.2.18
Release:	3%{?dist}
Summary:	Utility for converting TeX bitmap fonts to Type 1 or TrueType fonts
Summary(zh_CN.UTF-8): 转换 TeX 位图字体到 Type1 或 TrueType 字体的工具

Group:		Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
License:	GPLv2
URL:		http://lilypond.org/mftrace/
Source0:	http://lilypond.org/download/sources/mftrace/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python autotrace
Requires:	autotrace fontforge t1utils texlive-collection-fontsrecommended

%description
mftrace is a small Python program that lets you trace a TeX bitmap
font into a PFA or PFB font (A PostScript Type1 Scalable Font) or TTF
(TrueType) font.

Scalable fonts offer many advantages over bitmaps, as they allow
documents to render correctly at many printer resolutions. Moreover,
Ghostscript can generate much better PDF, if given scalable PostScript
fonts.

%description -l zh_CN.UTF-8
这是一个小 Python 程序，可以让你转换 TeX 位图字体到 PFA、PFB 或 TTF 字体。

%prep
%setup -q
sed -i -e "s/-Wall -O2/$RPM_OPT_FLAGS/" GNUmakefile.in


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt ChangeLog
%{_bindir}/*
%{_mandir}/man1/%{name}*
%{_datadir}/%{name}


%changelog
* Thu Aug 28 2014 Liu Di <liudidi@gmail.com> - 1.2.18-3
- 为 Magic 3.0 重建

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Jon Ciesla <limburgher@gmail.com> - 1.2.18-1
- Latest upstream, fixed tex requires.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.15-5
- recompiling .py files against Python 2.7 (rhbz#623337)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.15-2
- Rebuild for Python 2.6

* Wed Aug 27 2008 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.15-1
- Update to new release.

* Fri Aug  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.14-5
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.14-4
- Autorebuild for GCC 4.3

* Fri Jan  4 2008 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.14-3
- Change tetex-fonts dependency to texlive-fonts.

* Wed Aug 22 2007 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.14-2
- Rebuild.

* Mon Jul 30 2007 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.14-1
- New release.
- Update URLs.

* Mon Nov  6 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.5-1
- New release.

* Mon Aug 28 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.4-4
- Rebuild for FC6.

* Sat May 20 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.4-2
- Make sure $RPM_OPT_FLAGS are used

* Sat May 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.2.4-1
- New upstream release.

* Tue Apr 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.1.19-3
- Update description

* Tue Apr 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.1.19-2
- ghost .pyo files

* Thu Mar 30 2006 Quentin Spencer <qspencer@users.sourceforge.net> 1.1.19-1
- First version.
