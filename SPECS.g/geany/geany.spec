%global geany_docdir %{_docdir}/%{name}-%{version}

# The  Python templates in /usr/share/geany/templates can not be byte-compiled.
%global  _python_bytecompile_errors_terminate_build 0

Name:      geany
Version:   1.23
Release:   1%{?dist}
Summary:   A fast and lightweight IDE using GTK2

Group:     Development/Tools
License:   GPLv2+
URL:       http://www.geany.org/
Source0:   http://download.geany.org/%{name}-%{version}.tar.bz2

# The following tags files were retrieved 6th Jan 2011,
Source1:   http://wiki.geany.org/_media/tags/dbus-glib-0.76.c.tags
Source2:   http://wiki.geany.org/_media/tags/drupal.php.tags
Source3:   http://wiki.geany.org/_media/tags/ethos-1.0.c.tags
Source4:   http://wiki.geany.org/_media/tags/geany-api-0.21.c.tags
Source5:   http://wiki.geany.org/_media/tags/gladeui-1.0.c.tags
Source6:   http://wiki.geany.org/_media/tags/gnt.c.tags
Source7:   http://wiki.geany.org/_media/tags/gtk_-2.24.c.tags
Source8:   http://download.geany.org/contrib/tags/gtkscintilla-2.0.c.tags
Source9:   http://wiki.geany.org/_media/tags/gtksourceview-3.0.c.tags
Source10:  http://wiki.geany.org/_media/tags/libdevhelp-2.0.c.tags
Source11:  http://wiki.geany.org/_media/tags/libgdl-3.0.c.tags
Source12:  http://wiki.geany.org/_media/tags/libxml-2.0.c.tags
Source13:  http://wiki.geany.org/_media/tags/sqlite3.c.tags
Source14:  http://wiki.geany.org/_media/tags/standard.css.tags
Source15:  http://wiki.geany.org/_media/tags/std.glsl.tags
Source16:  http://wiki.geany.org/_media/tags/std.latex.tags
Source17:  http://download.geany.org/contrib/tags/std.vala.tags
Source18:  http://wiki.geany.org/_media/tags/v4l2.c.tags
Source19:  http://wiki.geany.org/_media/tags/webkit-1.0.c.tags
Source20:  http://wiki.geany.org/_media/tags/wordpress.php.tags
Source21:  http://wiki.geany.org/_media/tags/xfce48.c.tags
Source22:  http://advamacs.com/pub/tcl.tcl.tags


BuildRequires: desktop-file-utils, gettext, gtk2-devel, glib2-devel, pango-devel, intltool
BuildRequires: perl(XML::Parser)
Requires: vte


%description
Geany is a small and fast integrated development enviroment with basic
features and few dependencies to other packages or Desktop Environments.

Some features:
- Syntax highlighting
- Code completion
- Code folding
- Construct completion/snippets
- Auto-closing of XML and HTML tags
- Call tips
- Support for Many languages like C, Java, PHP, HTML, Python, Perl, Pascal
- symbol lists and symbol name auto-completion
- Code navigation
- Simple project management
- Plugin interface

%package devel
Summary:   Header files for building Geany plug-ins
Group:     Development/Tools
Requires:  geany = %{version}-%{release}
Requires:  pkgconfig gtk2-devel

%description devel
This package contains the header files and pkg-config file needed for building
Geany plug-ins. You do not need to install this package to use Geany.

%prep
%setup -q

# remove waf since this isn't needed for the build, we're building the package
# with autotools
rm -f waf
rm -f wscript


%build
%configure --docdir=%{geany_docdir}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=$RPM_BUILD_ROOT/%{geany_docdir}
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.ico
desktop-file-install --delete-original --vendor="fedora"        \
        --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --mode 0644                                             \
        $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

