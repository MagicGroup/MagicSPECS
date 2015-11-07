Summary: A X front-end for the Ghostscript PostScript(TM) interpreter
Summary(zh_CN.UTF-8): Ghostscripts PostScript(TM) 解释器的 X 前端
Name: gv
Version: 3.7.4
Release: 4%{?dist}
License: GPLv3+
Group: Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
Requires: ghostscript
URL: http://www.gnu.org/software/gv/
#Source0: ftp://ftp.gnu.org/gnu/gv/gv-%{version}.tar.gz
Source0: http://ftp.gnu.org/gnu/gv/gv-%{version}.tar.gz
Source1: gv.png
BuildRequires: /usr/bin/makeinfo
BuildRequires: Xaw3d-devel
%if 0%{?rhel} != 04
BuildRequires: libXinerama-devel
%endif
BuildRequires: zlib-devel, bzip2-devel
BuildRequires: desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/install-info, /usr/bin/update-mime-database
Requires(post): /usr/bin/update-desktop-database
Requires(preun): /sbin/install-info
Requires(postun): /usr/bin/update-mime-database
Requires(postun): /usr/bin/update-desktop-database


%description
GNU gv is a user interface for the Ghostscript PostScript(TM) interpreter.
Gv can display PostScript and PDF documents on an X Window System.

%description -l zh_CN.UTF-8
Ghostscripts PostScript(TM) 解释器的 X 前端，它在在 X 窗口系统下显示 PS 和 PDF 文档。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Still provide link
ln $RPM_BUILD_ROOT%{_bindir}/gv $RPM_BUILD_ROOT%{_bindir}/ghostview

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

cat > gv.desktop <<EOF
[Desktop Entry]
Name=GNU GV PostScript/PDF Viewer
GenericName=PostScript/PDF Viewer
Comment="View PostScript and PDF files"
Type=Application
Icon=gv
MimeType=application/postscript;application/pdf;
StartupWMClass=GV
Exec=gv
EOF

desktop-file-install --vendor=magic \
       --add-category=Applications\
       --add-category=Graphics \
       --dir %{buildroot}%{_datadir}/applications/ \
       gv.desktop

#Icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -p %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/pixmaps

# Remove info dir file
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post
/usr/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
/usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%postun
if [ $1 = 0 ]; then
    /usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
    /usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ghostview
%{_bindir}/gv
%{_bindir}/gv-update-userconfig
%{_datadir}/gv/
%{_datadir}/applications/magic-gv.desktop
%{_datadir}/info/gv.info.gz
%{_datadir}/pixmaps/gv.png
%{_mandir}/man1/gv.*
%{_mandir}/man1/gv-update-userconfig.*


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.7.4-4
- 为 Magic 3.0 重建

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 3.7.4-3
- 更新到 3.7.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.7.3.90-3
- 为 Magic 3.0 重建

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 5 2012 Orion Poplawski <orion@cora.nwra.com> - 3.7.3.90-1
- Update to 3.7.3.90
- Drop Xaw3d patch applied upstream

* Sun Feb 26 2012 Orion Poplawski <orion@cora.nwra.com> - 3.7.3-3
- Rebuild with Xaw3d 1.6.1
- Add patch from Gentoo for Xawd3d 1.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 2 2011 Orion Poplawski <orion@cora.nwra.com> 3.7.3-1
- Update to 3.7.3

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.2-2
- Rebuilt for glibc bug#747377

* Mon May 2 2011 Orion Poplawski <orion@cora.nwra.com> 3.7.2-1
- Update to 3.7.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 8 2010 Orion Poplawski <orion@cora.nwra.com> 3.7.1-2
- Re-enable international support

* Mon Jun 28 2010 Orion Poplawski <orion@cora.nwra.com> 3.7.1-1
- Update to 3.7.1
- Disable international support to avoid segfault on exit until
  bug 587349 is fixed

* Thu Jun 3 2010 Orion Poplawski <orion@cora.nwra.com> 3.6.91-1
- Update to 3.6.91 to fix CVE-2010-2055 and CVE-2010-2056

