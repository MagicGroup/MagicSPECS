Summary: A documentation system for C/C++
Summary(zh_CN.UTF-8): C/C++ 的文档系统
Name:    doxygen
Epoch:   1
Version: 1.8.10
Release: 3%{?dist}

# No version is specified.
License: GPL+
Url: http://www.stack.nl/~dimitri/doxygen/index.html
Source0: ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
# this icon is part of kdesdk
Source1: doxywizard.png
Source2: doxywizard.desktop

Patch1: doxygen-1.8.10-install.patch

# upstream fixes
Patch100: doxygen-1.8.10-drop-qt-arch-x86-64-definition.patch
Patch101: doxygen-1.8.10-angle-bracket.patch
Patch102: doxygen-1.8.10-SOURCE_DATE_EPOCH.patch
Patch103: doxygen-1.8.10-bibtex.patch
Patch104: doxygen-1.8.10-fixspace.patch
Patch105: doxygen-1.8.10-xml.patch
Patch106: doxygen-1.8.10-latex.patch
Patch107: doxygen-1.8.10-timestamp-latex.patch

BuildRequires: perl
BuildRequires: tex(dvips)
BuildRequires: tex(latex)
# arg, no safe/virtual provides for these
BuildRequires: /usr/bin/epstopdf
# Work around strange dependences in epstopdf packages (RHBZ#991699)
BuildRequires: texlive-epstopdf
BuildRequires: ghostscript
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: desktop-file-utils

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%description -l zh_CN.UTF-8
Doxygen 可以从带有注释的源文件中生成在线类浏览器（使用 HTML）和/或
参考手册（使用 LaTeX）。文档是直接从源码中抽取的。也可以从无注释的
源码中生成代码结构。

%package doxywizard
Summary: A GUI for creating and editing configuration files
Summary(zh_CN.UTF-8): 建立和编辑配置文件的界面
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildRequires: qt4-devel
%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.

%description doxywizard -l zh_CN.UTF-8
建立和编辑 doxygen 配置文件的图形界面。

%package latex
Summary: Support for producing latex/pdf output from doxygen
Summary(zh_CN.UTF-8): 从 doxygen 生成 latex/pdf 文件的支持
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tex(latex)
Requires: tex(multirow.sty)
Requires: tex(sectsty.sty)
Requires: tex(tocloft.sty)
Requires: tex(xtab.sty)
Requires: texlive-epstopdf-bin
%description latex
%{summary}.

%description latex -l zh_CN.UTF-8
从 doxygen 生成 latex/pdf 文件的支持。

%prep
%setup -q

%patch1 -p1 -b .config
%patch100 -p1
%patch101 -p1 -b .angle-bracket
%patch102 -p1 -b .SOURCE_DATE_EPOCH
%patch103 -p1 -b .bibtex
%patch104 -p1 -b .fixspace
%patch105 -p1 -b .xml
%patch106 -p1 -b .latex
%patch107 -p1 -b .latex-timestamps

# convert into utf-8
iconv --from=ISO-8859-1 --to=UTF-8 LANGUAGE.HOWTO > LANGUAGE.HOWTO.new
touch -r LANGUAGE.HOWTO LANGUAGE.HOWTO.new
mv LANGUAGE.HOWTO.new LANGUAGE.HOWT


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
		-Dbuild_doc=ON \
		-Dbuild_wizard=ON \
		-Dbuild_xmlparser=ON \
		-DMAN_INSTALL_DIR=%{_mandir}/man1 \
		-DDOC_INSTALL_DIR=%{_docdir}/doxygen \
		-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
		-DBUILD_SHARED_LIBS=OFF \
		..
popd

make %{?_smp_mflags} -C %{_target_platform}
make docs -C %{_target_platform}


%install
make install \
	DESTDIR=%{buildroot} \
	-C %{_target_platform}

mv %{buildroot}%{_docdir}/doxygen .

install -m644 -p -D %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/doxywizard.png