# Remove static library *.la files
rm -rf $RPM_BUILD_ROOT%{_libdir}/geany/*.la

# Install tags files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/tags/
install -p %{SOURCE1}  %{SOURCE2}  %{SOURCE3}  %{SOURCE4}  %{SOURCE5}  %{SOURCE6} \
           %{SOURCE7}  %{SOURCE8}  %{SOURCE9}  %{SOURCE10} %{SOURCE11} %{SOURCE12}\
           %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18}\
           %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22}\
           $RPM_BUILD_ROOT%{_datadir}/%{name}/tags/

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-, root, root, -)
%exclude %{geany_docdir}/TODO

%doc %{geany_docdir}
%doc %{_mandir}/man1/geany.1.*

%{_bindir}/%{name}
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/icons/*/*/*/*.svg
%{_datadir}/icons/*/*/*/*.png

%files devel
%defattr(-, root, root, -)
%doc HACKING TODO
%{_includedir}/geany
%{_libdir}/pkgconfig/geany.pc

%changelog
* Sun Mar 10 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 1.23-1
- New upstream release: Geany 1.23

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 1.22-1
- New upstream release: Geany 1.22
- remove the previous patch to fix DSO linking, this is now included upstream
- update upstream URLs for tags files

* Mon May 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.21-5
- Add patch to fix FTBFS due to DSO linking, spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.21-3
- update GTK+ tags to 2.24

* Sun Dec 18 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.21-2
- update Xfce tags to 4.8

* Sun Oct 02 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.21-1
- New upstream release: Geany 0.21

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.20-2
- install tags files correctly

* Thu Jan 06 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.20-1
- new upstream release
- a lot of new tags files

* Wed Dec 01 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.19.2-1
- New upstream release: Geany 0.19.2

* Fri Nov 19 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.19.1-2
- run update-desktop-database in %%post (#655152)

* Thu Aug 19 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.19.1-1
- New upstream release: Geany 0.19.1

* Sun Jun 13 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.19-2
- update tags files for GTK 2.20 and Geany Plugin API 0.19

* Sat Jun 12 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.19-1
- New upstream release: Geany 0.19

* Sun Apr 18 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18.1-3
- improve handling of documentation directory
- add upstream comment about the desktopfile patch

* Thu Apr 15 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18.1-2
- move TODO and HACKING into devel package
- add patch to fix mimetypes in desktop-file
- add Tcl tags
- replace the .gz of manpage with wildcard

* Sun Feb 14 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18.1-1
- New Geany release: 0.18.1
- update GTK2 tags to 2.18
- add tags fpr drupal, LaTeX and libxml
- remove files concerned to the waf build system
- give the Summary and description a small rework

* Sun Aug 16 2009 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18-6
- release bump to correct the update path

* Sun Aug 16 2009 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18-2
- update icon cache

* Sun Aug 16 2009 Dominic Hopf <dmaphy@fedoraproject.org> - 0.18-1
- new upstream release
- remove button pixmaps patch since this fix is included in 0.18
- add new tags-files geany-api-0.18.c.tags and std.vala.tags
- remove Geany icon from pixmaps path and add it to 48x48 and scalable

* Mon Jul 27 2009 Dominic Hopf <dmaphy@fedoraproject.org> - 0.17-9
- install additional *.tags-files to $prefix/share/geany/tags

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-7
- Fix commentary about button pixmap patch in spec file

* Sat Jun 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-6
- Add new patch to fix button pixmaps
- Remove debug patch and previous patch to fix button pixmaps
- Remove tango icon patch

* Sat Jun 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-5
- Fix spec file typo

* Sat Jun 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-4
- Add patch to output debugging message

* Sat Jun 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-3
- Add patch to fix missing button pixmaps

* Fri Jun 19 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-2
- Add patch to give a tango Save All button

* Wed May 20 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.17-1
- Update to version 0.17
- Replace gtk214.c.tags with gtk216.c.tags
- Add standard.css.tags
- Add all tags files to CVS

* Wed Apr 15 2009 pingou <pingou@pingoured.fr> - 0.16-3
- Add requires for gtk2-devel to geany-devel

* Thu Apr  2 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.16-2
- Add Requires for pkgconfig to geany-devel subpackage (BZ 493566)

* Sun Feb 25 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.16-1
- Update to 0.16
- Add tags files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.15-1
- Update to 0.15
- Update URL
- Add intltool to BuildRequires

* Sun May 11 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.14-1
- Update to 0.14
- New -devel sub-package for header files
- Corectly remove the .la libtool files
- Remove hack relating to finding the system installed html files
- No longer correct the desktop file

* Mon Mar 24 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13-2
- Fix docdir/doc_dir so geany correctly finds the system installed html docs (BZ
  438534)

* Sun Feb 24 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.13-1
- Update to version 0.13

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12-5
- Autorebuild for GCC 4.3

* Thu Oct 18 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.12-4
- Fix license tag
- Package new library files
- Remove static library .la files
- Package new icons

* Thu Oct 18 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.12-3
- Fix Version entry in .desktop file again

* Thu Oct 18 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.12-2
- Add a BuildRequires for perl(XML::Parser)

* Thu Oct 18 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.12-1
- Update to version 0.12

* Sun Sep  9 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.11-2
- Fix Version entry in .desktop file

* Sun Sep  9 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 0.11-1
- Update to version 0.11

* Fri Feb 23 2007 Josef Whiter <josef@toxicpanda.com> 0.10.1-1
- updating to 0.10.1 of geany

* Thu Jan 25 2007 Josef Whiter <josef@toxicpanda.com> 0.10-5
- removed autoconf/automake/vte-devel from BR as they are not needed
- removed patch to dynamically link in libvte
- adding patch to find appropriate libvte library from the vte package
- added vte as a Requires

* Wed Jan 24 2007 Josef Whiter <josef@toxicpanda.com> 0.10-4
- added autoconf and automake as a BR

* Wed Jan 24 2007 Josef Whiter <josef@toxicpanda.com> 0.10-3
- adding patch to dynamically link in libvte instead of using g_module_open

* Tue Jan 04 2007 Josef Whiter <josef@toxicpanda.com> 0.10-2
- Fixed mixed spaces/tabs problem
- added sed command to install to fix the ScintillaLicense.txt eol encoding
- fixed the docs so they are installed into the right place
- added an rm pixmaps/geany.ico, its only for windows installations

* Thu Dec 28 2006 Josef Whiter <josef@toxicpanda.com> 0.10-1
- Initial Release
