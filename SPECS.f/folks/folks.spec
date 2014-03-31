%global _changelog_trimtime %(date +%s -d "1 year ago")

%define tp_glib_ver	0.19.0
%define zeitgeist_ver   0.9.14

Name:           folks
Epoch:          1
Version:        0.9.6
Release:        4%{?dist}
Summary:        GObject contact aggregation library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://telepathy.freedesktop.org/wiki/Folks
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.8/%{name}-%{version}.tar.xz
Patch0:         Remove_Assert.patch

BuildRequires:  telepathy-glib-devel >= %{tp_glib_ver}
BuildRequires:  telepathy-glib-vala
BuildRequires:  zeitgeist-devel >= %{zeitgeist_ver}
BuildRequires:  glib2-devel
BuildRequires:  vala-devel >= 0.17.6
BuildRequires:  vala-tools
BuildRequires:  libxml2-devel
BuildRequires:  gobject-introspection >= 0.9.12
BuildRequires:  GConf2-devel
BuildRequires:  evolution-data-server-devel >= 3.9.1
BuildRequires:  readline-devel
## BuildRequires: tracker-devel >= 0.10
BuildRequires:  pkgconfig(gee-0.8) >= 0.8.4


%description
libfolks is a library that aggregates people from multiple sources (e.g.
Telepathy connection managers and eventually evolution data server,
Facebook, etc.) to create meta-contacts.


%package        tools
Summary:        Tools for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    tools
%{name}-tools contains a database and import tool.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Requires:       telepathy-glib-devel >= %{tp_glib_ver}
Requires:       glib2-devel
Requires:       pkgconfig
Requires:	pkgconfig(gee-0.8)
Requires:	vala-devel >= 0.15.2
Requires:	vala-tools

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .assert



%build
%configure --disable-static --disable-fatal-warnings --enable-eds-backend --enable-vala --enable-inspect-tool --disable-libsocialweb-backend
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}


%post -p /sbin/ldconfig


%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.*
%{_libdir}/folks
%{_libdir}/girepository-1.0/Folks-0.6.typelib
%{_libdir}/girepository-1.0/FolksEds-0.6.typelib
%{_libdir}/girepository-1.0/FolksTelepathy-0.6.typelib
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files tools
%{_bindir}/%{name}-import
%{_bindir}/%{name}-inspect

