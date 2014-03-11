# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man

%define tde_tdeappdir %{tde_datadir}/applications/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_docdir}


Summary:        Mandriva theme for TDE - Widget design
Name:           trinity-style-ia-ora
Version:        1.0.8
Release:	2%{?dist}%{?_variant}
License:        GPL
Group:          Environment/Desktop
URL:            http://www.mandrivalinux.com/

Source0:        ia_ora-kde-%{version}.tar.bz2

# [ia_ora] Fix automake 1.11 detection
Patch1:		ia_ora-1.08-fix_automake_detection.patch
# [ia_ora] Fix trinity directories detection
Patch2:		ia_ora-1.08-fix_trinity_directories.patch

Prefix:		%{_prefix}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1

Requires:	trinity-twin

%description
Mandriva theme for Trinity

%if 0%{?suse_version}
%debug_package
%endif


%prep
%setup -q -n ia_ora-kde-%{version}
%patch1 -p1 -b .automake11
%patch2 -p1 -b .trinity

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i admin/acinclude.m4.in \
  -e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
  -e "s|kde_htmldir='.*'|kde_htmldir='%{tde_tdedocdir}/HTML'|g"

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common" cvs


%build
unset QTDIR; . /etc/profile.d/qt3.sh
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --disable-rpath \
  --enable-closure \
  --disable-dependency-tracking \
  --enable-new-ldflags \
  --enable-final \
  --enable-shared \
  --disable-static \
  --with-extra-includes=%{tde_includedir}/tqt

%__make %{?_smp_mflags} LIBTOOL=$(which libtool)

%install
%__rm -rf %{buildroot}
%__make install DESTDIR=%{?buildroot}

