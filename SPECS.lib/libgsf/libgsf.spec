Summary: GNOME Structured File library
Summary(zh_CN.UTF-8): GNOME 结构文件库
Name: libgsf
Version:	1.14.34
Release: 4%{?dist}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: https://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz
URL: http://www.gnome.org/projects/libgsf/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glib2-devel, perl-XML-Parser
BuildRequires: libtool, libxml2-devel, glib2-devel, bzip2-devel, gettext
BuildRequires: libbonobo-devel, pygtk2-devel, intltool, gnome-vfs2-devel

%description
A library for reading and writing structured files (e.g. MS OLE and Zip)

%description -l zh_CN.UTF-8
GNOME 结构文件（如 MS OLE 或 Zip等）库。

%package devel
Summary: Support files necessary to compile applications with libgsf
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libgsf = %{version}-%{release}, glib2-devel, libxml2-devel
Requires: pkgconfig
Obsoletes: libgsf-gnome-devel < 1.14.22

%description devel
Libraries, headers, and support files necessary to compile applications using 
libgsf.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-gtk-doc --disable-static  --enable-introspection=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
magic_rpm_clean.sh
%find_lang libgsf
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{python_sitearch}/gsf/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libgsf.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB README
%{_libdir}/libgsf-1.so.*
%{_libdir}/girepository-1.0/Gsf-1.typelib
%{_bindir}/gsf-office-thumbnailer
%{_mandir}/man1/gsf-office-thumbnailer.1.gz
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/gsf-office.thumbnailer

%files devel
%defattr(-,root,root,-)
%{_bindir}/gsf
%{_bindir}/gsf-vba-dump
%{_libdir}/libgsf-1.so
%{_libdir}/pkgconfig/libgsf-1.pc
%dir %{_includedir}/libgsf-1
%{_includedir}/libgsf-1/gsf
%{_datadir}/gtk-doc/html/gsf
%{_datadir}/gir-1.0/Gsf-1.gir
%{_mandir}/man1/gsf.1.gz
%{_mandir}/man1/gsf-vba-dump.1.gz


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.14.34-4
- 更新到 1.14.34

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.14.30-3
- 更新到 1.14.30

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.14.21-3
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.14.21-2
- Rebuild for new libpng

* Sun May 22 2011 Caolán McNamara <caolanm@redhat.com> 1.14.21-1
- latest version

* Sat Apr 02 2011 Caolán McNamara <caolanm@redhat.com> 1.14.20-1
- latest version
- drop integrated libgsf.gnome634435.avoidcrash.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Caolán McNamara <caolanm@redhat.com> 1.14.19-3
- Resolves: rhbz#650874 / gnome#634435 crash parsing ancient .ppt

* Wed Sep 29 2010 jkeating - 1.14.19-2
- Rebuilt for gcc bug 634757

* Sun Sep 26 2010 Caolán McNamara <caolanm@redhat.com> 1.14.19-1
- latest version

* Tue Jul 27 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-5
- Resolves: rhbz#618514 pre/post only needed in gnome subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.14.18-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-3
- Resolves: rhbz#226023 merge review comments

* Sun Jun 13 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-2
- include COPYING.LIB

* Thu Apr 08 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-1
- latest version

* Sun Feb 14 2010 Caolán McNamara <caolanm@redhat.com> 1.14.17-1
- latest version

* Fri Oct 16 2009 Caolán McNamara <caolanm@redhat.com> 1.14.16-1
- latest version
- drop integrated libgsf.gnome594359.gdk-pixbuf.patch

* Mon Sep 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-4
- Resolves: rhbz#521513 try gdk-pixbuf before ImageMagick convert

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-2
- clean some rpmlint warnings

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-1
- latest version

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> 1.14.14-1
- latest version

* Thu May 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.13-1
- latest version

* Wed Apr 29 2009 Caolán McNamara <caolanm@redhat.com> 1.14.12-1
- latest version, drop integrated libgsf-1.14.11.gcc39015.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Caolán McNamara <caolanm@redhat.com> 1.14.11-2
- fix g_enum_register_static use

* Wed Jan 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.11-1
- latest version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.14.10-2
- Rebuild for Python 2.6

* Mon Oct 20 2008 Caolán McNamara <caolanm@redhat.com> 1.14.10-1
- latest version

* Tue Sep 23 2008 Matthias Clasen  <mclasen@redhat.com> - 1.14.9-2
- Drop the ImageMagick dependency again, since it causes size problems on 
  the live cd

* Wed Sep 03 2008 Caolán McNamara <caolanm@redhat.com> 1.14.9-1
- latest version with gio support

* Fri Aug 08 2008 Caolán McNamara <caolanm@redhat.com> 1.14.8-2
- Resolves: rhbz#458353 gsf-office-thumbnailer doesn't work without ImageMagick's convert.
  Move that into the gnome subpackage

* Thu Mar 06 2008 Caolán McNamara <caolanm@redhat.com> 1.14.8-1
- latest version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.14.7-3
- Autorebuild for GCC 4.3

