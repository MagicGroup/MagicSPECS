%define glib2_version 2.33.12
%define pkgconfig_version 0.12
%define freetype_version 2.1.5
%define fontconfig_version 2.10.91
%define cairo_version 1.7.6
%define libthai_version 0.1.9
%define harfbuzz_version 0.9.9
%define bin_version 1.8.0

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.33.7
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/pango
Source: http://download.gnome.org/sources/pango/1.33/pango-%{version}.tar.xz
URL: http://www.pango.org

Requires: glib2 >= %{glib2_version}
Requires: freetype >= %{freetype_version}
Requires: freetype >= %{freetype_version}
Requires: cairo >= %{cairo_version}
Requires: libthai >= %{libthai_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: libXft-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: libthai-devel >= %{libthai_version}
BuildRequires: harfbuzz-devel >= %{harfbuzz_version}
BuildRequires: gobject-introspection-devel
BuildRequires: cairo-gobject-devel
# Bootstrap requirements
BuildRequires: gnome-common intltool gtk-doc

%description
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package devel
Summary: Development files for pango
Group: Development/Libraries
Requires: pango%{?_isa} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: cairo-devel >= %{cairo_version}

%description devel
The pango-devel package includes the header files and developer documentation
for the pango package.

%prep
%setup -q -n pango-%{version}

%build

# We try hard to not link to libstdc++
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
          --enable-doc-cross-references \
          --with-included-modules=basic-fc )
make %{?_smp_mflags}


%install

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.la

PANGOXFT_SO=$RPM_BUILD_ROOT%{_libdir}/libpangoxft-1.0.so
if ! test -e $PANGOXFT_SO; then
        echo "$PANGOXFT_SO not found; did not build with Xft support?"
        ls $RPM_BUILD_ROOT%{_libdir}
        exit 1
fi

# We need to have separate 32-bit and 64-bit pango-querymodules binaries
# for places where we have two copies of the Pango libraries installed.
# (we might have x86_64 and i686 packages on the same system, for example.)
mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules $RPM_BUILD_ROOT%{_bindir}/pango-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/pango/%{bin_version}/modules.cache

%post
/sbin/ldconfig
/usr/bin/pango-querymodules-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
if test $1 -gt 0; then
  /usr/bin/pango-querymodules-%{__isa_bits} --update-cache || :
fi

%files
%doc README AUTHORS COPYING NEWS
%doc pango-view/HELLO.txt
%{_libdir}/libpango*-*.so.*
%{_bindir}/pango-querymodules*
%{_bindir}/pango-view
%{_mandir}/man1/pango-view.1.gz
%{_mandir}/man1/pango-querymodules.1.gz
%{_libdir}/pango
%ghost %{_libdir}/pango/%{bin_version}/modules.cache
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib


%files devel
%{_libdir}/libpango*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/pango
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir
%{_datadir}/gir-1.0/PangoXft-1.0.gir


%changelog
* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 1.33.7-1
- Update to 1.33.7

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 1.32.6-1
- Update to 1.32.6

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.32.5-1
- Update to 1.32.5

* Wed Nov 21 2012 Richard Hughes <hughsient@gmail.com> - 1.32.3-1
- Update to 1.32.3

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 1.32.2-1
- Update to 1.32.2

* Thu Sep 27 2012 Matthias Clasen <mclasen@redhat.com> - 1.32.1-1
- Update to 1.32.1
- Move module cache file to /usr/lib64/pango/1.8.0/modules.cache
- No more /etc/pango