desktop-file-install \
   --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}

%files
%doc LANGUAGE.HOWTO README.md doxygen
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*
%{_mandir}/man1/doxyindexer.1.gz
%{_mandir}/man1/doxysearch.1.gz

%files doxywizard
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*
%{_datadir}/applications/doxywizard.desktop
%{_datadir}/pixmaps/doxywizard.png

%files latex
# intentionally left blank

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1:1.8.10-3
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1:1.8.10-2
- 更新到 1.8.10

* Thu Dec 26 2013 Orion Poplawski <orion@cora.nwra.com> - 1:1.8.6-1
- 1.8.6

* Tue Oct 08 2013 Than Ngo <than@redhat.com> - 1:1.8.5-2
- add exlive-epstopdf-bin in requirement

* Mon Aug 26 2013 Than Ngo <than@redhat.com> - 1:1.8.5-1
- 1.8.5

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> - 1:1.8.4-4
- Work around strange dependencies in epstopdf packages (#991699)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Than Ngo <than@redhat.com> - 1:1.8.4-2
- backport upstream patch to fix endless loop

* Tue May 21 2013 Than Ngo <than@redhat.com> - 1:1.8.4-1
- 1.8.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Than Ngo <than@redhat.com> - 1.8.3.1-1
- 1.8.3.1
- fedora/rhel condition

* Tue Jan 08 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:1.8.3-3
- -latex subpkg (#892288)
- .spec cleanup

* Thu Jan 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:1.8.3-2
- doxygen is missing dependencies for texlive update (#891452)
- doxywizard: tighten dep on main pkg

* Wed Jan 02 2013 Than Ngo <than@redhat.com> - 1:1.8.3-1
- 1.8.3

* Mon Aug 13 2012 Than Ngo <than@redhat.com> - 1:1.8.2-1
- 1.8.2

* Mon Jul 30 2012 Than Ngo <than@redhat.com> - 1:1.8.1.2-1
- 1.8.1.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Than Ngo <than@redhat.com> - 1:1.8.1.1-3
- bz#832525, fix multilib issue

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1:1.8.1.1-2
- make HTML_TIMESTAMP default FALSE

* Mon Jun 11 2012 Than Ngo <than@redhat.com> - 1:1.8.1.1-1
- 1.8.1.1

* Wed Jun 06 2012 Than Ngo <than@redhat.com> - 1:1.8.1-1
- 1.8.1

* Mon Feb 27 2012 Than Ngo <than@redhat.com> - 1:1.8.0-1
- 1.8.0

* Wed Jan 18 2012 Than Ngo <than@redhat.com> - 1:1.7.6.1-2
- bz#772523, add desktop file

* Fri Dec 16 2011 Than Ngo <than@redhat.com> - 1:1.7.6.1-1
- 1.7.6.1

* Tue Dec 06 2011 Than Ngo <than@redhat.com> - 1:1.7.6-1
- 1.7.6

* Tue Nov 08 2011 Than Ngo <than@redhat.com> - 1:1.7.5.1-1
- 1.7.5.1

* Tue Aug 23 2011 Than Ngo <than@redhat.com> - 1:1.7.5-1
- 1.7.5

* Mon Jun 27 2011 Than Ngo <than@redhat.com> - 1:1.7.4-2
- bz#688684, apply patch to fix crash when not generating man format

* Tue Mar 29 2011 Than Ngo <than@redhat.com> - 1.7.4-1
- 1.7.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Than Ngo <than@redhat.com> - 1.7.3-1
- 1.7.3
- bz#661107

* Fri Nov 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.7.2-2
- Wrong Buildrequire to qt-devel (#651064)

* Mon Oct 11 2010 Than Ngo <than@redhat.com> - 1.7.2-1
- 1.7.2

* Wed Sep 08 2010 Than Ngo <than@redhat.com> - 1:1.7.1-2
- bz#629286, apply patch to fix broken thread handling
- bz#627553, #define in included file in different directory not handled properly
- Inherited documentation doesn't work in case of multiple inheritance

* Mon Jul 19 2010 Than Ngo <than@redhat.com> - 1.7.1-1
- 1.7.1

* Fri Feb 12 2010 Than Ngo <than@redhat.com> - 1.6.2-1.svn20100208
- fix #555526, snapshot 1.6.2-20100208

* Mon Jan 04 2010 Than Ngo <than@redhat.com> - 1:1.6.2-1
- 1.6.2

* Fri Dec 18 2009 Than Ngo <than@redhat.com> - 1:1.6.1-4
- drop _default_patch_fuzz

* Fri Dec 18 2009 Than Ngo <than@redhat.com> - 1:1.6.1-3
- bz#225709, merged review

* Fri Dec 11 2009 Than Ngo <than@redhat.com> - 1:1.6.1-2
- bz#225709, merged review 

* Tue Aug 25 2009 Than Ngo <than@redhat.com> - 1.6.1-1
- 1.6.1

* Mon Aug 24 2009 Than Ngo <than@redhat.com> - 1.6.0-2
- fix #516339, allow to enable/disable timstamp to avoid the multilib issue
  HTMP_TIMESTAMP is disable by default

* Fri Aug 21 2009 Than Ngo <than@redhat.com> - 1.6.0-1
- 1.6.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.9-3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Than Ngo <than@redhat.com> - 1.5.9-1
- 1.5.9

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Than Ngo <than@redhat.com> 1.5.8-1
- 1.5.8

* Mon Oct 06 2008 Than Ngo <than@redhat.com> 1.5.7.1-1
- 1.5.7.1

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.6-3
- fix license tag

* Wed May 21 2008 Than Ngo <than@redhat.com> 1.5.6-2
- rebuild

* Mon May 19 2008 Than Ngo <than@redhat.com> 1.5.6-1
- 1.5.6

* Fri Mar 14 2008 Than Ngo <than@redhat.com> 1.5.5-3
- apply patch to not break partial include paths, thanks to Tim Niemueller

* Wed Feb 20 2008 Than Ngo <than@redhat.com> 1.5.5-2
- apply patch to make doxygen using system libpng/zlib

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 1.5.5-1
- 1.5.5

* Wed Nov 28 2007 Than Ngo <than@redhat.com> 1.5.4-1
- 1.5.4

* Fri Aug 10 2007 Than Ngo <than@redhat.com> - 1:1.5.3-1
- 1.5.3

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 1:1.5.2-1
- 1.5.2

* Fri Nov 03 2006 Than Ngo <than@redhat.com> 1:1.5.1-2
- 1.5.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.7-1.1
- rebuild

* Mon Jun 12 2006 Than Ngo <than@redhat.com> 1:1.4.7-1
- update to 1.4.7

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-5
- fix build problem in mock #193358 

* Fri May 12 2006 Than Ngo <than@redhat.com> 1:1.4.6-4
- apply patch to fix Doxygen crash on empty file #191392 
- html docs #187177 

* Wed Mar 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-3
- fix typo bug #184400

* Mon Mar 06 2006 Than Ngo <than@redhat.com> 1:1.4.6-2
- fix build problem #184042

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Than Ngo <than@redhat.com> 1.4.6-1
- 1.4.6

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 1.4.5-3
- apply patch to fix build problem with gcc-4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com>
- fix references to /usr/X11R6

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.4.5

* Mon Sep 19 2005 Than Ngo <than@redhat.com> 1:1.4.4-2
- move doxywizard man page to subpackge doxywizard

* Thu Jul 21 2005 Than Ngo <than@redhat.com> 1:1.4.4-1
- update to 1.4.4

* Tue Jun 14 2005 Than Ngo <than@redhat.com> 1.4.3-1
- 1.4.3

* Thu Mar 31 2005 Than Ngo <than@redhat.com> 1:1.4.2-1
- 1.4.2

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:1.4.1-2
- rebuilt against gcc-4

* Wed Jan 19 2005 Than Ngo <than@redhat.com> 1:1.4.1-1
- update to 1.4.1

* Sun Oct 10 2004 Than Ngo <than@redhat.com> 1:1.3.9.1-1
- update to 1.3.9.1

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 1:1.3.9-1
- update to 1.3.9

* Sun Jul 25 2004 Than Ngo <than@redhat.com> 1:1.3.8-1
- update to 1.3.8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Than Ngo <than@redhat.com> 1.3.7-1
- update to 1.3.7, bug #119340

* Sun Apr 04 2004 Than Ngo <than@redhat.com> 1:1.3.6-2
- fix qt-mt linking problem

* Thu Feb 26 2004 Than Ngo <than@redhat.com> 1:1.3.6-1
- update to 1.3.6
- added more buildrequires, #110752

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 17 2003 Than Ngo <than@redhat.com> 1:1.3.5-1
- 1.3.5 release

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1:1.3.4-1
- update to 1.3.4
- doxsearch was removed

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without qt/doxywizard

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Than Ngo <than@redhat.com> 1.3-1
- 1.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 27 2002 Than Ngo <than@redhat.com> 1.2.18-2
- use gnu install

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 1.2.18-1.2
- fix some build problem

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 1.2.18-1
- 1.2.18

* Wed Aug 28 2002 Than Ngo <than@redhat.com> 1.2.17-1
- 1.2.17 fixes many major bugs

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-5
- rebuild against qt 3.0.3-10

* Fri Mar  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-4
- rebuild against qt 3.0.2

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.2.14-2
- rebuild against qt 2.3.2

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.14-1
- 1.2.14

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jan 06 2002 Than Ngo <than@redhat.com> 1.2.13.1-1
- update to 1.2.13.1
- fixed build doxywizard with qt3

* Sun Dec 30 2001 Jeff Johnson <jbj@redhat.com> 1.2.13-1
- update to 1.2.13

* Sun Nov 18 2001 Than Ngo <than@redhat.com> 1.2.12-1
- update to 1.2.12
- s/Copyright/License

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Wed Jun 13 2001 Than Ngo <than@redhat.com>
- update tp 1.2.8.1
- make doxywizard as separat package
- fix to use install as default

* Tue Jun 05 2001 Than Ngo <than@redhat.com>
- update to 1.2.8

* Tue May 01 2001 Than Ngo <than@redhat.com>
- update to 1.2.7
- clean up specfile
- patch to use RPM_OPT_FLAG

* Wed Mar 14 2001 Jeff Johnson <jbj@redhat.com>
- update to 1.2.6

* Wed Feb 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Dec 26 2000 Than Ngo <than@redhat.com>
- update to 1.2.4
- remove excludearch ia64
- bzip2 sources

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- rebuild with the fixed fileutils

* Mon Oct 30 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.3.

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.2.
- enable doxywizard.

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- 1.2.1 is latest stable, so we upgrade before Winston is released.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Florian La Roche <laroche@redhat.de>
- fix QTDIR detection

* Fri Jun 09 2000 Preston Brown <pbrown@redhat.com>
- compile on x86 w/o optimization, revert when compiler fixed!!

* Wed Jun 07 2000 Preston Brown <pbrown@redhat.com>
- use newer RPM macros

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- add to distro.

* Tue May  9 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- recompile with current Qt (2.1.0/1.45)

* Wed Jan  5 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.0.0.
- recompile with qt-2.0.1 if available.
- relocatable package.

* Mon Nov  8 1999 Tim Powers <timp@redhat.com>
-updated to 0.49-991106

* Tue Jul 13 1999 Tim Powers <timp@redhat.com>
- updated source
- cleaned up some stuff in the spec file

* Thu Apr 22 1999 Jeff Johnson <jbj@redhat.com>
- Create Power Tools 6.0 package.