# Removes useless files
%__rm -f %{?buildroot}%{tde_tdelibdir}/*.a
%__rm -f %{?buildroot}%{tde_tdelibdir}/plugins/styles/*.a

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{tde_tdelibdir}/kwin3_iaora.la
%{tde_tdelibdir}/kwin3_iaora.so
%{tde_tdelibdir}/kwin_iaora_config.la
%{tde_tdelibdir}/kwin_iaora_config.so
%{tde_tdelibdir}/plugins/styles/ia_ora.la
%{tde_tdelibdir}/plugins/styles/ia_ora.so
%{tde_datadir}/apps/kstyle/themes/ia_ora.themerc
%{tde_datadir}/apps/kwin/iaora.desktop




%changelog
* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.8-2
- Initial build for TDE 3.5.13.1

* Fri Aug 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0.8-1
- Initial version for TDE 3.5.13

* Fri Aug 05 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 1.0.8-9mib2011.0
- Port to 2011

* Sat Jul 10 2010 Andrey Bondrov <bondrov@math.dvgu.ru> 1.0.8-8mib2010.1
- Rebuild for MIB users

* Sun Nov 22 2009 Atilla ÖNTAŞ <atilla_ontas@mandriva.org> 1.0.8-8mvt2010.0
- Rename package to avoid unwanted KDE4 upgrade
- Merge packages in one kde-style package
- Fix package group in spec file

* Tue Nov 17 2009 Tim Williams <tim@my-place.org.uk> 1.0.8-7mdv2010.0
+ Rebuild for MDV 2010.0

* Thu Mar 26 2009 Helio Chissini de Castro <helio@mandriva.com> 1.0.8-6mdv2009.1
+ Revision: 361404
- Bump to rebuild against cooker

* Tue Nov 18 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.8-5mdv2009.1
+ Revision: 304189
- rebuild for new xcb

* Wed Aug 06 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.8-4mdv2009.0
+ Revision: 264680
- rebuild early 2009.0 package (before pixel changes)

* Thu May 08 2008 Helio Chissini de Castro <helio@mandriva.com> 1.0.8-2mdv2009.0
+ Revision: 204689
- Move to /opt

* Wed Feb 27 2008 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.8-1mdv2008.1
+ Revision: 175799
- New release (1.0.8):
   * Fix drawing of buttons when using mandriva color schemes
   * Update color scheme names to match the new ones

* Tue Feb 19 2008 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.7-1mdv2008.1
+ Revision: 173100
- new release (1.0.7) fixing some drawing issues on applications that don't use
  standard background colors (#33502)

* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-2mdv2008.1
+ Revision: 141786
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 12 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.6-1mdv2008.0
+ Revision: 84626
- new release: 1.0.6:
   * Use the right color for the bottom line of menubar
   * Remove some lines that were causing double borders at menubar and toolbar
     ends
   * Fix the bottom of toolbars: it was being drawn using the wrong color
   * Use a flat background for status bars
   * Add a minimum size for the scrollbar handle
- new release: 1.0.5
   * Use the widget style in all separators (#33260)
   * Fixed popup menu item drawing on menus that have titles (#33287)

* Thu Sep 06 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.4-1mdv2008.0
+ Revision: 81272
- new version: 1.0.4
   * Restore the old color themes (as they will be kept as alternatives)
   * Properly mask the rounded borders and properly draw the region previously
     masked
   * Create fake rounded corners on menu items
   * Reduced the button margin to get normal sized buttons (not giant ones)
   * Make it possible to resize windows by the top border
------------------------------------------------------------------------
  r227235 | boiko | 2007-09-06 13:58:18 -0300 (Qui, 06 Set 2007) | 3 lines

* Wed Sep 05 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.3-1mdv2008.0
+ Revision: 80378
- new release: 1.0.3
   * Implement highligh on hovering controls
   * Threat scrollbar buttons as buttons (showing them lowered when the button
     is pressed for example)
   * Show the combo box button as pressed when the list is opened
   * Removed Powerpack+ colors
   * Changed Discovery/One to just One and adjusted colors
   * Used more sane values when using ia_ora together with other KDE color
     schemes
- new release:
   * fix gradient colors of menus (thanks Frederic Crozat for pointing that)
   * implement correctly the combo box drawing according to the ia_ora spec
   * Fix the text color of menubar items

* Thu Aug 23 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.1-1mdv2008.0
+ Revision: 70685
- new version: 1.0.1
   * Replace the gradient code by the Plastik one (it is better written)
   * Fix drawing of menubar items and popupmenu items (#30659)

* Mon Jun 11 2007 Nicolas Lécureuil <neoclust@mandriva.org> 1.0-18mdv2008.0
+ Revision: 38004
- REBUILD


* Thu Mar 22 2007 Laurent Montel <lmontel@mandriva.com> 1.0-17mdv2007.1
+ Revision: 147929
- Fix theme

* Mon Mar 19 2007 Laurent Montel <lmontel@mandriva.com> 1.0-16mdv2007.1
+ Revision: 146479
- Fix progressbar text color

* Wed Mar 07 2007 Laurent Montel <lmontel@mandriva.com> 1.0-15mdv2007.1
+ Revision: 134563
- Fix style

* Tue Mar 06 2007 Laurent Montel <lmontel@mandriva.com> 1.0-14mdv2007.1
+ Revision: 133854
- New update

* Wed Feb 28 2007 Laurent Montel <lmontel@mandriva.com> 1.0-13mdv2007.1
+ Revision: 127097
- New update

* Wed Jan 24 2007 Laurent Montel <lmontel@mandriva.com> 1.0-12mdv2007.1
+ Revision: 112737
- Fix theme

* Tue Jan 02 2007 Laurent Montel <lmontel@mandriva.com> 1.0-11mdv2007.1
+ Revision: 103350
- Update tarball

* Mon Dec 11 2006 Laurent Montel <lmontel@mandriva.com> 1.0-10mdv2007.1
+ Revision: 94696
- Rename spec file name too
- Rename ia_ora to ia_ora-kde
  Fix a lot of bug
- Import ia_ora-kde

* Sat Sep 16 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-9
- Fix title bar

* Thu Sep 14 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-8
- Fix handle

* Thu Sep 14 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-7
- Fix toolbar color

* Thu Sep 14 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-6
- Fix Combobox/Scrollbar/Checkbox and bidi mode

* Tue Sep 12 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-5
- Fix tabbar

* Tue Sep 12 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-4
- Fix scrollbar

* Sun Sep 10 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-3
- Improve style

* Fri Sep 08 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-2
- Some fixes

* Tue Sep 05 2006 Laurent MONTEL <lmontel@mandriva.com> 1.0-1
- Initial package

