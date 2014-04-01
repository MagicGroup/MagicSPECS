%global _changelog_trimtime %(date +%s -d "1 year ago")

%define glib2_version 2.36.0
%define gtk3_version 3.4.0
%define gtkhtml_version 4.5.2
%define gnome_desktop_version 2.91.3
%define gnome_doc_utils_version 0.8.0
%define gnome_icon_theme_version 2.30.2.1
%define intltool_version 0.35.5
%define libgdata_version 0.10.0
%define libgweather_version 3.5.0
%define libsoup_version 2.40.3
%define clutter_gtk_version 0.10
%define webkit_version 1.8.0

%define evo_base_version 3.12

%define last_anjal_version 0.3.2-3
%define last_libgal2_version 2:2.5.3-2
%define last_evo_nm_version 3.5.0

%define ldap_support 1
%define libnotify_support 1
%define libpst_support 1

# Coverity scan can override this to 0, to skip checking in gtk-doc generated code
%{!?with_docs: %define with_docs 1}

%define evo_plugin_dir %{_libdir}/evolution/%{evo_base_version}/plugins

### Abstract ###

Name: evolution
Version: 3.11.90
Release: 2%{?dist}
Group: Applications/Productivity
Summary: Mail and calendar client for GNOME
License: GPLv2+ and GFDL
URL: https://wiki.gnome.org/Apps/Evolution
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz

Obsoletes: anjal <= %{last_anjal_version}
Obsoletes: libgal2 <= %{last_libgal2_version}
Obsoletes: evolution-NetworkManager < %{last_evo_nm_version}

### Patches ###

# bad hack
Patch01: evolution-1.4.4-ldap-x86_64-hack.patch

# RH bug #589555
Patch02: evolution-2.30.1-help-contents.patch

## Dependencies ###

Requires: gnome-icon-theme >= %{gnome_icon_theme_version}
Requires: gvfs
Requires: gtkspell3
Requires: highlight

### Build Dependencies ###

