Summary: Utility for converting FIG files (made by xfig) to other formats
Summary(zh_CN.UTF-8): 转换 FIG 文件（由 xfig 生成）到其它格式的工具
Name: transfig
Version: 3.2.5d
Release: 6%{?dist}
Epoch: 1
License: MIT
URL: http://www.xfig.org/
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Source0: http://downloads.sourceforge.net/mcj/%{name}.%{version}.tar.gz

Patch0: transfig-3.2.5-optflags.patch
Patch1: transfig-3.2.5-modularX.patch
Patch2: transfig-3.2.5-bitmap.patch
Patch3: transfig-3.2.5d-bz728825.patch
Patch4: transfig-3.2.5-libpng.patch
Patch5: transfig-3.2.5d-CVE-2009-4227.patch
Patch6: transfig-3.2.5d-bz1037365.patch

Requires:	ghostscript
Requires:	bc

BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: libXpm-devel
BuildRequires: imake

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The transfig utility creates a makefile which translates FIG (created
by xfig) or PIC figures into a specified LaTeX graphics language (for
example, PostScript(TM)).  Transfig is used to create TeX documents
which are portable (i.e., they can be printed in a wide variety of
environments).

Install transfig if you need a utility for translating FIG or PIC
figures into certain graphics languages.

%description -l zh_CN.UTF-8
转换 FIG 文件（由 xfig 生成）到其它格式的工具。

%prep
%setup -q -n %{name}.%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# fix source permissions
find -type f -exec chmod -x {} \;

# remove garbage
rm -f doc/manual/Makefile.orig doc/fig2dev.1.orig

%build
xmkmf
make Makefiles
make

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install install.man

# fig2ps2tex{,.sh} are equivalent, use the sh one
mv %{buildroot}%{_bindir}/fig2ps2tex.sh %{buildroot}%{_bindir}/fig2ps2tex
ln -s fig2ps2tex %{buildroot}%{_bindir}/fig2ps2tex.sh
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES NOTES README LATEX.AND.XFIG
%{_bindir}/transfig
%{_bindir}/fig2dev
%{_bindir}/fig2ps2tex
%{_bindir}/fig2ps2tex.sh
%{_bindir}/pic2tpic
%{_mandir}/man1/*
%{_datadir}/xfig
%{_datadir}/fig2dev

%changelog
* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 1:3.2.5d-6
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:3.2.5d-5
- 为 Magic 3.0 重建

* Fri Jul 27 2012 Liu Di <liudidi@gmail.com> - 1:3.2.5d-4
- 为 Magic 3.0 重建

* Tue Aug 09 2011 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-3
- fix crash of fig2dev on a failure of ghostscript (#728825)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 04 2010 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-1
- new upstream release (#546623)

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5c-1
- new upstream release
- patch to generate comments compliant with DSC 3.0, thanks to Ian Dall
  (#558380)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May  5 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:3.2.5-7
- Get rid of csh dependency, add missing one on bc (#435993).
- Build with $RPM_OPT_FLAGS (#329831).
- Convert specfile to UTF-8.
- Add URL, fix source URL.
- Escape macros in changelog.
- Improve summary.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:3.2.5-5
- Add transfig-3.2.5-bitmap.patch, tweak permission on sources (BZ #209865).

* Wed Sep 10 2008 Stepan Kasal <skasal@redhat.com> - 1:3.2.5-4
- remove transfig.3.2.4-pstex.patch, which reintroduced #164140
  at the update to 3.2.5

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.2.5-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.2.5-2
- Autorebuild for GCC 4.3

* Mon Apr 16 2007 Than Ngo <than@redhat.com> - 1:3.2.5-1.fc7
- 3.2.5

* Wed Aug 16 2006 Stepan Kasal <skasal@redhat.com> - 1:3.2.4-16
- Require ghostscript; fig2dev calls it.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-15.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-15
- fix #164140, transfig creates wrong dependencies for -L pstex

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-14
- fix #191825, buildrequire on imake
- fix #173748, fig2dev still refers to /usr/X11R6/lib/X11/rgb.txt

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 3.2.4-13
- fix build problem with modular X

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 1:3.2.4-12
- fix for modular X 

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 1:3.2.4-11
- rebuild

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.2.4-10
- fix compiler warnings #111394
- fix broken language selection #114849

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.2.4-9
- add patch to fix getrgb #117099

* Mon Oct 18 2004 Miloslav Trmac <mitr@redhat.com> - 1:3.2.4-8
- Fix at least a few obvious instances of C abuse (partly #74594 with patch by
  Sysoltsev Slawa)
- Drop -Dcfree=free fix, not needed with current version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.2.4-4
- patch build problem

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Jeremy Katz <katzj@redhat.com> 1:3.2.4-2
- fix build with gcc 3.3

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.2.4-1
- 3.2.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Than Ngo <than@redhat.com> 3.2.3d-8
- Added a patch file from d.binderman@virgin.net (bug #77980)

* Wed Jul 31 2002 Than Ngo <than@redhat.com> 3.2.3d-7
- fig2dev crashes with more than 1 gif files (bug #69917)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 han Ngo <than@redhat.com> 3.2.3d-5
- fhs fixes (bug #66732)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jul 23 2001 Than Ngo <than@redhat.com>
- fix build dependencies (bug #49725)
- Copyright -> License

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d release (Bug # 44742)

* Tue May 29 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d beta2

* Fri Apr 13 2001 Than Ngo <than@redhat.com>
- fix core dump when using LDAP auth
- update ftp site 

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Enable Japanese

* Sat Aug 05 2000 Than Ngo <than@redhat.de>
- update to 3.2.3c (Bug fixed release)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make it build as nobody. Imake sucks.
- include LATEX.AND.XFIG
- use %%{_tmppath}

* Wed Apr 26 2000 Matt Wilson <msw@redhat.com>
- add enable_japanese option, disable it for now.

* Sun Apr 16 2000 Bryan C. Andregg <bandregg@redhat.com>
- new version to support -b and -g which xfig uses

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.2.1.

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- add %%clean.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Nov 13 1997 Otto Hammersmith <otto@redhat.com>
- fixed problem with Imakefile for fig2dev not including $(XLIB)
- build rooted.

* Fri Oct 24 1997 Otto Hammersmith <otto@redhat.com>
- recreated the glibc patch that is needed for an alpha build, missed it
  building on the intel.

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- updated version
- fixed source url

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