%files devel
%{_includedir}/folks
%{_libdir}/*.so
%{_libdir}/pkgconfig/folks*.pc
%{_datadir}/gir-1.0/Folks-0.6.gir
%{_datadir}/gir-1.0/FolksEds-0.6.gir
%{_datadir}/gir-1.0/FolksTelepathy-0.6.gir
%{_datadir}/vala/vapi/%{name}*


%changelog
* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 1:0.9.6-4
- Rebuild against newer evolution-data-server

* Tue Jan 14 2014 Milan Crha <mcrha@redhat.com> - 1:0.9.6-3
- Rebuild against newer evolution-data-server

* Mon Nov 18 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.6-2
- Add patch to remove assert that was causing IRC crash. (#1031252)

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 1:0.9.6-1
- Update to 0.9.6

* Wed Oct 23 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.5-2
- Rebuild for latest libcamel.

* Tue Aug 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.5-1
- Update to 0.9.5.

* Mon Aug 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.4-1
- Update to 0.9.4.
- Bump minimum version of eds needed.

* Mon Aug 19 2013 Milan Crha <mcrha@redhat.com> - 1:0.9.3-5
- Rebuild against newer evolution-data-server

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Kalev Lember <kalevlember@gmail.com> - 1:0.9.3-3
- Including missing files
- Disable fatal warnings to fix the build

* Tue Jul 09 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.3-2
- Rebuild for new libcamel.

* Tue Jun 25 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.3-1
- Update to 0.9.3.
- Bump minimum version of zeitgeist needed.

* Sat Jun 22 2013 Matthias Clasen <mclasen@redhat.com> - 1:0.9.2-3
- Trim %%changelog

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 1:0.9.2-2
- Install NEWS instead of ChangeLog (saves some space)

* Sat Jun  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.2-1
- Update to 0.9.2.
- Bump minimum version of eds needed.

* Tue Apr 30 2013 Brian Pepple <bpepple@fedoraproject.org> - 1:0.9.1-2
- Rebuild against new eds.

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 1:0.9.1-1
- Update to 0.9.1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 1:0.8.0-4
- Rebuild for new libcamel.

* Tue Nov 20 2012 Milan Crha <mcrha@redhat.com> - 1:0.8.0-3
- Rebuild for new libcamel.

* Thu Oct 25 2012 Milan Crha <mcrha@redhat.com> - 1:0.8.0-2
- Rebuild for new libcamel.

* Thu Oct  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.8.0-1
- Update to 0.8.0
- Update source url.

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1:0.7.4.1-2
- Silence glib-compile-schemas scriplets

* Wed Sep 12 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.4.1-1
- Update to 0.7.4.1.
- Bump minimum requirement for tp-glib and vala.
- Drop staticmember patches. Fixed upstream.

* Mon Aug 27 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.3-2
- Rebuild for new libcamel.
- Pull upstream patches to fix build errors caused by accessing static members.

* Sun Jul 29 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.3-1
- Update to 0.7.3.

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Matthias Clasen <mclasen@redhat.com> - 1:0.7.2.2-2
- Rebuild

* Tue Jul  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.2.2-1
- Update to 0.7.2.2.
- Update eds version needed.

* Thu Jun 28 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.2.1-1
- Update to 0.7.2.1.
- Drop book-uid patch. Fixed upstream.
- Bump minimum version of eds needed.

* Mon Jun 25 2012 Matthias Clasen <mclasen@redhat.com> - 1:0.7.1-2
- Update for e-d-s api change

* Mon Jun 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.1-1
- Update to 0.7.1.
- Bump version of eds and tp-glib needed.
- Add BR on libzeitgeist-devel.

* Wed Jun 13 2012 Cosimo Cecchi <cosimoc@redhat.com> - 1:0.7.0-2
- Disable libsocialweb backend

* Tue Apr 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.7.0-1
- Update to 0.7.0.
- Update source url.

* Mon Apr 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.9-1
- Update to 0.6.9.
- Drop patch that fixed account sync crash. Fixed upstream.

* Thu Apr  5 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.8-4
- Enable inspect tool (#810098)
- Add BR on readline-devel.

* Tue Apr 03 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.8-3
- Rebuild against new tp-glib.

* Fri Mar 30 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.8-2
- Backport patch to fix crash cause by TpAccount are out of sync.
- Bump minimum version of tp-glib needed.

* Mon Mar 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.8-1
- Update to 0.6.8.
- Bump minimum verions of libsocialweb-devel and vala-devel.

* Wed Feb 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.7-1
- Update to 0.6.7.

* Mon Feb 6 2012 Brian Pepple <bpepple@fedoraproject.org> 1:0.6.6-3
- Rebuild for new eds.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.6-2
- Rebuild for new gcc.

* Wed Dec 14 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.6-1
- Update to 0.6.6.
- Drop name details non-null patch. Fixed upstream.

* Wed Nov 30 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.6.5-4
- Move the vala vapi files to the devel package where they should be and add the appropriate requires

* Sun Nov 27 2011 Colin Walters <walters@verbum.org> - 1:0.6.5-3
- Add patch from git to fix gnome-shell crashes

* Tue Nov 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.5-2
- Rebuild against new eds

* Fri Nov 11 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.5-1
- Update to 0.6.5.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6.4.1-3
- Rebuilt for glibc bug#747377

* Mon Oct 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.4.1-2
- Rebuld against libcamel.

* Tue Oct 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.4.1-1
- Update to 0.6.4.1.

* Tue Oct 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.4-1
- Update to 0.6.4.

* Mon Sep 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.3.2-1
- Update to 0.6.3.2.

* Sun Sep 25 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.3.1-1
- Update to 0.6.3.1.
- Drop typelib patch. Fixed upstream.

* Wed Sep 21 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.3-2
- Fix another typelib problem

* Mon Sep 19 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.3-1
- Update to 0.6.3.
- Drop typelib patch. Fixed upstream.

* Wed Sep 14 2011 Owen Taylor <otaylor@redhat.com> - 1:0.6.2.1-2
- Really fix the typelib to embed the right .so file

* Thu Sep  8 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.2.1-1
- Really fix the reentrancy problem, by using 0.6.2.1

* Thu Sep  8 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.2-2
- Fix a reentrancy problem that causes gnome-shell to crash

* Thu Sep  8 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.2-1
- Update to 0.6.2.1

* Thu Sep  8 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.2-1
- Update to 0.6.2
- Use old libgee api.

* Wed Sep  7 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.1-4
- Try again

* Tue Sep 06 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.1-3
- Rebuld against new libcamel.

* Thu Sep  1 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.1-2
- Fix up the typelib

* Mon Aug 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.1-1
- Update to 0.6.1.
- Drop EDS patch. Fixed upstream.

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 1:0.6.0-6
- Rebuild against newer evolution-data-server

* Fri Aug 19 2011 Matthias Clasen <mclasen@redhat.com> - 1:0.6.0-4
- Try again to rebuild

* Tue Aug 16 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.0-2
- Rebuld for new eds

* Sat Aug 13 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.6.0-1
- Update to 0.6.0.
- Update source url.
- Add BR on eds-devel and libsocialweb-devel.

* Fri Jun 10 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.5.2-1
- Update to 0.5.2.
- Add BR on GConf2-devel.

* Wed Mar 23 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.4.2-1
- Update to 0.4.2.

* Fri Mar 18 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.4.1-1
- Update to 0.4.1.

* Thu Mar 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.4.0-2
- Update source url.

* Thu Mar 17 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.4.0-1
- Update to 0.4.0.

* Mon Feb 14 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.3.6-1
- Update to 0.3.6.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:0.3.4-1
- Update to 0.3.4.

* Tue Dec 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 1:0.3.3-1
- Update to 0.3.3.

* Sun Nov 14 2010 Brian Pepple <bpepple@fedoraproject.org> - 1:0.3.2-1
- Update to 0.3.2.
- Update min version of tp-glib.
- Update source url.
- Drop dso linking patch. Fixed upstream.

* Fri Oct 29 2010 Brian Pepple <bpepple@fedoraproject.org> - 1:0.2.1-1
- Update to 0.2.1.
- Add patch to fix dso linking. (fdo #633511)

* Fri Oct 29 2010 Brian Pepple <bpepple@fedoraproject.org> - 1:0.2.0-4
- Add epoch to devel subpackage requires.

* Mon Oct 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 1:0.2.0-3
- Revert back to 0.2.x until gtk-2.92.1 or greater is in rawhide.

* Wed Oct 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1.
- Update source url.
- Update tp-glib version required.

* Wed Sep 29 2010 jkeating - 0.2.0-2
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0.
- Add missing requires to devel subpackage.
- Drop DSO linkng patch. Fixed upstream.

* Sun Sep 12 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.1.17-1
- Update to 0.1.17.
- Add patch to fix DSO linking for import tool.
- Add BR on libxml2-devel so import tool is built.

* Wed Sep  1 2010 Yanko Kaneti <yaneti@declera.com> 0.1.16-1
- New upstream release.

* Thu Aug 30 2010 Yanko Kaneti <yaneti@declera.com> 0.1.15-1
- New upstream release. Drop the RPATH hacks.

* Thu Aug 19 2010 Yanko Kaneti <yaneti@declera.com> 0.1.14.1-1
- New upstream release. Requires vala >= 0.9.6

* Thu Aug 19 2010 Yanko Kaneti <yaneti@declera.com> 0.1.14-2
- Use chrpath to remove the lingering RPATH because the guidelines
  recomended sed makes libtool incapable of building the tp-lowlevel.gir.
  Better solution welcome.

* Wed Aug 18 2010 Yanko Kaneti <yaneti@declera.com> 0.1.14-1
- New upstream. Remove patch and libtool hack.

* Tue Aug 17 2010 Yanko Kaneti <yaneti@declera.com> 0.1.13-4
- Add BR: vala-tools

* Tue Aug 17 2010 Yanko Kaneti <yaneti@declera.com> 0.1.13-3
- Update for the available telepathy-glib vala packaging

* Thu Aug 12 2010 Yanko Kaneti <yaneti@declera.com> 0.1.13-2
- Add BR: libgee-devel

* Thu Aug 12 2010 Yanko Kaneti <yaneti@declera.com> 0.1.13-1
- New upstream release
- Autofoo for the new vala api versioning

* Tue Aug  3 2010 Yanko Kaneti <yaneti@declera.com> 0.1.12-1
- New upstream release

* Mon Aug  2 2010 Yanko Kaneti <yaneti@declera.com> 0.1.11-1
- Packaged for review