BuildRequires: atk-devel
BuildRequires: autoconf >= 2.59
BuildRequires: automake >= 1.9
BuildRequires: cairo-gobject-devel
BuildRequires: clutter-gtk-devel >= %{clutter_gtk_version}
BuildRequires: desktop-file-utils
BuildRequires: evolution-data-server-devel >= %{version}
BuildRequires: gettext
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gnome-common
BuildRequires: gnome-desktop3-devel >= %{gnome_desktop_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
BuildRequires: gnome-icon-theme-devel >= %{gnome_icon_theme_version}
BuildRequires: gnome-online-accounts
BuildRequires: gnutls-devel
BuildRequires: gtk-doc
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gtkhtml3-devel >= %{gtkhtml_version}
BuildRequires: gtkspell3-devel
BuildRequires: highlight
BuildRequires: intltool >= %{intltool_version}
BuildRequires: itstool
BuildRequires: libcanberra-devel
BuildRequires: libgdata-devel >= %{libgdata_version}
BuildRequires: libgweather-devel >= %{libgweather_version}
BuildRequires: libpst-devel
BuildRequires: libsoup-devel >= %{libsoup_version}
BuildRequires: libtool >= 1.5
BuildRequires: libxml2-devel
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: pkgconfig
BuildRequires: webkitgtk3-devel >= %{webkit_version}
BuildRequires: yelp-tools

%if %{ldap_support}
BuildRequires: openldap-devel >= 2.0.11 
%endif

%if %{libnotify_support}
BuildRequires: libnotify-devel
%endif

%if %{libpst_support}
BuildRequires: libpst-devel
%endif

%description
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The components which make up Evolution
are tightly integrated with one another and act as a seamless
personal information-management tool.

%package devel
Group: Development/Libraries
Summary: Development files for building against %{name}
Requires: %{name} = %{version}-%{release}
Requires: evolution-data-server-devel >= %{version}
Requires: gtk3-devel >= %{gtk3_version}
Requires: gtkhtml3-devel >= %{gtkhtml_version}
Requires: gtkspell3-devel
Requires: libgdata-devel >= %{libgdata_version}
Requires: libgweather-devel >= %{libgweather_version}
Requires: libsoup-devel >= %{libsoup_version}
Requires: libxml2-devel
Obsoletes: libgal2-devel <= %{last_libgal2_version}

%description devel
Development files needed for building things which link against %{name}.

%package devel-docs
Summary: Developer documentation for Evolution
Group: Development/Libraries
Requires: devhelp
Requires: evolution-devel = %{version}-%{release}
BuildArch: noarch

%description devel-docs
This package contains developer documentation for Evolution.

%if %{with_docs}
%package help
Group: Applications/Productivity
Summary: Help files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: yelp
BuildArch: noarch

%description help
This package contains user documentation for %{name}. 
%endif

%package bogofilter
Group: Applications/Productivity
Summary: Bogofilter plugin for Evolution
Requires: %{name} = %{version}-%{release}
Requires: bogofilter
BuildRequires: bogofilter

%description bogofilter
This package contains the plugin to filter junk mail using Bogofilter.

%package spamassassin
Group: Applications/Productivity
Summary: SpamAssassin plugin for Evolution
Requires: %{name} = %{version}-%{release}
Requires: spamassassin
BuildRequires: spamassassin

%description spamassassin
This package contains the plugin to filter junk mail using SpamAssassin.

%package perl
Group: Applications/Productivity
Summary: Supplemental utilities that require Perl
Requires: %{name} = %{version}-%{release}

%description perl
This package contains supplemental utilities for %{name} that require Perl.

%if %{libpst_support}
%package pst
Group: Applications/Productivity
Summary: PST importer plugin for Evolution
Requires: %{name} = %{version}-%{release}

%description pst
This package contains the plugin to import Microsoft Personal Storage Table
(PST) files used by Microsoft Outlook and Microsoft Exchange.
%endif

%prep
%setup -q -n evolution-%{version}
%patch01 -p1 -b .ldaphack
%patch02 -p1 -b .help-contents

# Remove the welcome email from Novell
for inbox in mail/default/*/Inbox; do
  echo -n "" > $inbox
done

%build
# define all of our flags, this is kind of ugly :(
%if %{ldap_support}
%define ldap_flags --with-openldap=yes
%else
%define ldap_flags --without-openldap
%endif

%define ssl_flags --enable-nss=yes --enable-smime=yes

if ! pkg-config --exists nss; then 
  echo "Unable to find suitable version of mozilla nss to use!"
  exit 1
fi

%if %{with_docs}
%define gtkdoc_flags --enable-gtk-doc
%else
%define gtkdoc_flags --disable-gtk-doc
%endif

CPPFLAGS="-I%{_includedir}/et"; export CPPFLAGS
CFLAGS="$RPM_OPT_FLAGS -fPIC -DLDAP_DEPRECATED -I%{_includedir}/et -Wno-sign-compare -Wno-deprecated-declarations"; export CFLAGS

# Regenerate configure to pick up configure.ac changes
aclocal -I m4
autoheader
automake --add-missing
libtoolize
intltoolize --force
autoconf

%configure \
	--disable-maintainer-mode \
	--with-sub-version=" (%{version}-%{release})" \
	%ldap_flags %ssl_flags %gtkdoc_flags \
	--enable-plugins=all
export tagname=CC
make %{?_smp_mflags} LIBTOOL=/usr/bin/libtool CFLAGS="$CFLAGS -fno-strict-aliasing"

%if %{with_docs}

# Strip unneeded translations from .mo files.
# This reduces the RPM size by several megabytes.
cd po
grep -v ".*[.]desktop[.]in[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --gettext-package=%{name}-%{evo_base_version} --pot
for p in *.po; do
	msgmerge $p %{name}-%{evo_base_version}.pot > $p.out
	msgfmt -o `basename $p .po`.gmo $p.out
done
cd -

# Replace identical images in the help by links.
# This reduces the RPM size by several megabytes.
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

# %{with_docs}
%endif

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export tagname=CC
make LIBTOOL=/usr/bin/libtool DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# remove libtool archives for importers and the like
find $RPM_BUILD_ROOT/%{_libdir}/evolution -name '*.la' -exec rm {} \;

# remove statically built libraries:
find $RPM_BUILD_ROOT/%{_libdir}/evolution -name '*.a' -exec rm {} \;

%find_lang evolution-%{evo_base_version} --all-name --with-gnome

grep "/usr/share/locale" evolution-%{evo_base_version}.lang > translations.lang
grep -v "/usr/share/locale" evolution-%{evo_base_version}.lang > help.lang

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files -f translations.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS README

# GSettings schemas:
%{_datadir}/GConf/gsettings/evolution.convert

%{_datadir}/glib-2.0/schemas/org.gnome.evolution.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.shell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.addressbook.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.calendar.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.mail.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.importer.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.bogofilter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.spamassassin.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.attachment-reminder.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.autocontacts.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.email-custom-header.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.external-editor.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.face-picture.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.itip.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.mail-notification.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.prefer-plain.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.publish-calendar.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.evolution.plugin.templates.gschema.xml

# The main executable
%{_bindir}/evolution

%{_datadir}/appdata/evolution.appdata.xml

# Desktop files:
%{_datadir}/applications/evolution.desktop
%{_sysconfdir}/xdg/autostart/evolution-alarm-notify.desktop

# Icons:
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/22x22/apps/*
%{_datadir}/icons/hicolor/24x24/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/256x256/apps/*

# The main data directory
# (have not attempted to split this up into an explicit list)
%dir %{_datadir}/evolution
%{_datadir}/evolution/%{evo_base_version}

# Modules:
%dir %{_libdir}/evolution
%dir %{_libdir}/evolution/%{evo_base_version}
%dir %{_libdir}/evolution/%{evo_base_version}/modules
%{_libdir}/evolution/%{evo_base_version}/modules/module-addressbook.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-backup-restore.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-book-config-google.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-book-config-ldap.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-book-config-local.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-book-config-webdav.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-caldav.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-contacts.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-google.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-local.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-weather.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-cal-config-webcal.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-calendar.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-composer-autosave.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-contact-photos.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-gravatar.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-itip-formatter.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-mail-config.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-mail.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-mailto-handler.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-mdn.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-offline-alert.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-prefer-plain.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-plugin-lib.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-plugin-manager.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-settings.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-startup-wizard.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-text-highlight.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-vcard-inline.so
%{_libdir}/evolution/%{evo_base_version}/modules/module-web-inspector.so

# Shared libraries:
%{_libdir}/evolution/%{evo_base_version}/libevolution-mail-composer.so
%{_libdir}/evolution/%{evo_base_version}/libeabutil.so
%{_libdir}/evolution/%{evo_base_version}/libecontacteditor.so
%{_libdir}/evolution/%{evo_base_version}/libecontactlisteditor.so
%{_libdir}/evolution/%{evo_base_version}/libemail-engine.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-mail-formatter.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-shell.so
%{_libdir}/evolution/%{evo_base_version}/libessmime.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-util.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-addressbook-importers.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-calendar.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-calendar-importers.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-mail-importers.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-mail.so
%{_libdir}/evolution/%{evo_base_version}/libevolution-smime.so
%{_libdir}/evolution/%{evo_base_version}/libgnomecanvas.so

# Various libexec programs:
%dir %{_libexecdir}/evolution
%dir %{_libexecdir}/evolution/%{evo_base_version}
%{_libexecdir}/evolution/%{evo_base_version}/evolution-addressbook-export
%{_libexecdir}/evolution/%{evo_base_version}/evolution-alarm-notify
%{_libexecdir}/evolution/%{evo_base_version}/evolution-backup
%{_libexecdir}/evolution/%{evo_base_version}/killev

# The plugin directory:
%dir %{evo_plugin_dir}

# The various plugins follow; they are all part of the main package:
# (note that there are various resources such as ui and pixmap files that 
# are built as part of specific plugins but which are currently packaged using 
# globs above; the purpose of the separation below is to be more explicit about
# which plugins we ship)
%{evo_plugin_dir}/org-gnome-evolution-attachment-reminder.eplug
%{evo_plugin_dir}/liborg-gnome-evolution-attachment-reminder.so

%{evo_plugin_dir}/org-gnome-email-custom-header.eplug
%{evo_plugin_dir}/liborg-gnome-email-custom-header.so

%{evo_plugin_dir}/org-gnome-evolution-bbdb.eplug
%{evo_plugin_dir}/liborg-gnome-evolution-bbdb.so

%{evo_plugin_dir}/org-gnome-external-editor.eplug
%{evo_plugin_dir}/liborg-gnome-external-editor.so

%{evo_plugin_dir}/org-gnome-face.eplug
%{evo_plugin_dir}/liborg-gnome-face.so

%{evo_plugin_dir}/org-gnome-itip-formatter.eplug
%{evo_plugin_dir}/liborg-gnome-itip-formatter.so

%{evo_plugin_dir}/org-gnome-mailing-list-actions.eplug
%{evo_plugin_dir}/liborg-gnome-mailing-list-actions.so

%{evo_plugin_dir}/org-gnome-mail-notification.eplug
%{evo_plugin_dir}/liborg-gnome-mail-notification.so

%{evo_plugin_dir}/org-gnome-mail-to-task.eplug
%{evo_plugin_dir}/liborg-gnome-mail-to-task.so

%{evo_plugin_dir}/org-gnome-prefer-plain.eplug
%{evo_plugin_dir}/liborg-gnome-prefer-plain.so

%{evo_plugin_dir}/org-gnome-publish-calendar.eplug
%{evo_plugin_dir}/liborg-gnome-publish-calendar.so

%{evo_plugin_dir}/org-gnome-save-calendar.eplug
%{evo_plugin_dir}/liborg-gnome-save-calendar.so

%{evo_plugin_dir}/org-gnome-templates.eplug
%{evo_plugin_dir}/liborg-gnome-templates.so

%{evo_plugin_dir}/org-gnome-dbx-import.eplug
%{evo_plugin_dir}/liborg-gnome-dbx-import.so


%files devel
%defattr(-, root, root)
%{_includedir}/evolution-%{evo_base_version}
%{_libdir}/pkgconfig/evolution-calendar-3.0.pc
%{_libdir}/pkgconfig/evolution-mail-3.0.pc
%{_libdir}/pkgconfig/evolution-plugin-3.0.pc
%{_libdir}/pkgconfig/evolution-shell-3.0.pc
%{_libdir}/pkgconfig/libemail-engine.pc

%files devel-docs
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/evolution-mail-composer
%doc %{_datadir}/gtk-doc/html/evolution-mail-engine
%doc %{_datadir}/gtk-doc/html/evolution-mail-formatter
%doc %{_datadir}/gtk-doc/html/evolution-shell
%doc %{_datadir}/gtk-doc/html/evolution-util

%if %{with_docs}
%files help -f help.lang
%defattr(-, root, root)
%dir %{_datadir}/help/*/evolution
%endif

%files bogofilter
%defattr(-, root, root)
%{_libdir}/evolution/%{evo_base_version}/modules/module-bogofilter.so

%files spamassassin
%defattr(-, root, root)
%{_libdir}/evolution/%{evo_base_version}/modules/module-spamassassin.so

%files perl
%defattr(-, root, root)
%{_libexecdir}/evolution/%{evo_base_version}/csv2vcard

%if %{libpst_support}
%files pst
%defattr(-, root, root)
%{evo_plugin_dir}/org-gnome-pst-import.eplug
%{evo_plugin_dir}/liborg-gnome-pst-import.so
%endif

%changelog
* Wed Feb 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for libgnome-desktop soname bump

* Mon Feb 17 2014 Milan Crha <mcrha@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.5-2
- Drop krb5 dependency

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Fri Jan 17 2014 Adam Williamson <awilliam@redhat.com> - 3.11.4-2
- backport a couple of crasher fixes from upstream master

* Mon Jan 13 2014 Milan Crha <mcrha@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Thu Nov 21 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-2
- Rebuild for new libical (RH bug #1023020)

* Mon Nov 18 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-1
- Update to 3.11.2
- Conditionally build help subpackage
- Disable compiler warnings about deprecated symbols

* Mon Nov 11 2013 Milan Crha <mcrha@redhat.com> - 3.11.1-2
- Hide more help-related widgets when evolution-help is not installed

* Tue Oct 22 2013 Matthew Barnes <mbarnes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 3.10.1-1
- Update to 3.10.1
- Remove the dependency on libytnef, which apparently isn't needed for
  the PST importer and disable the experimental TNEF attachments plugin
- Avoid help launch with F1 when evolution-help is not installed

* Mon Sep 23 2013 Milan Crha <mcrha@redhat.com> - 3.10.0-1
- Update to 3.10.0
- Remove explicit Requires on libpst in pst subpackage

* Mon Sep 16 2013 Milan Crha <mcrha@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-2
- Rebuilt for libgnome-desktop soname bump

* Mon Sep 02 2013 Milan Crha <mcrha@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Fri Aug 23 2013 Milan Crha <mcrha@redhat.com> - 3.9.90-2
- Split developer documentation into evolution-devel-docs subpackage

* Mon Aug 19 2013 Milan Crha <mcrha@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 3.9.5-3
- rebuild for new libgweather

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 3.9.5-2
- Perl 5.18 rebuild

* Mon Jul 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Wed Jul 17 2013 Matthew Barnes <mbarnes@redhat.com> - 3.9.4-3
- Work around a crash caught by -fstack-protector-strong.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.9.4-2
- Perl 5.18 rebuild

* Mon Jul 08 2013 Milan Crha <mcrha@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Sat Jun 22 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.3-3
- Don't install ChangeLog
- Trim %%changelog

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-2
- Rebuilt for libgweather 3.9.3 soname bump

* Mon Jun 17 2013 Milan Crha <mcrha@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Mon May 27 2013 Milan Crha <mcrha@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Fri May 24 2013 Rex Dieter <rdieter@fedoraproject.org> 3.9.1-2
- rebuild (libical)

* Mon Apr 29 2013 Milan Crha <mcrha@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Mon Mar 25 2013 Milan Crha <mcrha@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Rebuilt for libgnome-desktop soname bump

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Mon Feb 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Fri Jan 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-1
- Correct help-context patch test path (Red Had bug #901341)

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-1
- Update to 3.7.4
- Add --add-missing to automake call

* Tue Jan 01 2013 Matthew Barnes <mbarnes@redhat.com> - 3.7.3.2-3
- Re-enable translation size reduction (RH bug #628073 is long fixed).

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3.2-2
- Rebuilt for libgnome-desktop3 3.7.3 soname bump

* Wed Dec 19 2012 Matthew Barnes <mbarnes@redhat.com> - 3.7.3.2-1
- Update to 3.7.3.2
- Remove obsolete BuildRequires:
    bison
    dbus-glib-devel
    libSM-devel
    rarian-compat

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Matthew Barnes <mbarnes@redhat.com> - 3.7.1-2
- Drop unique3-devel BR, it's an ancient artifact.

* Mon Oct 22 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Mon Sep 24 2012 Matthew Barnes <mbarnes@redhat.com> - 3.6.0-1
- Update to 3.6.0
- Remove patch for GNOME #678408 (fixed upstream).

* Mon Sep 24 2012 Bastien Nocera <bnocera@redhat.com> 3.5.92-4
- Use GStreamer 1.0 instead of 0.10

* Sat Sep 22 2012 Adam Williamson <awilliam@redhat.com> - 3.5.92-3
- backport fix for BGO #678408 (broken message display)

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-2
- Fix evolution-NetworkManager obsoletes

* Mon Sep 17 2012 Milan Crha <mcrha@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Mon Sep 03 2012 Milan Crha <mcrha@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Mon Aug 20 2012 Milan Crha <mcrha@redhat.com> - 3.5.90-1
- Update to 3.5.90
- Remove patches for BGO #678408 and #681321 (fixed upstream)
- Add itstool and yelp-tools into BuildRequires

* Wed Aug 15 2012 Adam Williamson <awilliam@redhat.com> - 3.5.5-2
- backport the fix for BGO #678408 and #681321 (libxml2 build)

* Mon Aug 06 2012 Milan Crha <mcrha@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-1
- Update to 3.5.4
- Enable weather plugin (fixed upstream)

* Wed Jun 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.5.3.1-4
- Temporarily disable weather plugin (not ported to new libgweather yet)

* Tue Jun 26 2012 Matthew Barnes <mbarnes@redhat.com> - 2.5.3.1-3
- Temporarily change e-d-s req in devel subpackage.

* Tue Jun 26 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3.1-2
- Remove unnecessary Requires: evolution-data-server.

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3.1-1
- Update to 3.5.3.1 (3.5.3, no build for you!)

* Mon Jun 25 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-1
- Update to 3.5.3
- Drop BR: GConf2-devel  \o/

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-2
- Rebuild against new gnome-desktop

* Mon Jun 04 2012 Milan Crha <mcrha@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Sun Apr 29 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.1-1
- Update to 3.5.1
- Add BR: webkitgtk3-devel

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Mon Apr 16 2012 Milan Crha <mcrha@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Milan Crha <mcrha@redhat.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Mon Mar 19 2012 Milan Crha <mcrha@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Tue Mar 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Mon Feb 20 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Mon Feb 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Thu Jan 19 2012 Matthew Barnes <mbarnes@redhat.com> - 3.3.4-2
- Keep all GSettings schema files in the main evolution package, even the
  ones for the Bogofilter and Spamassassin subpackages, since we just have
  one .convert file and missing schemas makes gsettings-data-convert crash.

* Mon Jan 16 2012 Milan Crha <mcrha@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Milan Crha <mcrha@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Nov 21 2011 Milan Crha <mcrha@redhat.com> - 3.3.2-1
- Update to 3.3.2
- Remove patch to not call g_thread_init() (fixed upstream)

* Fri Oct 28 2011 Matthew Barnes <mbarnes@redhat.com> - 3.3.1-2
- Fix detection of evolution-help (not using OMF files anymore).

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-1
- Update to 3.3.1
- Add patch to not call g_thread_init()

* Mon Sep 26 2011 Milan Crha <mcrha@redhat.com> - 3.2.0-1
- Update to 3.2.0
- Manage properly schemas files for evolution-bogofilter/spamassassin

* Mon Sep 19 2011 Milan Crha <mcrha@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Sep 05 2011 Milan Crha <mcrha@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Aug 15 2011 Milan Crha <mcrha@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Sat Jul 23 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.3-1
- Update to 3.1.3
- Remove patch for building against libgdata-0.9.0 (fixed upstream).

* Wed Jun 15 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-2
- Rebuild against newer gnome-desktop3

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Add patch by Philip Withnall to build against libgdata-0.9.0
- Add patch to enable GLib deprecated stuff (due to G_CONST_RETURN deprecation)

* Tue May 17 2011 Milan Crha <mcrha@redhat.com> - 3.1.1-3
- Keep libevolution-mail-settings.so* from the previous change,
  it is still used by other parts of evolution.

* Mon May 09 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.1-2
- Drop the "Email Settings" capplet.

* Mon May 09 2011 Milan Crha <mcrha@redhat.com> - 3.1.1-1
- Update to 3.1.1
- Drop groupwise plugin, as it was split out upstream

* Mon Apr 04 2011 Milan Crha <mcrha@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar 14 2011 Matthew Barnes <mbarnes@redhat.com> - 2.91.91-3
- Remove some unnecessary BuildRequires:
  gtkimageview-devel: No release available for gtk3.
  libgnomecanvas-devel: Evolution bundles its own libgnomecanvas now.

* Fri Mar 11 2011 Matthew Barnes <mbarnes@redhat.com> - 2.91.91-2
- Split off an evolution-NetworkManager subpackage containing the NM
  integration module.  Users that choose to bypass NetworkManager can
  uninstall this subpackage so Evolution doesn't insist it's offline.

* Mon Mar 07 2011 Milan Crha <mcrha@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthew Barnes <mbarnes@redhat.com> - 2.91.6.2-1
- Update to 2.91.6.2
- Fixes build breakage when using GTK+ 3.0.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Matthew Barnes <mbarnes@redhat.com> - 2.91.6.1-2
- Evolution uses gtk3 now; re-enable libnotify.

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6.1-1
- Update to 2.91.6.1

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-1
- Update to 2.91.6
- Require gtk3
- Remove patch for Red Hat bug #657254 (fixed upstream)

* Fri Jan 21 2011 Dan Williams <dcbw@redhat.com> - 2.91.5-4
- Fix crash at shutdown by finishing tasks before cleaning up (rh #657254)

* Tue Jan 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-3
- Rebuild against newer libgdata

* Thu Jan 13 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Drop gnome-themes dependency

* Mon Jan 10 2011 Milan Crha <mcrha@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Mon Dec 20 2010 Milan Crha <mcrha@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Mon Nov 29 2010 Milan Crha <mcrha@redhat.com> - 2.91.3-1
- Update to 2.91.3
- Remove patch for Red Hat bug #176400 (fixed upstream)

* Mon Nov 08 2010 Milan Crha <mcrha@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Fri Nov 05 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-3
- Rebuild against newer libxml2
- Disable libnotify, it's gtk3 only, but evolution is not

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-2
- Rebuild against new libnotify

* Mon Oct 18 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 2.91.0-1
- Update to 2.91.0
- Remove patch for Gnome bug #626066 (fixed upstream)

* Wed Sep 29 2010 jkeating - 2.31.92-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Milan Crha <mcrha@redhat.com> - 2.31.92-2.fc15
- Add patch for Gnome bug #626066 (login to NSS on demand)

* Mon Sep 13 2010 Milan Crha <mcrha@redhat.com> - 2.31.92-1.fc15
- Update to 2.31.92

* Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 2.31.91-1.fc14
- Update to 2.31.91
- Remove msgmerge calls due to a floating point exception there

* Mon Aug 16 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.90-1.fc14
- Update to 2.31.90

* Fri Aug 06 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.6-2.fc14
- Fix handling of migrated signature files.

* Tue Aug 03 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.6-1.fc14
- Update to 2.31.6
- Drop dbus-glib requirement.
- Bump glib2 requirement to 2.25.12.
- Roll back evo_base_version to 2.32.
- Add clutter-gtk requirement (for express mode).
- Remove gtk-compat macro patch (fixed upstream).

* Thu Jul 22 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.5-2.fc14
- Add patch to fix startup crash in gtk-compat macros.

* Tue Jul 13 2010 Milan Crha <mcrha@redhat.com> - 2.31.5-1.fc14
- Update to 2.31.5
- Remove 'conduit' (removed upstream)

* Mon Jun 07 2010 Milan Crha <mcrha@redhat.com> - 2.31.3-1.fc14
- Update to 2.31.3

* Fri May 28 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.2-2.fc14
- Evolution Express supercedes Anjal.
- No need to undefine GNOME_DISABLE_DEPRECATED.
- Remove nntp_support flag; that got moved to E-D-S ages ago.
- Remove exchange_support flag; it's all in evolution-exchange now.

* Mon May 24 2010 Milan Crha <mcrha@redhat.com> - 2.31.2-1.fc14
- Update to 2.31.2
- Bump gtkhtml3 requirement to 3.31.2

* Fri May 07 2010 Matthew Barnes <mbarnes@redhat.com> - 2.31.1-2.fc14
- Require yelp in evolution-help (RH bug #589555).
- Add patch for RH bug #589555 (hide Help->Contents if evolution-help
  is not installed).

* Mon May 03 2010 Milan Crha <mcrha@redhat.com> - 2.31.1-1.fc14
- Update to 2.31.1

* Tue Feb 09 2010 Milan Crha <mcrha@redhat.com> - 2.29.90-2.fc13
- Rebuild against evolution-data-server-2.29.90-3

* Mon Feb 08 2010 Milan Crha <mcrha@redhat.com> - 2.29.90-1.fc13
- Update to 2.29.90
- Removed unneeded BuildRequires.

* Fri Jan 29 2010 Matthew Barnes <mbarnes@redhat.com> - 2.29.6-2.fc13
- Bump gtkhtml3 requirement to 3.29.6.

* Mon Jan 25 2010 Milan Crha <mcrha@redhat.com> - 2.29.6-1.fc13
- Update to 2.29.6
- Remove patch for Gnome bug #606874 (fixed upstream).
- Add rarian-compat to BuildRequires for Scrollkeeper.

* Mon Jan 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-2.fc13
- Rebuild against new gnome-desktop

* Tue Jan 12 2010 Milan Crha <mcrha@redhat.com> - 2.29.5-1.fc13
- Update to 2.29.5
- Add patch for Gnome bug #606874 (mktemp removed in glibc-2.11.90-8)

* Tue Dec 22 2009 Matthew Barnes <mbarnes@redhat.com> - 2.29.4-2.fc13
- Update Scrollkeeper and Icon Cache scriptlets to conform to guidelines.
  (see: http://fedoraproject.org/wiki/Packaging:ScriptletSnippets)

* Mon Dec 21 2009 Milan Crha <mcrha@redhat.com> - 2.29.4-1.fc13
- Update to 2.29.4
- Remove patch for missing m4 files from tarball (fixed upstream).

* Mon Nov 30 2009 Milan Crha <mcrha@redhat.com> - 2.29.3-1.fc13
- Update to 2.29.3
- Add patch for missing m4 files from tarball.
- Disable autoreconf call.

* Tue Nov 17 2009 Matthew Barnes <mbarnes@redhat.com> - 2.29.2-1.fc13
- Update to 2.29.2
- Synchronize spec file with my kill-bonobo test package.

* Tue Oct 27 2009 Matthew Barnes <mbarnes@redhat.com> - 2.29.1-1.fc13
- Update to 2.29.1
- Bump evo_major to 2.30.
- Drop Bonobo + ORBit dependency (yay!).
- Remove option to use OpenSSL instead of NSS.
- Uninstall GConf schemas during %%pre and %%preun.

* Mon Sep 21 2009 Milan Crha <mcrha@redhat.com> - 2.28.0-1.fc12
- Update to 2.28.0

* Mon Sep 07 2009 Milan Crha <mcrha@redhat.com> - 2.27.92-1.fc12
- Update to 2.27.92

* Mon Aug 24 2009 Milan Crha <mcrha@redhat.com> - 2.27.91-1.fc12
- Update to 2.27.91
- Remove patch for GNOME bug #591414 (fixed upstream).

* Fri Aug 14 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.90-3.fc12
- Add patch for GNOME bug #591414 (calendar library linked as module).

* Tue Aug 11 2009 Milan Crha <mcrha@redhat.com> - 2.27.90-2.fc12
- Build requires gnome-desktop-devel >= 2.26
- New library libevolution-cal-shared.so

* Mon Aug 10 2009 Milan Crha <mcrha@redhat.com> - 2.27.90-1.fc12
- Update to 2.27.90

* Tue Jul 28 2009 Milan Crha <mcrha@redhat.com> - 2.27.5-3.fc12
- Enable pst-import plugin (RH bug #493049)

* Tue Jul 28 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.5-2.fc12
- Move libeconduit.so into the conduits subpackage to see if that
  untangles us from gnome-pilot.

* Mon Jul 27 2009 Milan Crha <mcrha@redhat.com> - 2.27.5-1.fc12
- Update to 2.27.5
- Remove pst import plugin patch (fixed upstream).
- Remove work around deprecation of g_mount_unmount (fixed upstream).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.4-1.fc12
- Update to 2.27.4
- Work around deprecation of g_mount_unmount().

* Fri Jul 10 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.3-5.fc11
- Add an evolution-pst subpackage for the PST importer plugin.
- Disabled until libpst settles on an API.

* Thu Jul 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.3-4.fc12
- Add BR for libpst-devel and libytnef-devel (RH bug #493049).
- Add patch to build pst-import plugin against current libpst.
- libpst's API broke again so disable the BR's for now.
- Specify the gettext package when calling intltool-update.

* Wed Jul 01 2009 Milan Crha <mcrha@redhat.com> - 2.27.3-3.fc12
- Rebuild against newer gcc

* Tue Jun 23 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.3-2.fc12
- Add patch to allow Anjal to build.

* Mon Jun 15 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.3-1.fc12
- Update to 2.27.3

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-2.fc12
- Don't make -perl own directories that are already owned by the base package

* Fri May 29 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.2-1.fc12
- Update to 2.27.2
- Patch broken libevolution-mail-shared library.
- Remove strict_build_settings since the settings are used upstream now.

* Mon May 04 2009 Matthew Barnes <mbarnes@redhat.com> - 2.27.1-1.fc12
- Update to 2.27.1
- Bump evo_major to 2.28.
- Temporarily disable EDS_DISABLE_DEPRECATED due to GNOME bug #569652.

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-2.fc11
- Don't drop schemas translations from po files

* Wed Apr 15 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.1.1-1.fc11
- Update to 2.26.1.1
- Remove patch for GNOME bug #578685 (fixed upstream).

* Tue Apr 14 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.1-2.fc11
- Add patch for GNOME bug #578685 (attachment bar crasher).

* Mon Apr 13 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.1-1.fc11
- Update to 2.26.1

* Fri Apr 10 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-3.fc11
- Fix directory ownership

* Thu Apr 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.0-2.fc11
- Require libpst.

* Mon Mar 16 2009 Matthew Barnes <mbarnes@redhat.com> - 2.26.0-1.fc11
- Update to 2.26.0

* Mon Mar 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.92-1.fc11
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-2.fc11
- Actually make the help subpackage noarch

* Mon Feb 16 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.91-1.fc11
- Update to 2.25.91

* Sat Feb 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-3.fc11
- Make the help subpackage noarch

* Fri Feb 06 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.90-2.fc11
- Update BuildRoot, License, Source and URL tags.
- Require gnome-common so we don't have to patch it out.

* Mon Feb 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.90-1.fc11
- Update to 2.25.90

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.5-1.fc11
- Update to 2.25.5
- Ditch eds_version and use our own version.  This will keep evolution
  and evolution-data-server versions in lockstep from now on.

* Mon Jan 05 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.4-1.fc11
- Update to 2.25.4
- Bump eds_version to 2.25.4.
- Bump libgweather_version to 2.25.4.

* Mon Dec 15 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.3.1-1.fc11
- Update to 2.25.3.1
- New BR: libgweather-devel
- Remove patch for GNOME bug #552583 (fixed upstream).
- Bump the gtkhtml and gtk2 minimum versions.

* Tue Dec 09 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.2-2.fc11
- Add patch for GNOME bug #552583 (fix account URI comparisons).

* Mon Dec 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.2-1.fc11
- Update to 2.25.2
- Bump eds_version to 2.25.2.

* Thu Nov 20 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.1-2.fc11
- Fix a typo (RH bug #472358).

* Mon Nov 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.25.1-1.fc11
- Update to 2.25.1
- Bump evo_major to 2.26.
- Bump eds_version to 2.25.1.

* Tue Oct 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.1-2.fc10
- Bump eds_version to 2.24.1 (unfortunately).

* Tue Oct 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.1-1.fc10
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-3
- Save space in the -help package by not shipping multiple copies
  of each screenshot

* Thu Sep 25 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.0-2.fc10
- Strip unneeded translations from .mo files (RH bug #463887).
- Split Perl-based utilities into a "perl" subpackage (RH bug #462345).

* Mon Sep 22 2008 Matthew Barnes <mbarnes@redhat.com> - 2.24.0-1.fc10
- Update to 2.24.0

* Mon Sep 08 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.92-1.fc10
- Update to 2.23.92

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.91-1.fc10
- Update to 2.23.91
- Bump eds_version to 2.23.91

* Mon Aug 25 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.90-2.fc10
- Bump gtkhtml_version to 3.23.5 (RH bug #460076).

* Wed Aug 20 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.90-1.fc10
- Update to 2.23.90
- Bump eds_version to 2.23.90.1

* Mon Aug 04 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.6-1.fc10
- Update to 2.23.6

* Tue Jul 22 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.5-1.fc10
- Update to 2.23.5
- Bump eds_version to 2.23.5.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-3.fc10
- fix license tag
- fix patches to apply with fuzz=0

* Thu Jun 19 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.4-2.fc10
- Don't ship the unfinished "Custom Header" plugin.

* Mon Jun 16 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.4-1.fc10
- Update to 2.23.4
- Remove patches for RH bug #449925 (fixed upstream).

* Fri Jun 06 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.3.1-4.fc10
- Use a less pretentious summary.

* Fri Jun 06 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.3.1-3.fc10
- Remove the gnome-spell requirement.

* Wed Jun 04 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.3.1-2.fc10
- Add patches for RH bug #449925 (buffer overflow vulnerabilities).

* Mon Jun 02 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.3.1-1.fc10
- Update to 2.23.3.1
- Bump eds_version to 2.23.3.

* Mon May 12 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.2-1.fc10
- Update to 2.23.2
- Remove enchant-devel requirement.
- Remove patch for RH bug #437208 (fixed upstream).

* Mon Apr 28 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-2.fc10
- Explicitly require enchant-devel, even though I shouldn't need to.

* Mon Apr 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.23.1-1.fc10
- Update to 2.23.1
- Bump evo_major to 2.22.
- Bump eds_version to 2.23.1.
- Bump glib2_version to 2.16.0.
- Bump gtkhtml_version to 3.19.1.
- Add gvfs requirement.
- Drop gnomevfs2 requirement.
- Remove patch for RH bug #164957 (obsolete).

* Mon Apr 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.1-1.fc9
- Update to 2.22.1
- Remove patch for GNOME bug #524310 (fixed upstream).

* Tue Mar 25 2008 Dan Williams <dcbw@redhat.com> - 2.22.0-4.fc9
- Add patch for GNOME bug #524310

* Fri Mar 14 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.0-3.fc9
- Explicit require evolution-data-server since its shared object names
  still can't be trusted (RH bug #426511).

* Fri Mar 14 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.0-2.fc9
- Add patch for RH bug #437208 (tracking network status).

* Mon Mar 10 2008 Matthew Barnes <mbarnes@redhat.com> - 2.22.0-1.fc9
- Update to 2.22.0
- Remove patch for CVE-2008-0072 (fixed upstream).

* Tue Mar 04 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.92-2.fc9
- Add patch for CVE-2008-0072 (format string vulnerability).

* Mon Feb 25 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.92-1.fc9
- Update to 2.21.92
- Bump eds_version to 2.21.92.

* Wed Feb 13 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.91-2.fc9
- Rebuild against libsoup 2.3.2.

* Mon Feb 11 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.91-1.fc9
- Update to 2.21.91
- Bump eds_version to 2.21.91.
- Remove patch for GNOME bug #240073 (fixed upstream).

* Sat Feb 02 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.90-4.fc9
- Remove some obsolete configure options:
  --enable-file-chooser, --enable-file-locking, --enable-dot-locking
- Remove gnome-doc-utils work-around for GNOME bug #427939 (fixed upstream).
- Remove patch for RH bug #215478 (fixed upstream).

* Tue Jan 29 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.90-3.fc9
- Add patch to address the recent deprecation of G_GNUC_FUNCTION.

* Tue Jan 29 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.90-2.fc9
- Add patch for GNOME bug #240073 (don't strikeout Click to Add in tasks).

* Mon Jan 28 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.90-1.fc9
- Update to 2.21.90
- Update build requirements.
- Remove patch for GNOME #363695 (obsolete/problematic).
- Remove patch for GNOME #509741 (fixed upstream).

* Tue Jan 15 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.5-2.fc9
- Add patch for GNOME bug #509741 (crash on startup).

* Mon Jan 14 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.5-1.fc9
- Update to 2.21.5
- The backup-restore plugin is stable again.
- Remove patch for RH bug #154360 (fixed upstream).
- Remove patch for RH bug #166231 (obsolete, possibly fixed upstream).
- Remove patch for RH bug #178295 (fixed upstream).
- Remove patch for GNOME bug #362638 (fixed upstream).
- Remove patch for GNOME bug #504030 (fixed upstream).
- Remove patch for GNOME bug #507311 (fixed upstream).

* Sat Jan 05 2008 Matthew Barnes <mbarnes@redhat.com> - 2.21.4-2.fc9
- Add patch for GNOME bug #507311 (send Bug Buddy reports to the new
  BugBuddyBugs Bugzilla component).

* Mon Dec 17 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.4-1.fc9
- Update to 2.21.4
- Expunge unused patches.
- Bump eds_version to 2.21.4 for new Camel functions.

* Mon Dec 10 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.3-4.fc9
- Split junk filtering plugins into evolution-bogofilter and
  evolution-spamassassin subpackages, each of which requires the
  necessary backend packages.  (RH bug #377381)

* Wed Dec 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.3-3.fc9
- Bump eds_version to 2.21.3 and gtkhtml_version to 3.17.3.

* Tue Dec  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-2
- Rebuild against new openssl

* Mon Dec 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.3-1.fc9
- Update to 2.21.3
- Remove patch for RH bug #215467 (fixed upstream).
- Remove patch for GNOME bug #499920 (fixed upstream).

* Sat Dec 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.2-4.fc9
- Fix a corrupted patch that caused GNOME bug #499291.

* Thu Nov 29 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.2-3.fc9
- Add patch for GNOME bug #499920 (invalid #include).

* Fri Nov 23 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.2-2.fc9
- Rebuild against newer libpisync.so.

* Mon Nov 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.2-1.fc9
- Update to 2.21.2

* Tue Oct 30 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-2.fc9
- Attempt to split the gnome-pilot stuff into a separate
  evolution-conduits subpackage (RH bug #178155).

* Mon Oct 29 2007 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-1.fc9
- Update to 2.21.1
- Remove redundant requirements.
- Bump EDS requirement to 2.21.1.
- Bump gtkhtml requirement to 3.17.1.
- Backup/restore plugin got moved from standard to experimental.
- Revert the per-component menu items (RH bug #222105, #241462, #293771).
- Show the switcher buttons by default (RH bug #186403).
- Alter the desktop file Name and Comment.
- Disable patch for GNOME bug #376991 for now.  It may be contributing
  to password prompting problems as described in RH bug #296671.
- Remove patch for GNOME bug #417999 (fixed upstream).
- Remove patch for GNOME bug #476040 (fixed upstream).
- Remove patch for GNOME bug #477045 (fixed upstream).

* Mon Oct 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-2.fc8
- Fix a broken zoom icon.

* Mon Oct 15 2007 Milan Crha <mcrha@redhat.com> - 2.12.1-1.fc8
- Update to 2.12.1
- Add files for the new backup-restore plugin.

* Tue Oct 09 2007 Matthew Barnes <mbarnes@redhat.com. - 2.12.0-8.fc8
- Sync version requirements up with configure.in.

* Tue Oct 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-7.fc8
- Revise patch for GNOME bug #477045 (more icon tweaks).

* Fri Oct 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-6.fc8
- Require libbonobo >= 2.16.0 (RH bug #213823).

* Thu Oct 04 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-5.fc8
- Require gnome-themes (RH bug #235617).

* Wed Oct 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-4.fc8
- Revise patch for GNOME bug #477045 (run-time warnings when composing mail).

* Wed Sep 19 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-3.fc8
- Re-enable the inline audio plugin since it now uses GStreamer 0.10.

* Wed Sep 19 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-2.fc8
- Revise patch for GNOME bug #477045 (less-zealous icon renaming).

* Mon Sep 17 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.0-1.fc8
- Update to 2.12.0
- Remove patch for RH bug #182247 (fixed upstream).

* Sat Sep 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.92-4.fc8
- Add patch for GNOME bug #477045 (use standard icon names).

* Tue Sep 11 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.92-3.fc8
- Add patch for GNOME bug #476040 (fix attachment icon).

* Sat Sep  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.11.92-2.fc8
- Split off an evolution-help package

* Mon Sep 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.92-1.fc8
- Update to 2.11.92

* Wed Aug 29 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.91-3.fc8
- Revise patch for GNOME bug #362638 to fix GNOME bug #357175
  (Evolution fails to close after IMAP alert has been displayed).

* Tue Aug 28 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.91-2.fc8
- Fix compilation breakage caused by our strict build settings.

* Tue Aug 28 2007 Milan Crha <mcrha@redhat.com> - 2.11.91-1.fc8
- Update to 2.11.91
- Removed patch for RH bug #157400 / GNOME bug #303877 (fixed upstream).
- Removed patch for RH bug #157505 / GNOME bug #303878 (fixed upstream).
- Removed patch for RH bug #161885 / GNOME bug #309166 (fixed upstream).
- Removed patch for RH bug #202751 / GNOME bug #355766 (fixed upstream).
- Removed patch for RH bug #218898 / GNOME bug #385414 (fixed upstream).
- Removed patch for RH bug #253348 / GNOME bug #467883 (fixed upstream).

* Thu Aug 23 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.90-4.fc8
- Obsolete the evolution-bogofilter package.

* Mon Aug 20 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.90-3.fc8
- Revise patch for GNOME bug #417999 to fix GNOME bug #447591
  (Automatic Contacts combo boxes don't work).

* Sat Aug 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.90-2.fc8
- Add patch for RH bug #253348 (crash on startup).

* Wed Aug 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.90-1.fc8
- Update to 2.11.90

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.11.6.1-2
- Update the license field
- Use %%find_lang for help files

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.6.1-1.fc8
- Update to 2.11.6.1

* Tue Jul 31 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.6-1.fc8
- Update to 2.11.6
- Remove patch for GNOME bug #380534 (fixed upstream).

* Fri Jul 27 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.5-3.fc8
- Add patch for GNOME bug #380534 (clarify version requirements).

* Mon Jul 16 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.5-2.fc8
- Remove spamassassin requirement since it's optional.

* Fri Jul 13 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.5-1.fc8
- Update to 2.11.5
- Revise patch for GNOME bug #362638 to fix RH bug #245695.

* Wed Jun 27 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.4-2.fc8
- Revise patch for GNOME bug #363638 to fix RH bug #245289 (frequent hangs).

* Mon Jun 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.4-1.fc8
- Update to 2.11.4
- Remove patch for GNOME bug #447727 (fixed upstream).

* Thu Jun 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3-5.fc8
- Add patch for GNOME bug #447727 (remove EClippedLabel).

* Wed Jun 06 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3-4.fc8
- Revise patch for GNOME bug #362638 to fix RH bug #240507 (hang on exit).

* Wed Jun 06 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3-3.fc8
- Remove some debug messages that accidentally slipped in.

* Tue Jun 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3-2.fc8
- Fix an invalid g_free() that was causing lock-ups.

* Mon Jun 04 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.3-1.fc8
- Update to 2.11.3
- Evolution no longer has versioned file names.
- Remove patch for RH bug #202289 (fixed upstream).
- Remove patch for RH bug #235878 (fixed upstream).
- Remove patch for RH bug #238155 (fixed upstream).
- Remove patch for RH bug #240147 (fixed upstream).

* Thu May 31 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.2-2.fc8
- Evolution no longer requires libgnomeprint[ui].

* Fri May 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.11.2-1.fc8
- Update to 2.11.2
- Bump evo_major to 2.12.
- Bump eds_version to 1.11.0.
- Update files with new plugins and icons.
- Remove patch for RH bug #190359 (fixed upstream).
- Remove patch for RH bug #218801 (fixed upstream).
- Remove patch for RH bug #234315 (fixed upstream).
- Remove patch for RH bug #236399 (fixed upstream).
- Remove patch for RH bug #236860 (fixed upstream).
- Remove patch for RH bug #238551 (fixed upstream).
- Remove patch for GNOME bug #373837 (fixed upstream).
- Remove patch for GNOME bug #373116 (fixed upstream).
- Remove patch for GNOME bug #418971 (fixed upstream).
- Remove patch for GNOME bug #419469 (fixed upstream).
- Remove patch for GNOME bug #419524 (fixed upstream).
- Remove evolution-2.6.0-prototypes.patch (obsolete).

* Wed May 16 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-17.fc7
- Revise patch for GNOME bug #362638 to fix RH bug #237206
  (certificate prompt causes crash, again).

* Tue May 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-16.fc7
- Add patch for RH bug #240147 (Send/Receive dialog layout).

* Mon May 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-15.fc7
- Revise patch for RH bug #236860 to match upstream's solution.

* Mon May 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-14.fc7
- Revise patch for RH bug #238155 (crash on startup).

* Mon May 07 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-13.fc7
- Add patch for RH bug #238155 (crash on startup).

* Tue May 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-12.fc7
- Add patch for RH bug #238551 (incorrect attachment count).

* Tue May 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-10.fc7
- Revise patch for GNOME bug #363695 to fix RH bug #238497
  (crash sorting "To" column).

* Mon Apr 30 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-9.fc7
- Revise some patches so that we don't have to run autoreconf.
- Remove patch for GNOME bug #427939 (use a different work-around).

* Fri Apr 27 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-8.fc7
- Add patch for RH bug #236399 (en_CA attribution format).

* Mon Apr 23 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-7.fc7
- Remove the welcome email from evolution@novell.com (bug #179427).

* Sun Apr 22 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-6.fc7
- Add patch for RH bug #236860 (launching from clock applet).

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.1-5
- Don't install INSTALL

* Sat Apr 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-4.fc7
- Add patch for RH bug #234315 (fix saving attachments).

* Fri Apr 13 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-3.fc7
- Add patch for RH bug #235878 (make Help->Contents work again).

* Tue Apr 10 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-2.fc7
- Revise patch for GNOME bug #362638 to fix RH bug #235096
  (crash when displaying a mail server message to user).

* Mon Apr 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.1-1.fc7
- Update to 2.10.1
- Fix buggy gnome-doc-utils.make (GNOME bug #427939).
- Remove patch for CVE-2007-1002 (fixed upstream).
- Remove patch for RH bug #231767 (fixed upstream).
- Remove patch for RH bug #235056 (fixed upstream).
- Remove patch for GNOME bug #352713 (fixed upstream).

* Wed Apr 04 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-10.fc7
- Add patch for GNOME bug #352713 (improve folder tree updates).

* Tue Apr 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-9.fc7
- Require libxml2-devel in evolution-devel package (RH bug #235056).
- Add libxml-2.0 requirement to evolution-plugin-2.10.pc.

* Tue Apr 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-8.fc7
- Revise patch for GNOME bug #419524 to fix RH bug #235082
  (crash in initial account setup wizard).

* Mon Apr 02 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-7.fc7
- Add patch for RH bug #231767 (allow mail-notification to build).

* Fri Mar 30 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-6.fc7
- Revise patch for GNOME bug #362638 (deprecate EThread).

* Thu Mar 29 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-5.fc7
- CVE-2007-1002 (Shared memo categories format string vulnerability)
- Add -Wdeclaration-after-statement to strict build settings.

* Mon Mar 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-4.fc7
- Run gtk-update-icon-cache in %post and %postun (RH bug #234018).

* Sat Mar 17 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-3.fc7
- Add flag to disable deprecated Camel symbols.
- Add patch for GNOME bug #419469 (refactor shell/main.c).
- Add patch for GNOME bug #419524 (use GLib's i18n macros).
- Add patch for GNOME bug #418971 (drop support for GLib < 2.8).

* Wed Mar 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-2.fc7
- Add patch for GNOME bug #417999 (use ESourceComboBox).

* Mon Mar 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.10.0-1.fc7
- Update to 2.10.0.
- Add patch for GNOME bug #376991 (refactor password handling).

* Mon Feb 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.92-1.fc7
- Update to 2.9.92.
- Require gtkhtml3 >= 3.13.92.
- Add missing libgnomeprintui22 requirements.
- Remove patch for GNOME bug #350253 (fixed upstream).
- Remove patch for GNOME bug #356177 (fixed upstream).
- Remove patch for GNOME bug #360946 (fixed upstream).
- Remove evolution-2.5.4-move-autosave-file.patch (fixed upstream).
- Add minimum version to intltool requirement (currently >= 0.35.5).

* Thu Feb 15 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.91-3.fc7
- Revise patch for GNOME bug #362638 to fix RH bug #220714
  (certificate prompt causes crash).

* Tue Feb 13 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.91-2.fc7
- Require GConf2 in post.
- Require scrollkeeper in post and postun.

* Mon Feb 12 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.91-1.fc7
- Update to 2.9.91
- Require gtkhtml3 >= 3.13.6.
- Add files for new imap-features plugin.
- Add flag to disable deprecated Pango symbols.
- Remove patch for GNOME bug #357216 (fixed upstream).
- Remove patch for GNOME bug #359979 (fixed upstream).

* Fri Jan 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-4.fc7
- Compile with the -fno-strict-aliasing flag, which will hopefully improve
  reliability until the illegal type-punning is fixed (RH bug #224552).

* Sun Jan 21 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-3.fc7
- Revise evolution-2.7.1-no-gnome-common.patch so that we no longer
  have to run autoconf before building.
- Revise evolution-2.5.4-fix-conduit-dir.patch so that we no longer
  have to run automake before building.

* Wed Jan 10 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-2.fc7
- Add patch for GNOME bug #359979 (change EMsgPort semantics).

* Mon Jan 08 2007 Matthew Barnes <mbarnes@redhat.com> - 2.9.5-1.fc7
- Update to 2.9.5
- Remove pilot-link-0.12 patch (fixed upstream).
- Remove patch for RH bug #215466 and #218589 (fixed upstream).
- Remove patch for RH bug #215695 (fixed upstream).

* Sat Dec 30 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.4-4.fc7
- Add Requires evolution-data-server-devel to devel subpackage
  (RH bug #218889).

* Thu Dec 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.4-3.fc7
- Add patch for RH bug #218898 (viewing message source).

* Wed Dec 20 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.4-2.fc7
- Revise patch for RH bug #202751 (printing of indic languages).

* Tue Dec 19 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.4-1.fc7
- Update to 2.9.4
- Bump eds_version to 1.9.4 due to soname changes.
- Remove patch for GNOME bug #382431 (fixed upstream).

* Fri Dec 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-5.fc7
- Add patch for GNOME bug #373116 (use GtkColorButton).

* Fri Dec 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-4.fc7
- Disable patch for RH bug #216537, which caused RH bug #219228.

* Tue Dec 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-3.fc7
- Revise patch for RH bug #215466 to also fix RH bug #218589.

* Mon Dec 11 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-2.fc7
- Add patch for RH bug #215467 (missing meeting participants).

* Sat Dec 09 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.3-1.fc7
- Update to 2.9.3
- Configure with scrollkeeper disabled.
- Disable automake portability checking.
- Ship our own icons from gnome-icon-theme.
- BuildRequires: gnome-doc-utils >= 0.8.0
- Add patch for RH bug #215478 (Maildir and MH accounts).
- Add patch for RH bug #215695 (crashes w/o mail accounts).
- Add patch for RH bug #216537 (viewing attachments).
- Add patch for RH bug #218801 (count unread messages first).
- Add patch for GNOME bug #350253 (ship our own icons).
- Add patch for GNOME bug #382431 (implicit function declaration).
- Revise patch for GNOME bug #360946 (improved "about" dialog).
- Remove patch for GNOME bug #357970 (fixed upstream).

* Tue Nov 28 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.2-3.fc7
- Add patch to port evolution conduits to pilot-link 0.12.
- Add patch for RH bug #215466 (optional meeting participants).
- Add patch for GNOME bug #373837 (use GtkFontButton).
- Remove patch for GNOME bug #343331 (fixed upstream).

* Tue Nov 07 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.2-2.fc7
- Revise patch for RH bug #202751 and re-enable it.

* Mon Nov 06 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.2-1.fc7
- Update to 2.9.2
- Remove patch for Gnome.org bug #360240 (fixed upstream).
- Remove patch for Gnome.org bug #360619 (fixed upstream).

* Mon Nov 06 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.1-3.fc7
- Add patch for RH bug #176400 (reset calendar IM context).
- Add patch for RH bug #182247 (calendar input glitch).

* Fri Oct 20 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.1-2.fc7
- Add patch for Gnome.org bug #356177 (deprecate EMutex).
- Add patch for Gnome.org bug #363695 (deprecate EStrv/EPoolv).
- Disable patch for RH bug #202751 (unwanted side-effects).

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.9.1-1.fc7
- Update to 2.9.1
- Bump eds_version to 1.9.1, evo_major to 2.10.
- Remove patch for Gnome.org bug #359236 (fixed upstream).

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-4.fc7
- Another typo.

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-3.fc7
- Fix a typo in setting up .desktop symlinks.

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-2.fc7
- Forgot to check-in one of the patches.

* Mon Oct 16 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.1-1.fc7
- Update to 2.8.1
- Use stricter build settings.
- Make .desktop symlinks absolute (RH bug #209322).
- Add patch for RH bug #202751 (printing of indic languages).
- Add patch for Gnome.org bug #357970 (deprecated GLib / GDK symbols).
- Add patch for Gnome.org bug #359236 (search state crash).
- Add patch for Gnome.org bug #360240 ("unused variable" warnings).
- Add patch for Gnome.org bug #360619 ("incompatible pointer type" warnings).
- Add patch for Gnome.org bug #360946 (improved "about" dialog).
- Add patch for Gnome.org bug #362638 (deprecate EThread).
- Update patch for RH bug #211058 (partially fixed upstream).
- Remove patch for RH bug #201307 (fixed upstream).
- Remove patch for RH bug #205576 (fixed upstream).
- Remove patch for Gnome.org bug #351332 (fixed upstream).
- Remove patch for Gnome.org bug #352450 (fixed upstream).
- Remove patch for Gnome.org bug #353472 (fixed upstream).
- Remove patch for Gnome.org bug #356811 (fixed upstream).

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.8.0-7.fc6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-6.fc6
- Add patch for RH bug #205576 (message deletion in thread view).

* Wed Sep 20 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-5.fc6
- Add patch for Gnome.org bug #356811 (lingering file on uninstall).

* Tue Sep 19 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-4.fc6
- Bump eds_version to 1.8.0.

* Wed Sep 13 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-3.fc6
- Add patch for RH bug #161885.

* Wed Sep 13 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-2.fc6
- Add patch for RH bug #201307.

* Mon Sep  4 2006 Matthew Barnes <mbarnes@redhat.com> - 2.8.0-1.fc6
- Update to 2.8.0
- Remove patch for RH bug #197868 (fixed upstream).
- Remove patch for RH bug #201541 (fixed upstream).
- Remove patch for RH bug #201831 (fixed upstream).
- Remove patch for RH bug #202383 (fixed upstream).
- Remove patch for RH bug #203036 (fixed upstream).
- Remove patch for Gnome.org bug #352248 (fixed upstream).
- Remove patch for Gnome.org bug #352423 (fixed upstream).
- Update patch for Gnome.org bug #351332 (partially fixed upstream).

* Thu Aug 31 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-8.fc6
- Add patch for RH bug #203036.
- Disable notification-cleanups patch.

* Tue Aug 29 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-7.fc6
- Add patch for Gnome.org bug #353472.

* Mon Aug 28 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-6.fc6
- Add another hunk to the patch for RH bug #201541.
- Add patch for RH bug #202289.

* Mon Aug 28 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-5.fc6
- Add patch for RH bug #201541.

* Wed Aug 23 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-4.fc6
- Add patches for Gnome.org bug #352450.

* Tue Aug 22 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-3.fc6
- Replace my patch for RH bug #202383 with a better one from upstream.
- Add patch for Gnome.org bug #352423.

* Mon Aug 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-2.fc6
- Add patch for Gnome.org bug #352248 (and remember to commit it).

* Mon Aug 21 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.92-1.fc6
- Update to 2.7.92
- Remove patch for RH bug #197834 (fixed upstream).
- Update patch for Gnome.org bug #351332 (partially fixed upstream).

* Tue Aug 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-5.fc6
- Drop the bug-buddy dependency since it's not required for Evolution to run.

* Mon Aug 14 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-4
- Add patch for RH bug #201831.

* Mon Aug 14 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-3
- Consolidate "missing declarations" patches.
- Add patch for RH bug #202383.

* Fri Aug 11 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-2
- Add patch for RH bug #197868.

* Mon Aug  7 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.91-1
- Update to 2.7.91
- Update patch for RH bug #197834 for use with bug-buddy 2.15.90.
- Require bug-buddy >= 2.15.90.

* Fri Aug  4 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.90-6
- Update to 2.7.90
- Require evolution-data-server-1.7.90.1.

* Wed Aug  2 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-5
- Remove patch for RH bug #167157, as it fixed it the wrong way.
- The real fix for #167157 is in evolution-data-server-1.7.4-5.
- No longer packaging unused patches.

* Mon Jul 31 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-4
- Add patch for RH bug #178295.
- Add patch for RH bug #167157.

* Tue Jul 18 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-3
- Clean up spec file, renumber patches.
- Add BuildRequires for dbus-glib-devel.
- Rebuild to pick up new D-Bus.

* Thu Jul 13 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-2
- Update patch for RH bug #157400.
- Update patch for RH bug #157505.

* Wed Jul 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.4-1
- Update to 2.7.4
- Remove evo-calendar-print-with-pango-7.patch (fixed upstream).
- Remove patch for Gnome.org bug #345677 (fixed upstream).
- Remove patch for RH bug #175596 (fixed upstream).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.7.3-10.1
- rebuild

* Tue Jul 11 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-10
- Update patch for RH bug #190359.

* Fri Jul  7 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-9
- Make "Submit Bug Report" menu item work again (RH #197384).

* Thu Jul  6 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-8
- Add patch for RH bug #166231 (also addresses #131227 and #157391).

* Thu Jun 29 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-7
- Add patch for RH bug #157400, reorder some patch #'s.

* Thu Jun 29 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-6
- Properly capitalize "Message->Mailing List" menu items (RH #175596).

* Tue Jun 27 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-5
- Add patch for Gnome.org bug #211058 for Trever Adams to test.

* Mon Jun 26 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-4
- Add patch for RH bug #157505 for QE testing.

* Thu Jun 22 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.3-3
- Fix bad type in schema file (Gnome.org #345677).

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 2.7.3-2
- rebuilt with new gnutls

* Tue Jun 13 2006 Matthias Clasen  <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Mon May 29 2006 Dan Williams <dcbw@redhat.com> - 2.7.2.1-4
- Don't crash on quit when trying to save window size (Gnome.org #343331)

* Tue May 23 2006 Matthew Barnes <mbarnes@redhat.com> 2.7.2.1-3
- Port evolution-2.7.1-notification-cleanups.patch to new libnotify API.
- Require libnotify >= 0.4.

* Fri May 19 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.2.1-2
- Require specific versions of GNU Autotools packages for building.
- Add evolution-2.7.2-preedit-gnome.bz-264485.patch (Mayank Jain).
- Various spec file cleanups.
- Pick up new libnotify.

* Wed May 17 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.2.1-1
- Update to 2.7.2.1
- Remove nss/nspr hunk from evolution-2.7.1-no-gnome-common.patch
  (fixed upstream).

* Fri May 12 2006 Matthew Barnes <mbarnes@redhat.com> - 2.7.1-1
- Update to 2.7.1
- Bump evo_major from 2.6 to 2.8
- Upstream evolution.desktop renamed evolution-%{evo_major}.desktop.
- Upstream evolution.keys renamed evolution-%{evo_major}.keys.
- Upstream evolution.mime renamed evolution-%{evo_major}.mime.
- Update line numbers in evolution-2.5.2-no-gnome-common.patch and
  evolution-2.5.5.1-notification-cleanups.patch and rename them to
  version 2.7.1.

* Wed May  3 2006 Matthew Barnes <mbarnes@redhat.com> - 2.6.1-3
- rebuilt

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.6.1-2
- Update to 2.6.1

* Thu Mar 30 2006 Caolan McNamara <caolanm@redhat.com> - 2.6.0-2
- rebuild against reverted pilot-link
- disable evolution-2.5.4-fix-conduits.patch for reversion to pilot-link 0.11.8

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.com> - 2.6.0-1
- 2.6.0
- turn on the "error on missing prototypes" check thing

* Mon Feb 27 2006 Ray Strode <rstrode@redhat.com> - 2.5.92-1
- 2.5.92

* Tue Feb 14 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.91-1
- 2.5.91
- updated patch 101 to track upstream changes to calendar printing code
- remove uptreamed patch 807 (NM multiple initialization assertion)
- readded the mail-to-task plugin XML UI file
- bump e-d-s req to 1.5.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.90-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Christopher Aillon <caillon@redhat.com> - 2.5.90-2
- Disable the inline audio plugin for now since it uses gstreamer08

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.90-1
- 2.5.90
- trimmed patches 805 and 808, as parts of these got merged upstream
- trimmed and regenerated patch 806 to track upstream
- removed the mail-to-task plugin XML UI file

* Sat Jan 28 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.5.1-2
- added missing patch

* Wed Jan 25 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.5.1-1
- 2.5.5.1
- update patch 106 to track upstream, renaming from 
  evolution-2.2.2-commit-enter-on-calendar.patch to 
  evolution-2.5.5.1-commit-enter-on-calendar.patch
- update patch 805 to track upstream
- added patch to fix some newly missing declarations (patch 808)
- replace evolution-2.5.4-port-to-new-libnotify-api.patch with 
  evolution-2.5.5.1-notification-cleanups.patch, since much of this was 
  duplicated by another patch that landed upstream; removing the actions code 
  as it was crashing deep inside DBus (patch 806, #177666)
- explicitly list various files to reduce reliance on globbing; organized the
  files into logical groups; comment them
- added -Wno-sign-compare to CFLAGS
- enabled parallel make
- introduced require_function_declarations macro to make 
  -Werror-implicit-function-declaration flag optional; turn it off for now
- include the new CalDAV and mail-attachments-import plugins in the file list;
  add an XML UI file for the mail-to-task plugin. 
- use "sed -i -e" rather than "sed -ie" to avoid getting severe bonobo files

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 2.5.4-10
- fix fix for multilib issue with shlib bonobo components (bug 156982)

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 2.5.4-9
- fix multilib issue with shlib bonobo components (bug 156982)

* Thu Jan 12 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-8
- avoid multiple initialization of NetworkManager connections (patch 807, 
  gnome bug #326785)

* Thu Jan 12 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-7
- updated alarm notification patch(patch 806, #177546, #177666, #177667, 
  #177670)

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 2.5.4-6
- Remove unneeded Requires: notify-daemon

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 2.5.4-5
- Update BR to libnotify-devel

* Wed Jan 11 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-4
- ported alarm notification code to the new libnotify API (patch 806, #177546)
- added libnotify_support macro
- added explicit notify-daemon requirement as a workaround for bug #177535

* Tue Jan 10 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-3
- updated patch 800 to include patch for memo conduit (untested at this stage);
  renaming from evolution-2.5.2-fix-conduits.patch to 
  evolution-2.5.4-fix-conduits.patch; extended patch 802 to handle the memo 
  conduit; renaming from evolution-2.2.2-fix-conduit-dir.patch to 
  evolution-2.5.4-fix-conduit-dir.patch; re-enable conduits in build (#175160)
- switch the build-time dep for the audio-inline plugin from gstreamer-devel to
  gstreamer08-devel to better reflect the test in the tarball's configure.in

* Wed Jan  4 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-2
- added optional build-time requirement on NetworkManager-glib-devel
- update patch 805 to cover a missing declaration in Network Manager support

* Tue Jan  3 2006 David Malcolm <dmalcolm@redhat.com> - 2.5.4-1
- 2.5.4
- update patch 107 to track underlying code changes; rename from
  evolution-2.2.2-move-autosave-file.patch to
  evolution-2.5.4-move-autosave-file.patch
- added patch to fix more missing declarations (patch 805)
- added files for publish-calendar plugin

* Mon Dec 19 2005 David Malcolm <dmalcolm@redhat.com> - 2.5.3-1
- 2.5.3
- Updated patch 106 (evolution-2.2.2-commit-enter-on-calendar.patch) so that it
  still applies cleanly

* Thu Dec 15 2005 Christopher Aillon <caillon@redhat.com> 2.5.2-2
- Require nspr and nss instead of mozilla-nspr and mozilla-nss
- Update no-gnome-common patch to work with standalone nss package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 David Malcolm <dmalcolm@redhat.com> - 2.5.2-1
- 2.5.2
- bump gtkhtml requirement from 3.7.6 to 3.9.2
- bump eds requirement from 1.4.1.1 to 1.5.2
- bump evo_major from 2.4 to 2.6
- updated patch 107
- updated patch 108
- updated patch 800, replacing 
  rh-161817-attach-116019-conduit_pilot_link_updates.diff with 
  evolution-2.5.2-fix-conduits.patch.  Not yet complete.
- disable pilot support for now (see #175160)
- added hula plugin to list of packaged plugins
- generalize gconf schema packaging to support changing evo_major

* Fri Dec  2 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.2-2
- force regeneration of the intltool files to prevent a problem where the 
  tarball copy of intltool-merge.in was out of sync with the intltool.m4 in the
  latest shipped copy of intltool, which resulted in a broken intltool-merge 
  script when the tree was reautotooled.  (appears that the tarball was built 
  with a CVS copy of intltool where @EXPANDED_LIBDIR@ had been renamed to
  @INTLTOOL_LIBDIR@, but our aclocal/intltool.m4 doesn't yet reflect that 
  change)

* Tue Nov 29 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.2-1
- 2.4.2
- explicitly list the plugins that are packaged (#166234)
- added build-time requirement on gstreamer-devel to cope with audio-inline
  plugin

* Tue Nov 29 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-8
- add -DLDAP_DEPRECATED to CFLAGS (#172999)

* Wed Oct 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-7
- Added a patch (110) to hide the component switcher buttons by default on new
  windows (#170799) by patching the GConf schema.
- Made list of installed schemas explicit.
- Own the plugins subdirectory

* Tue Oct 25 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-6
- use 4 separate .desktop files from the redhat-menus package, rather than the
  current single one; bump the redhat-menus requirement accordingly (from 1.13
  to 5.0.4); introduce a macro for this requirement.

* Mon Oct 24 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-5
- fix removal of upstream .desktop file (broke on upgrade to Evolution 2.2, and
  continued to be broken with 2.3/2.4) (#103826, again)

* Tue Oct 18 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-4
- updated patch 804 to declare e_calendar_table_process_completed_tasks

* Tue Oct 18 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-3
- added patch (804: evolution-2.4.1-fix-missing-declarations.patch) to fix
  missing declaration (thanks to Peter Robinson)

* Mon Oct 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-2
- bump e-d-s requirement to 1.4.1.1

* Tue Oct  4 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.1-1
- 2.4.1
- regenerate patch 101 to handle conflict in 
  calendar/gui.print.c: print_week_day_event introduced by fix to upstream bug
  244981 (end date added while printing in the week view); bump patch name from
  version 5 to version 6
- removed patch 804 (conduits-multi-day-crash); this is now in upstream tarball

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-2
- rebuild for mozilla on ppc64

* Wed Sep  7 2005 David Malcolm <dmalcolm@redhat.com> - 2.4.0-1
- 2.4.0
- Removed patch to fix implicit function declarations (patch 110, added in 
  2.3.8-1) as this is now upstream.

* Thu Sep  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.8-4
- Enable exchange support when configuring, so that the exchange-operations
  plugin gets built.

* Fri Aug 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.8-3
- Added patch for #157074 (patch 804)

* Fri Aug 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.8-2
- Move -Werror-implicit-function-declaration from configuration to the make
  stage, to avoid breaking configuration tests.

* Tue Aug 23 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.8-1
- 2.3.8
- add -Werror-implicit-function-declaration to CFLAGS and a patch to fix the 
  problems arising (patch 110)

* Tue Aug 16 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.7-3
- Introduce macro for gnome-pilot dependency, bumping from 2.0.6 to 2.0.13
- Add obsoletion of libgal2/libgal2-devel (dependency was removed in 2.3.6-1);
  based on the last EVR of the libgal2 package in CVS, 2:2.5.3-2

* Mon Aug 15 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.7-2
- rebuild

* Tue Aug  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.7-1
- 2.3.7
- Bump evolution-data-server requirement from 1.3.6 to 1.3.7
- Bump gtkhtml3 requirement from 3.6.2 to 3.7.6

* Mon Aug  8 2005 Tomas Mraz <tmraz@redhat.com> - 2.3.6.1-5
- rebuild with new gnutls

* Tue Aug  2 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6.1-4
- Added patch to show correct mimetype for OpenOffice.org files when guessing 
  type for attachments with mimetype "application/octet-stream" (#164957)

* Mon Aug  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6.1-3
- Improved version of evolution-2.3.5.1-fix-150458.patch (#150458)

* Sat Jul 30 2005 David Malcolm <dmalcolm@redhat.com> 2.3.6.1-2
- Fixed version numbers in GConf schema files (#164622); added 
  apps-evolution-mail-prompts-checkdefault-2.4.schemas

* Fri Jul 29 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6.1-1
- 2.3.6.1

* Thu Jul 28 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.6-1
- 2.3.6
- Bump evolution-data-server requirement to 1.3.6 (needed for 
  CAL_STATIC_CAPABILITY_HAS_UNACCEPTED_MEETING)
- Removed libgal2[-devel] dependencies; the code has been moved into the 
  evolution tarball

* Thu Jul 28 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.5.1-2
- added experimental patch to port ETable printing to use Pango (#150458)

* Mon Jul 25 2005 David Malcolm <dmalcolm@redhat.com> - 2.3.5.1-1
- 2.3.5.1
- Update evo_major from 2.2 to 2.4
- Updated evo-calendar-print-with-pango- patch from version 4 to 5
- Removed Patch105: evolution-2.2.2-fix-new-mail-notify.patch as configure.in
  in this branch tests for existance for dbus-glib-1, rather than max-version.
- Removed Patch801: gb-309138-attach-48417-fix-evo-conduit-memleaks.patch as
  this is now in upstream tarball.
- Removed evolution-calendar-importers and evolution-addressbook-importers
  directories.
- Updated evolution-2.2.2-no-gnome-common.patch to include a patch to rename
  mozilla-nspr to nspr

* Tue Jun 28 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-11.fc5
- Remove GNOME_COMPILE_WARNINGS from configure.in (since gnome-common might not be available when we rerun the autotools; patch 803)

* Tue Jun 28 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-10.fc5
- Moved .conduit files to libdir/gnome-pilot/conduits, rather than beneath datadir, to match gnome-pilot (patch 802)

* Mon Jun 27 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-9.fc5
- Replaced patch to port conduits to pilot-link-0.12 with Mark G Adams's version of same (#161817)
- Added Mark G Adams's memory leak fix (patch 801)

* Mon Jun  6 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-8
- Added Ivan Gyurdiev's patch to move autosave files inside the .evolution
  directory

* Thu May 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-7
- Added Akira Tagoh's patch for calendar keypress handling (#154360)

* Mon May 23 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-6
- Remove static versions of libraries

* Thu May  5 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-5
- added evolution-2.2.2-fix-new-mail-notify.patch to CVS

* Thu May  5 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-4
- Removed explicit mozilla_build_version; instead use pkg-config to determine 
the path to the NSS/NSPR headers.
- Use a macro to express requirement on pilot-link (was 1:0.11.4, now 0.12; 
patches depend on this)
- Re-enabled the new-mail-notify plugin (my patch to handle differing DBus 
versions is in the upstream tarball; but configure.in disables the plugin for 
dbus versions > 0.23; patched configure.in to allow arbitrary DBus versions, 
and run autoconf at the start of the build) (#156328)

* Sat Apr 30 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-3
- updated mozilla_build_version to 1.7.7

* Sat Apr 30 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-2
- Finished porting conduits to pilot-link-0.12 API; re-enabled pilot support (#152172)

* Mon Apr 11 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.2-1
- 2.2.2
- updated evo-calendar-print-with-pango-4.patch to handle upstream change to print_comp_item
- removed patch for XB73912; now in upstream tarball
- removed patch to new-mail-notify; generalised fix to cope with various DBus API versions is now upstream
- removed patch for XB73844; now in upstream tarball
- Update requirements:
  - gtkhtml3 from 3.6.1 to 3.6.2
  - libgal2 from 2.4.1 to 2.4.2
  - eds from 1.2.1 to 1.2.2

* Wed Mar 23 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.1.1-2
- Add patch for upstream bug XB73844 (should now be able to accept meeting requests)

* Fri Mar 18 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.1.1-1
- 2.1.1.1

* Thu Mar 17 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.1-1
- 2.2.1
- Updated requirements:
  * gtkhtml3 from 3.6.0 to 3.6.1
  * libgal2 from 2.4.0 to 2.4.1
  * eds from 1.2.0 to 1.2.1
- Added rum-time requirement on gnome-vfs2; updated version requirement from 2.0 to 2.4
- The new-mail-notify plugin will not be built for now since the upstream configure test now checks for dbus-glib-1 version <= 0.23.4 (to minimise problems caused by the API change)

* Mon Mar 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-10
- disabled pilot-link support for now so that we have an evolution package; more patching is needed to get this to work with pilot-link-0.12

* Mon Mar 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-9
- another attempt at porting to pilot-link 0.12

* Mon Mar 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-8
- Added patch to deal with changes to pilot-link from 0.11->0.12

* Mon Mar 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-7
- use 0.31 rather than 0.31.0 for DBus version

* Mon Mar 14 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-6
- rebuilt against pilot-link-0.12
- added versioning to the requirement on dbus (>=0.31)

* Thu Mar 10 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-5
- Added patch for changes to DBus API in version 0.31 (#150671)
- Removed explicit run-time spec-file requirement on mozilla.
  The Mozilla NSS API/ABI stabilised by version 1.7.3
  The libraries are always located in the libdir
  However, the headers are in /usr/include/mozilla-%{mozilla_build_version}
  and so they move each time the mozilla version changes.
  So we no longer have an explicit mozilla run-time requirement in the specfile; 
  a requirement on the appropriate NSS and NSPR .so files is automagically generated on build.
  We have an explicit, exact build-time version, so that we can find the headers (without
  invoking an RPM query from the spec file; to do so is considered bad practice)
- Introduced mozilla_build_version, to replace mozilla_version

* Wed Mar  9 2005 Christopher Aillon <caillon@redhat.com> - 2.2.0-4
- Depend on mozilla 1.7.6

* Wed Mar  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- added patch from upstream for bug XB-73192, fixing missing "Mark as Read/Unread" context menu items

* Tue Mar  8 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-2
- actually add source tarball this time

* Tue Mar  8 2005 David Malcolm <dmalcolm@redhat.com> - 2.2.0-1
- 2.2.0
- Removed patch for GCC 4 fix as this is now in upstream tarball
- Updated requirements:
  * gtkhtml3 from 3.5.7 to 3.6.0
  * libgal2 from 2.3.5 to 2.4.0
  * eds from 1.1.6 to 1.2.0

* Tue Mar  8 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-3
- rebuild (to use latest DBus library)

* Tue Mar  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-2
- added patch to fix build with GCC4

* Tue Mar  1 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.6-1
- Update from upstream unstable 2.1.6 to 2.1.6
- Added patches to fix calendar and addressbook printing for non-Roman scripts (#138075)
- Added explicit requirement on libgnomeprint22 >= 2.8.0
- Added BuildRequires: gtk-doc
- Updated requirements:
  * gtkhtml3 from 3.5.6 to 3.5.7
  * libgal2 from 2.3.4 to 2.3.5
  * eds from 1.1.5 to 1.1.6

* Wed Feb  9 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.5-1
- Update from upstream unstable 2.1.4 to 2.1.5
- Updated requirements:
  * gtkhtml3 from 3.5.4 to 3.5.6
  * libgal2 from 2.3.3 to 2.3.4
  * eds from 1.1.4.1 to 1.1.5
- Removed explicit packaging of weather icons as these are now below DATADIR/evolution/2.2 rather than DATADIR/evolution-2.2

* Wed Jan 26 2005 David Malcolm <dmalcolm@redhat.com> - 2.1.4-1
- Update from upstream stable 2.0.3 to unstable 2.1.4
- Updated evo_major from 2.0 to 2.2
- Removed camel packaging as this has been moved to evolution-data-server for Evolution 2.2
- Added plugins to the packaged files
- Added weather icons to the packaged files
- Updated requirements:
  * gtkhtml3 from 3.3.2 to 3.5.4
  * libgal2 from 2.2.4 to 2.3.3
  * eds from 1.0.3 to 1.1.4.1
  * libsoup from 2.2.0 to 2.2.2
- Added built-time requirement on atk-devel
- Enable all plugins for now
- Added requirement on dbus (for the new-mail-notify plugin)
- Enable gtk-doc
- Updated GConf schema name suffixes from 2.0 to 2.2

* Sun Dec 19 2004 Christopher Aillon <caillon@redhat.com> 2.0.3-2
- Rebuild against mozilla 1.7.5

* Wed Dec 15 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.3-1
- Update from upstream 2.0.2 to 2.0.3 with these bug fixes:
 * Addressbook
   XB67656 - almost the same email address are considrered identical (Siva)
   XB69079 - Data repeated after save with bad date format (Siva)
   XB66854 - Some strings are missed to translation (Rodney)

 * Calendar 	
   XB47529 - Date in reminder window appears in UTF-8 in non-UTF-8 locale (Rodney)
   XB68707 - Events ending at 12:00 AM show as ending at 12:00 pm (JP)
   XB67403 - wrong alarm time displayed (Rodrigo)
   XB68077 - appointment dialog re-size (Rodrigo)
   - leak fixes (Chen)
   - sensitize menu items in list view properly (JP)
   - redraw display when 24hr time setting changes (JP)

 * Mail
   XB69533 - Unable to subscribe to the alt hierarchy (Michael)
   XB69776 - Signed Mail with attachments displays everything with multipart/boundaries stuff (Michael)
   XB69615 - delete certificate after viewing smime message (Michael)
   XB69109 - EHLO or HELO with ip addresses does not conform rfc 821  (Michael)
   XB69982 - During Newsgroup list refresh, it crashes (Michael) 
   XB69446 - Mail shown as attachment if some headers are upper case (S. Caglar Onur) 
   XB68556 - NNTP with SSL won't work, even with stunnel (Michael) 
   XB69145 - toplevel message/rfc822 parts are broken for IMAP (Michael)
   XB69241 - base64 attachement holding PGP block (Jeff)
   XB67895 - nntp support not asking for password (Michael)
   XB67898 - Use of symbolic port-names is not guaranteed to work everywhere (Michael)
   XB69851 - remember password check doesn't stick (Michael)
   XB69623 - Moving a message from an IMAP INBOX to an IMAP folder caused crash (Radek)
   XB69339 - postscript and some other attachments not visable (Michael)
   XB69579 - vFoldersXBUNMATCHED generates errors (Michael)
   XB68958 - current message forgotten in vfolders (Michael)
   XB68974 - Wizard doesn't store smtp auth settings (Michael)
   XB67496 - html email not rendered in preview pane (Michael)
   XB67014 - Checking supported auth types doesn't work with new SSL certificate (Michael)
   XB68006 - Evo crashed after viewing previously-sent email and copying URL from it (Michael)
   XB68787 - Crash when migrating 1.4 data to 2.0.2 (Michael)
   XB67622 - SMTP auth usernames containing % character fail (Jeff)
   - fix pthread_key_delete args (Julio M. Merino Vidal)
- Removed patch for "Unmatched" vfolder properties dialog (#141458) as this is now in upstream tarball (XB69579 above)
- Update dependency on e-d-s from 1.0.2 to 1.0.3
- Update dependency on libgal2 from 2.2.3 to 2.2.4

* Wed Dec  1 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-6
- Fix broken properties dialog for "Unmatched" vfolder (#141458)

* Wed Oct 27 2004 Christopher Aillon <caillon@redhat.com> - 2.0.2-4
- Re-enable s390(x)

* Fri Oct 22 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-3
- added requirement on gnutls/gnutls-devel

* Fri Oct 22 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-2
- Fix for #132050 (no entry for Evolution in the menus): use the new redhat-evolution.desktop file provided by redhat-menus-1.13

* Tue Oct 12 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.2-1
- Update from 2.0.1 to 2.0.2
- Updated dependency on e-d-s from 1.0.1 to 1.0.2
- Updated dependency on libgal2 from 2.2.2 to 2.2.3
- Updated dependency on gtkhtml3 from 3.3.0 to 3.3.2
- ppc's mozilla dependency is now in line with the other architectures at 1.7.3

* Sat Oct  9 2004 David Malcolm <dmalcolm@redhat.com>
- disable s390/s390x for now

* Fri Oct  8 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-3
- Fix for #135135, updating the fix for #103826 that removes the evolution.desktop file in "Office"; the file to delete had been renamed to evolution-2.0.desktop
- Added requirement on redhat-menus, since this supplies the target of our .desktop symlink

* Tue Sep 28 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-2
- update mozilla dependency from 1.7.2 to 1.7.3, apart from on ppc (and on s390 and s390x, which remain at 1.6, and on ppc64 where it isn't available at all)

* Tue Sep 28 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.1-1
- Update from 2.0.0 to 2.0.1
- Updated dependency on e-d-s from 1.0.0 to 1.0.1
- Updated dependency on libgal2 from 2.2.0 to 2.2.2

* Mon Sep 20 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.0-2
- rebuilt

* Tue Sep 14 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.0-1
- Update from 1.5.94.1 to 2.0.0
- Change source FTP location from 1.5 to 2.0
- Updated dependency on e-d-s from 0.0.99 to 1.0.0
- Documentation has now moved from 1.5 to 2.0

* Tue Aug 31 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.94.1-1
- updated tarball from 1.5.93 to 1.5.94.1
- the BASE_VERSION in the configure.in script has finally been updated from 1.5 to 2.0 (affects OAFIIDs, install dirs, binary names etc); updated evo_major and various other parts of the spec-file to reflect this; however documentation is still 1.5 in upstream tarball
- updated dependency on libgal2 from 2:2.1.14 to 2:2.2.0
- updated dependency on libsoup from 2.1.13 to 2.2.0
- updated dependency on e-d-s from 0.0.98 to 0.0.99

* Tue Aug 17 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.93-2
- updated gnome-icon-theme requirement from 1.2.0 to 1.3.6 to fix problem with missing stock icons (bz #130142)

* Mon Aug 16 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.93-1
- updated tarball from 1.5.92.2 to 1.5.93
- removed filechooser patch - this is now in the upstream tarball, with a test at configuration time; it was autodetected and enabled in my test build; I've explicitly enabled it to be certain.
- updated dependency on libgal2 from 2:2.1.13 to 2:2.1.14
- updated dependency on libsoup from 2.1.12 to 2.1.13
- updated dependency on e-d-s from 0.0.97 to 0.0.98

* Wed Aug 11 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.92.2-2
- Increased mozilla_version from 1.7 to 1.7.2 so that the NSS test looks in the correct place

* Wed Aug 11 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.92.2-1
- updated tarball from 1.5.92.1 to 1.5.92.2

* Wed Aug  4 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.92.1-1
- updated tarball from 1.5.91 to 1.5.92.1
- added a dependency on gnome-icon-theme
- updated dependency on libgal2 from 2:2.1.11 to 2:2.1.13
- updated dependency on gtkhtml3 from 3.1.17 to 3.3.0
- updated dependency on libsoup from 2.1.11 to 2.1.12
- updated dependency on e-d-s from 0.0.95 to 0.0.97

* Mon Jul 26 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.91-1
- 1.5.91

* Thu Jul  8 2004 Jeremy Katz <katzj@redhat.com> - 1.5.90-5
- use mozilla 1.7 on platforms where it's available
- check to make sure the appropriate mozilla headers exist if using
  mozilla nss for ssl or fail the build

* Thu Jul  8 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Wed Jul  7 2004 David Malcolm <dmalcolm@redhat.com>
- rebuilt

* Tue Jul  6 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.90-2
- Fixed sources file

* Tue Jul  6 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.90-1
- 1.5.90; updated requirements on gtkhtml3, libgal2, and e-d-s

* Thu Jun 17 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9.2-1
- 1.5.9.2

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9.1-3
- Replaced /usr/lib with %%{_libdir} in mozills_nss ssl_flags

* Mon Jun  7 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9.1-2
- updated filechooser patch again

* Mon Jun  7 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.9.1-1
- 1.5.9.1; updated filechooser patch

* Wed May 26 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.8-3
- added ORBit2 and spamassassin requirements

* Mon May 24 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.8-2
- Fixed up filechooser patch and re-enabled it

* Fri May 21 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.8-1
- 1.5.8; added explicit libbonoboui requirement; disabled filechooser patch for now

* Tue May  4 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.7-3
- Added GtkFileChooser patch based on work by Carlos Garnacho Parro (http://lists.ximian.com/archives/public/evolution-patches/2004-March/004867.html); added requirement for GTK 2.4

* Thu Apr 22 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.7-2
- added emfv signal fix patch and fix for defaults in switch statements on gcc3.4

* Wed Apr 21 2004 David Malcolm <dmalcolm@redhat.com> - 1.5.7-1
- 1.5.7

* Wed Mar 10 2004 Jeremy Katz <katzj@redhat.com> - 1.5.5-1
- 1.5.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Jeremy Katz <katzj@redhat.com> - 1.5.4-1
- 1.5.4

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> 
- buildrequire e-d-s-devel instead of e-d-s (#114712)
- enable nntp support (#114802)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jeremy Katz <katzj@redhat.com> 1.5.3-1
- 1.5.3

* Wed Jan 21 2004 Jeremy Katz <katzj@redhat.com> 1.5.2-2
- size_t/int mismatch compile fix for 64bit platforms

* Wed Jan 14 2004 Jeremy Katz <katzj@redhat.com> 1.5.2-0
- 1.5.2
- add patch to fix gconf warning with schema

* Sun Jan  4 2004 Jeremy Katz <katzj@redhat.com> 1.5.1-0
- 1.5.1
- temporarily disable redhatify patch
- use mozilla-nss for SSL
- fix schema names

* Thu Nov  6 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-8
- fall back to HELO for ESMTP (#108753)

* Tue Oct 28 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-7
- fix title on composer save dialog (#108159)

* Mon Oct 27 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-6
- Make imap command length shorter to avoid choking some imap servers 
  (notably cyrus-imap).
- Make wombat session managed so that we don't hit weird bonobo activation
  things.  This adds a dependency on $DISPLAY for wombat.  (#106826)

* Sun Oct 19 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-5
- use AI_ADDRCONFIG to avoid returning IPv6 addresses on hosts without 
  IPv6 support
- add patch from upstream with reply-to-list shortcut (Ctrl-l)

* Wed Oct 15 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-4
- really, really remove duplicate menu entry (#103826)

* Tue Oct 14 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-3
- Pull in some patches from upstream CVS
  * Avoid division by zero with POP (X#41610)
  * Don't mangle headers (X#33545)
  * Prefix IPV6 numeric hosts properly (X#46006, #105028)
  * Use proper function for IPV6 reverse lookups (X#46006)
  * Allow timezone offset to be up to 14 hours (X#49357)

* Mon Oct 13 2003 Jeremy Katz <katzj@redhat.com> 
- add patch from upstream CVS to fix SMTP syntax problems (#106630) 
- really remove duplicate menu entry (#103826)

* Mon Oct  6 2003 Jeremy Katz <katzj@redhat.com> 
- make redhat-email.desktop symlink relative (#104391)

* Wed Sep 24 2003 Jeremy Katz <katzj@redhat.com> 
- add ipv6 support per dwmw2's request

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 1.4.5-2
- 1.4.5

* Wed Sep 17 2003 Jeremy Katz <katzj@redhat.com> 
- move static libs into -devel (#104399)

* Tue Sep 16 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-7
- filter types are gtypes, not ints (#103934)

* Wed Sep 10 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-6
- fix from upstream (will be in 1.4.5) to fix menu merging in the 
  composer with new libbonobo

* Fri Sep  5 2003 Jeremy Katz <katzj@redhat.com> 
- remove the desktop file in Office (#103826)

* Tue Sep  2 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-5
- patch from upstream to fix display of some mails in 
  different charsets (#102899)
- add requires on newer version of ORBit2 (#103386)
- add patch from upstream (extracted by George Karabin) to use gnome-vfs 
  mime icon lookup where available (#102553)

* Fri Aug 22 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-4
- include static libs (#102834)

* Wed Aug  6 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-3
- add a -devel subpackage (#99376)

* Mon Aug  4 2003 Jeremy Katz <katzj@redhat.com> 1.4.4-1
- 1.4.4

* Wed Jul 30 2003 Jeremy Katz <katzj@redhat.com> 
- buildrequires fixup from Ville Skytta (#101325)

* Thu Jul 24 2003 Jeremy Katz <katzj@redhat.com> 1.4.3-6
- include tagoh's patch for printing cjk contacts (committed upstream, #99374)

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-5
- rebuild

* Tue Jul 15 2003 Jeremy Katz <katzj@redhat.com> 1.4.3-4
- build on all arches again

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 1.4.3-3
- rebuild

* Thu Jul 10 2003 Jeremy Katz <katzj@redhat.com> 1.4.3-1
- 1.4.3

* Thu Jun 19 2003 Jeremy Katz <katzj@redhat.com> 
- make gal version dep more explicit

* Fri Jun 13 2003 Jeremy Katz <katzj@redhat.com> 
- fix desktop file (#97162)

* Tue Jun 10 2003 Jeremy Katz <katzj@redhat.com> 1.4.0-2
- rebuild
- excludearch ppc64 for now

* Mon Jun  9 2003 Jeremy Katz <katzj@redhat.com> 1.4.0-1
- 1.4.0

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  5 2003 Jeremy Katz <katzj@redhat.com> 1.3.92-2
- rebuild

* Wed Jun  4 2003 Jeremy Katz <katzj@redhat.com> 
- buildrequires gettext (#92276)

* Sun May 25 2003 Jeremy Katz <katzj@redhat.com> 1.3.92-1
- 1.3.92

* Wed May  7 2003 Jeremy Katz <katzj@redhat.com> 1.3.3-2
- fix default for /schemas/apps/evolution/mail/display/mime_types

* Tue May  6 2003 Jeremy Katz <katzj@redhat.com> 1.3.3-1
- 1.3.3

* Sun May  4 2003 Jeremy Katz <katzj@redhat.com> 1.3.2-2
- enable pilot support
- add redhatify patch back

* Tue Apr 22 2003 Jeremy Katz <katzj@redhat.com>
- add a /usr/bin/evolution symlink

* Mon Apr 21 2003 Jeremy Katz <katzj@redhat.com> 
- fix gnome-spell version requirement

* Wed Apr 16 2003 Jeremy Katz <katzj@redhat.com> 1.3.2-1
- add trivial fix for evolution-mail schema key (ximian #41419)

* Tue Apr 15 2003 Jeremy Katz <katzj@redhat.com> 
- update to 1.3
- don't build with pilot support for now
- don't redhat-ify the summary prefs for now

* Sun Apr  6 2003 Jeremy Katz <katzj@redhat.com> 1.2.4-2
- fix krb5 libdir for lib64 systems

* Sun Apr  6 2003 Jeremy Katz <katzj@redhat.com> 1.2.4-1
- update to 1.2.4

* Thu Apr  3 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-7
- oops, fix a tyop

* Thu Apr  3 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-6
- add a few cleanups for 64bit cleanliness (#86347)

* Sun Mar 30 2003 Jeremy Katz <katzj@redhat.com> 
- add some buildrequires (#87612)

* Mon Mar 24 2003 Jeremy Katz <katzj@redhat.com> 1.2.3-1
- update to 1.2.3

* Wed Mar 19 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-5
- security patches from upstream
  - sanity check UUEncoding header before decoding (CAN-2003-0128)
  - don't decode doubly UUEncoded content (CAN-2003-0129)
  - don't use a bonobo component to display things without registered 
    handlers (CAN-2003-0130)

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 1.2.2-4
- debuginfo rebuild

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-3
- memleak patch had some bits that weren't supposed to be there.  update 
  to newer from upstream.
- fix directory checking in proxy patch

* Thu Feb 20 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-2
- add missing build dep (#84388)
- add patch from upstream for evolution-mail memleak
- add patch from upstream to use the gnome2 proxy settings by default

* Fri Feb  7 2003 Jeremy Katz <katzj@redhat.com> 1.2.2-1
- 1.2.2
- build on x86_64 

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-4
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- if building with OpenSSL, attempt to get cflags and ldflags from pkgconfig

* Thu Jan  2 2003 Jeremy Katz <katzj@redhat.com> 1.2.1-3
- we don't want to use native POSIX threads for mutexes in db3, override them

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 1.2.1-2
- rebuild

* Fri Dec 13 2002 Jeremy Katz <katzj@redhat.com> 1.2.1-1
- update to 1.2.1

* Thu Dec 12 2002 Jeremy Katz <katzj@redhat.com> 1.2.0-6
- require a newer soup, the old one Has Bugs (tm)
- excludearch x86_64; getting a R_X86_64_32S relocation in libical 
  although everything appears to be built with -fPIC correctly

* Tue Dec 10 2002 Jeremy Katz <katzj@redhat.com> 1.2.0-5
- patch for multilib krb5

* Mon Dec  2 2002 Jeremy Katz <katzj@redhat.com> 1.2.0-4
- add upstream patch to handle LDAPv3 better
- add upstream patch to fix shell memory leaks
- add upstream patch to fix ldap scope selection
- build with openssl instead of mozilla-nss since it's available on 
  more platforms
- build on all arches

* Fri Nov 22 2002 Jeremy Katz <katzj@redhat.com>
- require bonobo-conf, not -devel (#78398)

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de> 1.2.0-3
- disable pilot support for mainframe

* Mon Nov 18 2002 Jeremy Katz <katzj@redhat.com> 1.2.0-2
- macro-ify the mozilla version to make it easier to build against 
  newer mozillas with headers in new locations
- buildrequire pilot-link-devel (#78077)
- drop uneeded ldapv3 patch (toshok says 1.2 already handles this)
- drop unneeded patch for ordering of the libdb checks
- add fejj's patch to always subscribe to the inbox from evolution-patches

* Tue Nov 12 2002 Jeremy Katz <katzj@redhat.com> 1.2.0-1
- 1.2.0

* Sat Nov  2 2002 Jeremy Katz <katzj@redhat.com> 1.1.90-2
- reenable pilot support
- redhatify

* Fri Nov  1 2002 Jeremy Katz <katzj@redhat.com> 1.1.90-1
- update to 1.1.90

* Thu Oct 31 2002 Jeremy Katz <katzj@redhat.com>
- include mozilla epochs in requires (#74577)
- add build requires on newer oaf (#76801)

* Thu Oct 24 2002 Jeremy Katz <katzj@redhat.com> 1.1.2-1
- update to 1.1.2
- remove unpackaged files from the buildrooot
- disable pilot support for now

* Tue Sep  3 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-10
- add freetype-devel to build requires (#73319)

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Fix a problem where evolution-mail right click items corrupted the stack
  (#67992)

* Thu Aug 29 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-9
- don't install two desktop files (#72871)

* Wed Aug 28 2002 Preston Brown <pbrown@redhat.com> 1.0.8-8
- absolute symlink .desktop file (#72913)

* Thu Aug 22 2002 han Ngo <than@redhat.com> 1.0.8-7
- rebuild against new pilot-link

* Sat Aug 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- bzip2 source

* Tue Aug  6 2002 Than Ngo <than@redhat.com> 1.0.8-5
- rebuild against new pilot-link-0.11.2

* Thu Jul 18 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-4
- rebuild against new gnome-pilot

* Tue Jul  9 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-3
- remove static and libtool archives for importers and camel-providers (#68222)
- do desktop-file-install magic 
- remove dead sites from summary list (#64522)
- support openldap protocol version 3 based off of Nalin's autofs changes 

* Mon Jul  8 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-2
- fix openldap-devel buildrequire

* Mon Jul  1 2002 Jeremy Katz <katzj@redhat.com> 1.0.8-1
- 1.0.8 

* Thu Jun 27 2002 Jeremy Katz <katzj@redhat.com> 1.0.7-2
- include patch to omf files from otaylor@redhat.com to fix 
  scrollkeeper validation errors

* Sun Jun 23 2002 Jeremy Katz <katzj@redhat.com> 1.0.7-1
- update to 1.0.7
- excludearch alpha while mozilla isn't being built there

* Sun May 26 2002 Tim Powers <timp@redhat.com> 1.0.5-2
- automated rebuild

* Mon May 13 2002 Jeremy Katz <katzj@redhat.com> 1.0.5-1
- update to 1.0.5

* Fri May  3 2002 Jeremy Katz <katzj@redhat.com> 1.0.3-6
- add patch to fix spool unread counts (#64198)
- build with the fix for the crasher mail sent to 
  evolution-list (ximian #24140)

* Mon Apr 15 2002 Jeremy Katz <katzj@redhat.com> 1.0.3-4
- include fejj(at)ximian.com's patch to fix the EINPROGRESS error with ssl 
  since it's been committed to the branch and fixes the problem for me
- include patch from tagoh(at)redhat.com to change the default charset 
  for Japanese to ISO-2022-JP (#63214)

* Wed Apr 10 2002 Jeremy Katz <katzj@redhat.com> 1.0.3-3
- minor tweaks to the redhatify patch
- make accepting appointments sent to mailing lists work
- use the RFC specified LDAP attribs for freebusy and calendarURI 
  in addressbook
- fix a crash in the startup wizard

* Sun Mar 31 2002 Jeremy Katz <katzj@redhat.com> 1.0.3-2
- move desktop file to /etc/X11/applnk (#62399)

* Sun Mar 24 2002 Jeremy Katz <katzj@redhat.com> 1.0.3-1
- update to evolution 1.0.3
- change summary view to show a recent errata list by default

* Thu Mar 14 2002 Jeremy Katz <katzj@redhat.com>
- put correct path to nspr includes on configure command line

* Mon Mar 11 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-3
- mozilla 0.9.9 has nspr and nss subpackages, hooray!  rip out the static 
  libnss linkage and just link against what is provided dynamically
- kill the -devel subpackage since it's of questionable use
- explicitly require mozilla-nss and mozilla-nspr packages to make it easier
  to resolve the requirements

* Thu Feb 21 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-2
- rebuild in new environment
- temporarily exclude on ia64 again

* Thu Jan 31 2002 Jeremy Katz <katzj@redhat.com> 1.0.2-1
- update to 1.0.2

* Mon Jan 28 2002 Jeremy Katz <katzj@redhat.com> 1.0.1-4
- build on ia64 now that mozilla exists for ia64

* Sun Jan 27 2002 Jeremy Katz <katzj@redhat.com> 1.0.1-3
- rebuild in new environment
- add pilot support

* Sun Jan 13 2002 Jeremy Katz <katzj@redhat.com> 1.0.1-2
- rebuild without mozilla-psm in the buildroot so libnss is linked 
  statically as intended

* Sat Jan 12 2002 Jeremy Katz <katzj@redhat.com> 1.0.1-1
- update to 1.0.1
- patch for autoconf 2.52 accepted upstream
- include man page
- use --with-sub-version=" (%%{version}-%%{release})"

* Tue Dec 18 2001 Jeremy Katz <katzj@redhat.com> 1.0-2
- really disable news
- add patch from Jens Petersen <juhp@redhat.com> to hopefully get 
  builds working with autoconf 2.52
- conditionalize static libnss stuff so that it can go away when we
  have a mozilla with shared libnss

* Thu Dec  6 2001 Jeremy Katz <katzj@redhat.com> 1.0-1.7.2
- add patches off of branch for:
  * do not show up as Preview Release in version string
  * have next/previous work with multiple selected messages
- build without pilot support

* Mon Dec  3 2001 Jeremy Katz <katzj@redhat.com> 1.0-1
- and bump to 1.0

* Sun Dec  2 2001 Jeremy Katz <katzj@redhat.com>
- let's build with an included copy of libnss now since OpenSSL is support
  is disabled on the 1.0 branch
- build with --enable-dot-locking=no
- excludearch ia64 again now that we need libnspr

* Mon Nov 26 2001 Jeremy Katz <katzj@redhat.com>
- build with gnome-pilot and krb5 support
- conditionalize ldap, pilot and krb5 support
- clean up buildrequires some

* Sat Nov 17 2001 Jeremy Katz <katzj@redhat.com>
- we can build on ia64 since we're using openssl instead of nspr
- disable non-functional nntp support 
- 0.99.2 (rc2) 

* Fri Nov  9 2001 Jeremy Katz <katzj@redhat.com>
- add explicit requires on current bonobo, oaf, and GConf to help people
  help themselves
- s/Copyright/License/

* Thu Nov  8 2001 Jeremy Katz <katzj@redhat.com>
- add a patch to revert changes to camel-tcp-stream-openssl; appears to 
  fix the SSL hangs

* Wed Nov  7 2001 Jeremy Katz <katzj@redhat.com>
- fix filelist to include libical zoneinfo
- add devel subpackage with includes and static libs

* Mon Nov  5 2001 Jeremy Katz <katzj@redhat.com>
- updated to 0.99.0 aka 1.0 RC1

* Tue Oct 23 2001 Havoc Pennington <hp@redhat.com>
- 0.16 snagged from Ximian GNOME

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- initial build based on David Sainty's specfile

* Thu Oct 04 2001 David Sainty <dsainty@redhat.com>
- Updated to 0.15.99, 20011004 from cvs.

* Wed Sep 05 2001 David Sainty <dsainty@redhat.com>
- Updated to 0.13.99, 20010905 from cvs.

* Mon Sep 03 2001 David Sainty <dsainty@redhat.com>
- Updated to 0.13.99, 20010903 from cvs.
- Fixed Requires + BuildRequires

* Mon Aug 06 2001 David Sainty <dsainty@redhat.com>
- Updated to 0.12.99, 20010806 from cvs.

* Mon Aug 06 2001 David Sainty <dsainty@redhat.com>
- Relocated libical* from /usr/lib due to kdepim, -2

* Mon Aug 06 2001 David Sainty <dsainty@redhat.com>
- First spec file for evolution.