* Sat Aug 25 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.31.0-3
- Fix %%postun error on multilib erase (#684729).

* Wed Aug 22 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 1.31.0-2
- Add missing BR:harfbuzz-devel
- Remove file pangox.aliases as pangox support is now removed

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.31.0-1
- Update to 1.31.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 1.30.1-1
- Update to 1.30.1

* Sat May 19 2012 Matthias Clasen <mclasen@redhat.com> - 1.30.0-2
- Fix up scriptlet dependencies (#684729)

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 1.30.0-1
- Update to 1.30.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.29.5-1
- Update to 1.29.5

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 1.29.4-1
- Update to 1.29.4

* Wed Aug 17 2011 Kalev Lember <kalevlember@gmail.com> - 1.29.3-2
- Fix a crash in the fallback engine

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.29.3-1
- Update to 1.29.3

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.28.4-2
- Stop using G_CONST_RETURN

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 1.28.4-1
- Update to 1.28.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.3-1
- Update 1.28.3

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.1-6
- Rebuild against newer gobject-introspection

* Fri Sep 03 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.28.1-5
- Merge Review cleanup (rh#226229)

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.28.1-4
- Rebuild for new gobject-introspection

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 1.28.1-3
- Remove usage of chrpath, should no longer be needed

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 1.28.1-2
- Support builds from snapshots

* Tue Jun 15 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.1-1
- Update to 1.28.1

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.0-2
- Enable introspection

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.0-1
- Update to 1.28.0

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 1.27.1-1
- Update to 1.27.1

* Wed Dec 16 2009 Matthias Clasen <mclasen@redhat.com> - 1.26.2-1
- Update to 1.26.2
- See http://download.gnome.org/sources/pango/1.26/pango-1.26.2.news

* Thu Dec  3 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.26.1-1
- 1.26.1

* Mon Sep 21 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.26.0-1
- 1.26.0

* Tue Sep  8 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.6-1
- 1.25.6

* Mon Aug 24 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.5-1
- 1.25.5

* Thu Aug 20 2009 Karsten Hopp <karsten@redhat.com> 1.25.4-2
- fix autoconf host on s390x

* Tue Aug 17 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.4-1
- 1.25.4

* Tue Aug 11 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.3-1
- 1.25.3

* Tue Aug 11 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.2-1
- 1.25.2

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-7
- Yes, I am stupid.

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-6
- One more try

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-5
- Remove -fexceptions from CXXFLAGS actually
- Hopefully builds this time

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-4
- Remove -fexceptions from RPM_OPT_FLAGS
- Hopefully builds this time

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-3
- Remove pango-1.25.1-no-hb-main.patch
- Add pango-1.25.1-cxx.patch
- Hopefully builds this time

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-2
- Add pango-1.25.1-no-hb-main.patch to fix build on x86-64

* Mon Aug 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.25.1-1
- Update to 1.25.1

* Wed Jul 22 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.24.5-1
- Update to 1.24.5

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> - 1.24.4-1
- Update to 1.24.4

* Wed Jun 24 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.24.3-1
- Update to 1.24.3

* Fri May 15 2009 Karsten Hopp <karsten@redhat.com> 1.24.2-1
- Update to 1.24.2
- See http://download.gnome.org/sources/pango/1.24/pango-1.24.2.news

* Sat Apr 18 2009 Karsten Hopp <karsten@redhat.com> 1.24.1-1.1
- autoconf uses ibm-linux not redhat-linux (s390x)

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 1.24.1-1
- Update to 1.24.1
- See http://download.gnome.org/sources/pango/1.24/pango-1.24.1.news

* Wed Mar 26 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.24.0-2
- Remove weird Requires(pre).
- Resolves #486641

* Mon Mar 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.24.0-1
- Update to 1.24.0
- Package pango-view.1.gz

* Wed Mar 11 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.23.0-4.g5317893
- Push changes from git

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Behdad Esfahbod <besfahbo@redhat.com> - 1.23.0-2
- Move pango-view from pango-devel to pango

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 1.23.0-1
- Update to 1.23.0

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.4-1
- Update to 1.22.4

* Sun Dec  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.22.3-2
- Rebuild for pkgconfig provides

* Mon Nov 24 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.3-1
- Update to 1.22.3

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.2-1
- Update to 1.22.2

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.1-1
- Update to 1.22.1

* Mon Sep 22 2008 Behdad Esfahbod <besfahbo@redhat.com> - 1.22.0-1.1
- Rebuild against cairo 1.7.6
- Update cairo and glib required versions

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.6-1
- Update to 1.21.6

* Mon Aug 26 2008 Behdad Esfahbod <besfahbo@redhat.com> - 1.21.5-1
- Update to 1.21.5

* Mon Aug 11 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.4-1
- Update to 1.21.4

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.3-1
- Update to 1.21.3

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.2-1
- Update to 1.21.2

* Mon May 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.21.1-2
- add sparc64 to multilib handling

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.1-1
- Update to 1.21.1

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.0-1
- Update to 1.21.0

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.20.1-1
- Update to 1.20.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 1.20.0-1
- Update to 1.20.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 1.19.4-1
- Update to 1.19.4

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.19.3-3
- Autorebuild for GCC 4.3

* Mon Jan 29 2008 Behdad Esfahbod <besfahbo@redhat.com> - 1.19.3-2
- Bump libthai requirement.

* Mon Jan 21 2008 Behdad Esfahbod <besfahbo@redhat.com> - 1.19.3-1
- Update to 1.19.3

* Tue Dec 18 2007 Matthias Clasen <mclasne@redhat.com> - 1.19.2-1
- Update to 1.19.2

* Thu Dec  6 2007 Matthias Clasen <mclasne@redhat.com> - 1.19.1-1
- Update to 1.19.1

* Wed Oct 31 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.19.0-1
- Update to 1.19.0

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.3-1
- Update to 1.18.3 (make Nafees Nastaliq font work)

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.2-1
- Update to 1.18.2

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.1-1
- Update to 1.18.1

* Thu Aug 23 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.17.5-3
- Rebuild for PPC toolchain bug

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.5-2
- Update license field
- Don't install ChangeLog

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.5-1
- Update to 1.17.5

* Tue Jul 03 2007 Behdad Esfahbod <besfahbo@redhat.com>
- Distribute NEWS

* Mon Jul  2 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.4-1
- Update to 1.17.4

* Mon Jul  2 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.3-1
- Update to 1.17.3
- Drop ancient Obsoletes

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Mon May 28 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.1-1
- Update to 1.17.1

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.0-1
- Update to 1.17.0

* Fri Apr 10 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.16.4-1
- Update to 1.16.4.
- Enable doc rebuilding to get cross-references right.

* Tue Apr 10 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.16.2-1
- Update to 1.16.2.

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.16.1-1
- Update to 1.16.1

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.15.6-1
- Update to 1.15.6

* Mon Jan 22 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.5-1
- Update to 1.15.5.
- Drop upstreamed pango-1.15.4-slighthint.patch

* Wed Jan 18 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.4-5
- Again... HELLO.txt is moved.

* Wed Jan 18 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.4-4
- Bump again.  I accidentally tagged 1.15.3-4 as 1.15.4-3 previously :(.

* Wed Jan 18 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.4-3
- s/HELLO.utf8/HELLO.txt/ to match upstream.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.4-2
- Update slighthint patch to apply.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.4-1
- Update to 1.15.4
- [Build]Require libthai[-devel]
- Require pkgconfig in -devel
- Remove "static libs" from -devel description, since we don't ship them.

* Fri Jan 12 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.3-5
- Require pango = %%{version}-%%{release} in devel (previously didn't have
  releaes).

* Thu Jan 11 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.3-4
- Undo the posttrans change.  That's a no no.  We now regenerate the module
  file in postun if there are any other pango versions left.  This should
  take care of the problem in the future.

* Thu Jan 11 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.3-3
- Move pango.modules generation to posttrans, to make sure modules available
  in an older version but not this one are removed.
- Resolves #222217

* Tue Jan 09 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.3-2
- Update sources

* Tue Jan 09 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1.15.3-1
- Update to 1.15.3
- Pass --with-included-modules=basic-fc.  Saves one page of memory per process.

* Tue Dec 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.15.2-1
- Update to 1.15.2

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 1.15.0-1
- Update to 1.15.0

* Thu Oct 12 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.6-1
- Update to 1.14.6

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.14.4-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.4-2
- Remove illegal g_object_unref().

* Fri Sep 15 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.4-1
- Update to 1.14.4
- Fixes bugs 198136, 306388, 206390
- Remove upstreamed patch

* Tue Sep 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.14.3-2
- Fix Hangul decomposition issues (#206044)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.14.3-1
- Update to 1.14.3

* Tue Aug 22 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.14.1-1.fc6
- Update to 1.14.1

* Thu Aug 17 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.0-3
- Bump glib requirement to 2.12.0. (bug #201586)

* Wed Aug 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.0-2
- Incorrect sources in last update.  Fix.

* Wed Aug 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Wed Aug 02 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.13.5-1
- Update to 1.13.5

* Mon Jul 27 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.13.4-2
- Add umask 022 to post (#185419)

* Tue Jul 25 2006 Matthias Clasen <mclasen@redhat.com> - 1.13.4-1
- Update to 1.13.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.13.3-1.1
- rebuild

* Mon Jul 10 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.13.3-1
- Update to 1.13.3

* Thu Jun 15 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.13.2-1
- Update to 1.13.2

* Sun May 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.13.1-3
- Add missing BuildRequires (#191958)

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> - 1.13.1-2
- Update to 1.13.1

* Mon May  8 2006 Matthias Clasen <mclasen@redhat.com> - 1.13.0-1
- Update to 1.13.0

* Fri Apr  7 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.1-2
- Update to 1.12.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Sun Feb 26 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.99-1
- Update to 1.11.99

* Tue Feb 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.6-1
- Upate to 1.11.6
- Drop upstreamed patches

* Fri Feb 17 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.5-2
- Fix a crash in pango_split
- Hide some private API

* Mon Feb 11 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.5-1
- Update to 1.11.5

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.11.4-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.11.4-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.4-1
- Update to 1.11.4

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.3-1
- Update to 1.11.3

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Wed Dec 19 2005 Matthias Clasen <mclasen@redhat.com> - 1.11.1-2
- BuildRequire cairo-devel

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Tue Nov 29 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> - 1.10.1-6
- switch prereqs to modular X

* Fri Nov  4 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.1-5
- Switch buildrequires to modular X.
- Don't install .la files for modules.

* Thu Oct 27 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.1-2
- Bump the requirement for glib (#165928)

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.1-1
- Newer upstream version
- Use the docs which are included in the tarball

* Wed Aug 17 2005 Owen Taylor <otaylor@redhat.com> - 1.10.0-1
- Upgrade to 1.10.0

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> 1.9.1-2
- Patch out libpixman dependency.

* Thu Jul 28 2005 Owen Taylor <otaylor@redhat.com> 1.9.1-1
- Update to 1.9.1

* Tue Jun 21 2005 Matthias Clasen <mclasen@redhat.com> 
- Add a missing requires

* Tue Jun 21 2005 Matthias Clasen <mclasen@redhat.com> 1.9.0-1
- Update to 1.9.0
- Require cairo

* Fri Mar  4 2005 Owen Taylor <otaylor@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Tue Dec 21 2004 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- Version 1.8.0
- Drop unneeded patches and hacks

* Wed Oct 20 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-7
- Fix problem with pango_layout_get_attributes returning one too few items
  (Needed to fix problems mentioned in #135656, 
  http://bugzilla.gnome.org/show_bug.cgi?id=155912)

* Tue Oct 19 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-6
- Make Hangul and Kana not backspace-deletes-char (#135356)

* Tue Oct 19 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-5
- Fix problem in the last patch where we weren't getting the metrics from the 
  right font description (#136428, Steven Lawrance)

* Mon Oct 18 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-4
- Move place where we compute fontset metrics to fix problems with line 
  height in CJK locales (#131218)

* Mon Oct 11 2004 Colin Walters <walters@redhat.com> - 1.6.0-3
- BR xorg-x11-devel instead of XFree86-devel

* Mon Sep 20 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-2
- Add patch from CVS to fix display of U+3000 (#132203,  
  reported upstream by Suresh Chandrasekharan, Federic Zhang)

* Mon Sep 20 2004 Owen Taylor <otaylor@redhat.com> - 1.6.0-1
- Version 1.6.0
- Add patch from CVS to fix bitmap-fonts/no-hint problem (#129246)

* Wed Sep  8 2004 Jeremy Katz <katzj@redhat.com> - 1.5.2-3
- fix running of pango-query-modules to have necessary libraries available
  (#132052)

* Mon Aug 16 2004 Owen Taylor <otaylor@redhat.com> - 1.5.2-2
- Fix crashes with left-matra fixups (#129982, Jatin Nansi)

* Mon Aug  2 2004 Owen Taylor <otaylor@redhat.com> - 1.5.2-1
- Update to 1.5.2
- Fix ppc/powerpc confusion when creating query-modules binary (#128645)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 17 2004 Owen Taylor <otaylor@redhat.com> 1.4.0-2
- Fix location for modules file on ppc/ppc64 (#114399)
- Make the spec file check to avoid further mismatches

* Wed Mar 17 2004 Alex Larsson <alexl@redhat.com> 1.4.0-1
- update to 1.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 1.3.6-1
- Update to 1.3.6
- Bump required glib2 to 2.3.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Mark McLoughlin <markmc@redhat.com> 1.3.5-1
- Update to 1.3.5

* Wed Feb 25 2004 Mark McLoughlin <markmc@redhat.com> 1.3.3-1
- Update to 1.3.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 1.3.2-1
- new version
- add man page

* Thu Dec 18 2003 Owen Taylor <otaylor@redhat.com> 1.2.5-4
- Deal with autoconf changing -linux to -linux-gnu (#112387)

* Mon Dec  8 2003 Owen Taylor <otaylor@redhat.com> 1.2.5-3.0
- Package pango-querymodules as pango-querymodules-{32,64}; look for 
  pango.modules in an architecture-specific directory.
  (Fixes #111511, Justin M. Forbes)

* Mon Sep  8 2003 Owen Taylor <otaylor@redhat.com> 1.2.5-2.0
- Fix problem with corrupt Thai shaper

* Wed Aug 27 2003 Owen Taylor <otaylor@redhat.com> 1.2.5-1.1
- Version 1.2.5

* Tue Aug 26 2003 Owen Taylor <otaylor@redhat.com> 1.2.4-1.1
- Version 1.2.4

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 1.2.3-2.0
- Bump for rebuild

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com>
- Version 1.2.3

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  2 2003 Owen Taylor <otaylor@redhat.com>
- Use the right version-1.2.2 tarball

* Thu May 29 2003 Owen Taylor <otaylor@redhat.com>
- Version 1.2.2

* Thu Feb 13 2003 Tim Powers <timp@redhat.com> 1.2.1-3
- remove deps on Xft and Xft-devel since XFree86 no longer has the
  virtual prvodes. Instead, require XFree86-devel > 4.2.99

* Tue Feb 11 2003 Owen Taylor <otaylor@redhat.com>
- Fix problem where language tag wasn't causing relookup of font (#84034)

* Sun Feb  2 2003 Owen Taylor <otaylor@redhat.com>
- Version 1.2.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 14 2003 Owen Taylor <otaylor@redhat.com>
- Patch from CVS to synthesize GDEF tables for fonts
  without them, like the Kacst fonts in fonts-arabic

* Thu Jan  9 2003 Owen Taylor <otaylor@redhat.com>
- Make requires freetype, not freetype-devel (#81423)

* Tue Jan  7 2003 Owen Taylor <otaylor@redhat.com>
- Update slighthint patch for freetype-2.1.3 (#81125)

* Fri Dec 20 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.2.0

* Mon Dec 16 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.1.6

* Wed Dec 11 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.1.5

* Tue Dec  3 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.1.4

* Thu Nov 21 2002 Havoc Pennington <hp@redhat.com>
- change PKG_CONFIG_PATH hack to also search /usr/X11R6/lib64/pkgconfig

* Wed Nov 20 2002 Havoc Pennington <hp@redhat.com>
- explicitly require pangoxft to be built, so we catch situations such
  as xft.pc moving to /usr/X11R6
- also add /usr/X11R6/lib/pkgconfig to PKG_CONFIG_PATH as a temporary 
  hack

* Thu Nov  7 2002 Havoc Pennington <hp@redhat.com>
- 1.1.3

* Thu Oct 31 2002 Owen Taylor <otaylor@redhat.com> 1.1.1-5
- Require the necessary freetype version, don't just
  BuildRequires it (#74744)

* Thu Oct 31 2002 Owen Taylor <otaylor@redhat.com> 1.1.1-4
- Own /etc/pango (#73962, Enrico Scholz)
- Remove .la files from the build root

* Mon Oct  7 2002 Havoc Pennington <hp@redhat.com>
- require glib 2.0.6-3, try rebuild on more arches

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.1.1 (main change, fixes font selection for FT2 backend, 
  as in gdmgreeter)

* Thu Aug 15 2002 Owen Taylor <otaylor@redhat.com>
- Fix linked list manipulation problem that was causing hang for anaconda
- Fix warning from loading mini-fonts with context == NULL

* Wed Aug 14 2002 Owen Taylor <otaylor@redhat.com>
- Fix major memory leak in the last patch

* Tue Aug 13 2002 Owen Taylor <otaylor@redhat.com>
- Actually use language tags at the rendering layer (should fix #68211)

* Mon Jul 15 2002 Owen Taylor <otaylor@redhat.com>
- Remove fixed-ltmain.sh, relibtoolize; to fix relink problems without 
- Fix bug causing hex boxes to be misrendered
  leaving RPATH (#66005)
- For FT2 backend, supply FT_LOAD_NO_BITMAP to avoid problems with 
  fonts with embedded bitmaps (#67851)

* Mon Jul  8 2002 Owen Taylor <otaylor@redhat.com>
- Make basic-x shaper work with our big-5 fonts

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- New upstream tarball with hooks for change-on-the fly font rendering

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Up FreeType version to deal with FreeType-2.0.x / 2.1.x \
  ABI changes for pango's OpenType code.

* Mon Jun 24 2002 Owen Taylor <otaylor@redhat.com>
- Add some Korean aliases that the installer wants

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Jun  8 2002 Havoc Pennington <hp@redhat.com>
- devel package requires fontconfig/Xft devel packages

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Jun  6 2002 Owen Taylor <otaylor@redhat.com>
- Snapshot with Xft2/fontconfig support

* Wed May 29 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.0.2
- Patch for charmaps problem

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed May 22 2002 Havoc Pennington <hp@redhat.com>
- add patch to adjust to newer version of freetype

* Wed Apr  3 2002 Alex Larsson <alexl@redhat.com>
- Update to version 1.0.1, remove patch

* Tue Mar 19 2002 Owen Taylor <otaylor@redhat.com>
- Patch from CVS for big speedup with FreeType-2.0.9

* Mon Mar 11 2002 Owen Taylor <otaylor@redhat.com>
- Rebuild

* Fri Mar  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.0.0

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Update to 0.26

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Mon Feb 18 2002 Alex Larsson <alexl@redhat.com>
- Update to 0.25

* Fri Feb 15 2002 Havoc Pennington <hp@redhat.com>
- add horrible buildrequires hack

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 0.24.90 cvs snap

* Tue Jan 29 2002 Owen Taylor <otaylor@redhat.com>
- Version 0.24

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- new snap 0.23.90

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- rebuild with 64-bit-fixed glib

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- Version 0.22
- add explicit check for required glib2 version before we do the build,
  so we don't end up with bad RPMs on --nodeps builds
- PreReq the glib2_version version, instead of 1.3.8 hardcoded that 
  no one had updated recently

* Thu Oct 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 0.21

* Thu Oct  4 2001 Havoc Pennington <hp@redhat.com>
- cvs snap
- new cvs snap with a bugfix

* Thu Sep 27 2001 Havoc Pennington <hp@redhat.com>
- sync with Owen's changes, fix up dependency versions

* Wed Sep 19 2001 Havoc Pennington <hp@redhat.com>
- 0.19

* Mon Sep 10 2001 Havoc Pennington <hp@redhat.com>
- build CVS snap

* Wed Sep 05 2001 Havoc Pennington <hp@redhat.com>
- no relinking junk

* Tue Sep  4 2001 root <root@dhcpd37.meridian.redhat.com>
- Version 0.18

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Configure --disable-gtk-doc
- BuildRequires freetype-devel, XFree86-devel

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- 0.17
- libtool hackarounds

* Fri May 04 2001 Owen Taylor <otaylor@redhat.com>
- 0.16, rename back to pango from pango-gtkbeta

* Fri Feb 16 2001 Owen Taylor <otaylor@redhat.com>
- Obsolete fribidi-gtkbeta

* Mon Dec 11 2000 Havoc Pennington <hp@redhat.com>
- Remove that patch I just put in

* Mon Dec 11 2000 Havoc Pennington <hp@redhat.com>
- Patch pangox.pc.in to include -Iincludedir

* Fri Nov 17 2000 Owen Taylor <otaylor@redhat.com>
- final 0.13

* Tue Nov 14 2000 Owen Taylor <otaylor@redhat.com>
- New 0.13 tarball

* Mon Nov 13 2000 Owen Taylor <otaylor@redhat.com>
- 0.13pre1

* Sun Aug 13 2000 Owen Taylor <otaylor@redhat.com>
- Rename to 0.12b to avoid versioning problems

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- Move to a CVS snapshot

* Fri Jul 07 2000 Owen Taylor <otaylor@redhat.com>
- Move back to /usr
- Version 0.12

* Mon Jun 19 2000  Owen Taylor <otaylor@redhat.com>
- Add missing %%defattr

* Thu Jun 8 2000  Owen Taylor <otaylor@redhat.com>
- Rebuild with a prefix of /opt/gtk-beta

* Wed May 31 2000 Owen Taylor <otaylor@redhat.com>
- version 0.11
- add --without-qt

* Wed Apr 26 2000 Owen Taylor <otaylor@redhat.com>
- Make the devel package require *-gtkbeta-* not the normal packages.

* Tue Apr 25 2000 Owen Taylor <otaylor@redhat.com>
- GTK+ snapshot version installing in /opt/gtk-beta

* Fri Feb 11 2000 Owen Taylor <otaylor@redhat.com>
- Created spec file