* Mon Apr 26 2010 Orion Poplawski <orion@cora.nwra.com> 3.6.9-1
- Update to 3.6.9

* Tue Mar 2 2010 Orion Poplawski <orion@cora.nwra.com> 3.6.8-2
- Ship icon, update desktop file

* Mon Dec 28 2009 Orion Poplawski <orion@cora.nwra.com> 3.6.8-1
- Update to 3.6.8

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 Orion Poplawski <orion@cora.nwra.com> 3.6.7-1
- Update to 3.6.7

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.6-1
- Update to 3.6.6
- Add extra neede BuildRequires
- Remove upstreamed patches
- Fix license - GPLv3+

* Wed Aug 6 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.5-3
- Apply upstream patch to display more error messages

* Thu Jul 18 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.5-2
- Change install dir patch to be more palatable for upstream

* Thu Jul 17 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.5-1
- Update to 3.6.5

* Mon Jun 2 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.4-1
- Update to 3.6.4
- Cleanup desktop file a little

* Sat Feb  9 2008 Orion Poplawski <orion@cora.nwra.com> 3.6.3-3
- Rebuild for gcc 3.4

* Tue Aug 21 2007 Orion Poplawski <orion@cora.nwra.com> 3.6.3-2
- Update license tag to GPLv2+
- Rebuild for ppc32

* Fri Jun 29 2007 Orion Poplawski <orion@cora.nwra.com> 3.6.3-1
- Update to 3.6.3

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.2-2
- Apply patch from Mandriva to fix CVE-2006-5864/bug 215136

* Wed Oct 11 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.2-1
- Update to 3.6.2

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-8
- Rebuild for FC6

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-7
- Rebuild for gcc/glibc changes

* Wed Feb  1 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-6
- Remove info dir file

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-5
- Rebuild

* Thu Oct 27 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-4
- Add patch find app defaults file (#171848)
- Add BR: /usr/bin/makeinfo to properly build .info file (#171849)

* Thu Oct 20 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-3
- Fixup .desktop file, add Comment and StartupWMClass

* Thu Oct 20 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-2
- Trim install paragraph from Description
- Add MimeType to desktop and update mime and desktop databases
- Fix info file handling

* Mon Oct 17 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-1
- Updated to 3.6.1
- Fedora Extras version

* Sun Sep 19 2004 Dan Williams <dcbw@redhat.com> 3.5.8-29
- Fix .desktop file (#125849)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 14 2004 Dan Williams <dcbw@redhat.com> 3.5.8-27
- display empty page when input file has size 0 (#100538)

* Fri May 14 2004 Dan Williams <dcbw@redhat.com> 3.5.8-26
- fix argv array size (#80672)

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 3.5.8-25
- fix desktop file (#120190)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.5.8-21
- rebuild on all arches

* Tue Nov 19 2002 Bill Nottingham <notting@redhat.com> 3.5.8-20
- rebuild

* Tue Sep 24 2002 Bill Nottingham <notting@redhat.com>
- fix handling of certain postscript/pdf headers
- use mkstemp

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Bill Nottingham <notting@redhat.com>
- remove anti-aliasing change; it causes problems

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Fri Jan 25 2002 Bill Nottingham <notting@redhat.com>
- fix anti-aliasing (#58686)

* Fri Jul 13 2001 Bill Nottingham <notting@redhat.com>
- fix some build issues (#48983, #48984)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- add filename quoting patch from debian
- rebuild in new build environment

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new libXaw3d

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Mon Jan 23 1999 Michael Maher <mike@redhat.com>
- fixed bug #272, changed group

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built pacakge for 6.0

* Sat Aug 15 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Thu Nov 06 1997 Cristian Gafton <gafton@redhat.com>
- we are installin a symlink to ghostview

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 3.5.8

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 15 1997 Erik Troan <ewt@redhat.com>
- added ghostscript requirement, added errlist patch for glibc.