* Fri Dec 21 2007 Caolán McNamara <caolanm@redhat.com> 1.14.7-2
- Resolves: rhbz#426436 fix up python x86_64 import gsf

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> 1.14.7-1
- Update to 1.14.7

* Wed Sep 05 2007 Caolán McNamara <caolanm@redhat.com> 1.14.6-1
- next version

* Wed Aug 29 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-3
- rebuild

* Thu Aug 02 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-2
- clarify license: LGPL v2.1 in source headers, no "later"

* Thu Jul 12 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-1
- next version

* Mon Jun 18 2007 Caolán McNamara <caolanm@redhat.com> 1.14.4-1
- next version

* Sun Mar 25 2007 Caolán McNamara <caolanm@redhat.com> 1.14.3-4
- Resolves rhbz#233862 unowned directory fix from Michael Schwendt

* Fri Feb 09 2007 Caolán McNamara <caolanm@redhat.com> 1.14.3-3
- some spec cleanups

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.14.3-2
- rebuild for python 2.5

* Thu Nov 09 2006 Caolán McNamara <caolanm@redhat.com> 1.14.3-1
- bump to 1.14.3

* Wed Nov  1 2006 Dan Williams <dcbw@redhat.com> - 1.14.2-2
- Split to remove gnome-vfs2 dependency on core sub-packages

* Mon Oct 09 2006 Caolán McNamara <caolanm@redhat.com> - 1.14.2-1
- bump to 1.14.2

* Fri Jul 14 2006 Bill Nottingham <notting@redhat.com> - 1.14.1-6
- gnome-vfs2-devel no longer requires libbonobo-devel; add it as a buildreq

* Wed Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 1.14.1-5
- rebuild
- add missing br gettext

* Mon May 29 2006 Caolán McNamara <caolanm@redhat.com> 1.14.1-4
- rh#193417# Add BuildRequires perl-XML-Parser

* Tue May 23 2006 Caolán McNamara <caolanm@redhat.com> 1.14.1-3
- rh#192707# disable rebuilding of gtk-doc so as to allow multi-arch devel

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 1.14.1-2
- Update to 1.14.1

* Mon Mar 20 2006 Caolán McNamara <caolanm@redhat.com> 1.14.0-1
- next version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.13.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.13.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Caolán McNamara <caolanm@redhat.com> 1.13.3-2
- rh#172062# Obsolete extras libgsf113

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> 1.13.3-1
- Update to 1.13.3

* Tue Sep 20 2005 Caolán McNamara <caolanm@redhat.com> 1.12.3-1
- bump to next version
- add manpage for gsf-office-thumbnailer

* Fri Aug 26 2005 Caolán McNamara <caolanm@redhat.com> 1.12.2-1
- bump to latest version

* Wed Jun 15 2005 Caolán McNamara <caolanm@redhat.com> 1.12.1-1
- bump to latest version

* Wed Mar  2 2005 Caolán McNamara <caolanm@redhat.com> 1.12.0-1
- bump to latest version
- clean spec

* Wed Mar  2 2005 Caolán McNamara <caolanm@redhat.com> 1.11.1-2
- rebuild with gcc4

* Thu Dec 16 2004 Caolán McNamara <caolanm@redhat.com> 1.11.1-1
- upgrade to 1.11.1

* Tue Aug 31 2004 Caolán McNamara <caolanm@redhat.com> 1.10.1-1
- upgrade to 1.10.1

* Wed Aug 18 2004 Caolán McNamara <caolanm@redhat.com> 1.10.0-1
- upgrade to 1.10.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  6 2004 Dams <anvil[AT]livna.org> 1.9.0-2
- -devel now requires libgsf=version-release
- Added smp_mflags
- Fixed double included .so files

* Wed May 5 2004 Caolán McNamara <caolanm@redhat.com> 1.9.0-1
* upgrade to 1.9.0 to get crash fixes

* Sun Apr 11 2004 Warren Togami <wtogami@redhat.com> 1.8.2-3
- BR libtool libxml2-devel gnome-vfs2-devel bzip2-devel
- -devel req glib2-devel libxml2-devel gnome-vfs2-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 12 2004 Jonathan Blandford <jrb@redhat.com> 1.8.2-1
- make $includedir/libgsf-1 owned by -devel

* Fri Sep 19 2003 Havoc Pennington <hp@redhat.com> 1.8.2-1
- 1.8.2

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com>
- rebuild

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 1.8.1-5
- Fix libtool

* Sat Jul 12 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-4
- use system libtool so that lib64 library deps are correct

* Thu Jul 10 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-3
- forcibly disable gtk-doc (openjade is broken on s390)

* Mon Jul  7 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-2
- ldconfig in %%post/%%postun

* Sun Jul  6 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-1
- use standard macros
- build for Red Hat Linux

* Tue May 13 2003 Rui M. Seabra <rms@407.org>
- fix spec to reflect current stat of the build

* Tue Jun 18 2002 Rui M. Seabra <rms@407.org>
- set permission correctly
- fix common mistake of Copyright flag into License flag.

* Thu May 23 2002 Jody Goldberg <jody@gnome.org>
- Initial version
