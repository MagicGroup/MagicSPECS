# TODO: merge patches upstream where applicable

Name:           gnokii
Version:        0.6.30
Release:        2%{?dist}
Summary:        Linux/Unix tool suite for various mobile phones

Group:          Applications/Communications
License:        GPLv2+
URL:            http://www.gnokii.org/
Source0:        http://www.gnokii.org/download/gnokii/%{name}-%{version}.tar.bz2
Source2:        %{name}-smsd.init
Source3:        %{name}-smsd.sysconfig
Source4:        %{name}-smsd.logrotate
Source5:        %{name}-smsd2mail.sh
Source6:        %{name}-smsd-README.smsd2mail
# Patch to make gnokii use "htmlview" instead of "mozilla" as default browser
Patch0:         %{name}-htmlview.patch
# Patch to remove port locking and apply the system-wide /usr/sbin directory
# to the path instead of the default /usr/local
Patch1:         %{name}-config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	gtk2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick
BuildRequires:	postgresql-devel
BuildRequires:	mysql-devel
BuildRequires:	sqlite-devel
BuildRequires:	zlib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	libusb-devel
BuildRequires:	libical-devel >= 0.24
BuildRequires:	libXt-devel
BuildRequires:	libXpm-devel 
BuildRequires:	pcsc-lite-devel
BuildRequires:	readline-devel
BuildRequires:	perl(XML::Parser) intltool
Requires(pre):  %{_sbindir}/groupadd

%description
Gnokii provides tools and a user space driver for use with mobile
phones under Linux, various unices and Win32. With gnokii you can do
such things as make data calls, update your address book, change
calendar entries, send and receive SMS messages and load ring tones
depending on the phone you have.

%package     -n xgnokii
Summary:        Graphical Linux/Unix tool suite for various mobile phones
Group:          Applications/Communications
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n xgnokii
Xgnokii is graphical Linux/Unix tool suite for various mobile
phones. It allows you to edit your contacts book, send/read SMS's
from/in computer and more other features.

%package        smsd
Summary:        Gnokii SMS daemon
Group:          System Environment/Daemons
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(pre):  %{_sbindir}/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig

%description    smsd
The Gnokii SMS daemon receives and sends SMS messages.

%package        smsd-pgsql
Summary:        PostgreSQL support for Gnokii SMS daemon
Group:          System Environment/Daemons
Requires:       %{name}-smsd%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-smsd-postgresql < 0.6.4-0.lvn.2

%description    smsd-pgsql
%{summary}.

%package        smsd-mysql
Summary:        MySQL support for Gnokii SMS daemon
Group:          System Environment/Daemons
Requires:       %{name}-smsd%{?_isa} = %{version}-%{release}

%description    smsd-mysql
%{summary}.

%package        smsd-sqlite
Summary:        SQLite support for Gnokii SMS daemon
Group:          System Environment/Daemons
Requires:       %{name}-smsd%{?_isa} = %{version}-%{release}

%description    smsd-sqlite
%{summary}.

%package        devel
Summary:        Gnokii development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
%{summary}.


%prep
%setup -q
#%patch0 -p0
%patch1 -p0
install -pm 644 %{SOURCE5} smsd2mail.sh
install -pm 644 %{SOURCE6} README.smsd2mail

%build
%configure --enable-security --disable-static
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' -i libtool
sed -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' -i libtool
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Rename smsd to gnokii-smsd
mv $RPM_BUILD_ROOT%{_bindir}/{,gnokii-}smsd
mv $RPM_BUILD_ROOT%{_mandir}/man8/{,gnokii-}smsd.8
sed -i 's,smsd ,gnokii-smsd ,' $RPM_BUILD_ROOT%{_mandir}/man8/gnokii-smsd.8
sed -i 's,smsd.,gnokii-smsd.,' $RPM_BUILD_ROOT%{_mandir}/man8/gnokii-smsd.8

# Remove libtool droppings
rm $RPM_BUILD_ROOT%{_libdir}{,/smsd}/lib*.la

# Fix up the default desktop file
desktop-file-install \
  --delete-original \
  --vendor "" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --mode 644 \
  --add-category X-Fedora \
  $RPM_BUILD_ROOT%{_datadir}/applications/xgnokii.desktop

# Convert the default icons to PNG
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/pixmaps
convert Docs/sample/logo/gnokii.xpm \
  $RPM_BUILD_ROOT%{_datadir}/pixmaps/xgnokii.png
chmod 644 $RPM_BUILD_ROOT%{_datadir}/pixmaps/xgnokii.png

# Install the configuration files
install -Dpm 755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/gnokii-smsd
install -Dpm 640 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gnokii-smsd
install -Dpm 644 %{SOURCE4} \
  $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/gnokii-smsd
cp -a Docs/sample/gnokiirc $RPM_BUILD_ROOT%{_sysconfdir}/

# Install the docs
mv $RPM_BUILD_ROOT%{_datadir}/doc/gnokii/ temporary-gnokii-docs/

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%pre
%{_sbindir}/groupadd -r gnokii >/dev/null 2>&1 || :

%pre smsd
%{_sbindir}/useradd -r -M -d / -g gnokii \
  -s /sbin/nologin -c "Gnokii system user" gnokii >/dev/null 2>&1 || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post smsd
/sbin/chkconfig --add gnokii-smsd

%preun smsd
if [ $1 -eq 0 ] ; then
  %{_initrddir}/gnokii-smsd stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del gnokii-smsd
fi

%postun smsd
if [ $1 -ge 1 ] ; then
  %{_initrddir}/gnokii-smsd try-restart >/dev/null 2>&1 || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPY* MAINTAINERS TODO temporary-gnokii-docs/*
%config(noreplace) %{_sysconfdir}/gnokiirc
%attr(4750,root,gnokii) %{_sbindir}/mgnokiidev
%{_bindir}/gnokii
%{_bindir}/sendsms
%{_bindir}/gnokiid
%{_libdir}/libgnokii.so.*
%{_mandir}/man1/gnokii.1*
%{_mandir}/man1/sendsms.1*
%{_mandir}/man8/gnokiid.8*
%{_mandir}/man8/mgnokiidev.8*

%files -n xgnokii
%defattr(-,root,root,-)
%doc xgnokii/ChangeLog xgnokii/README.vcard
%{_bindir}/xgnokii
%{_datadir}/pixmaps/xgnokii.png
%{_datadir}/applications/*xgnokii.desktop
%{_mandir}/man1/xgnokii.1*

%files smsd
%defattr(-,root,root,-)
%doc smsd/action smsd/ChangeLog smsd/README README.smsd2mail smsd2mail.sh
%attr(-,gnokii,gnokii) %config(noreplace) %{_sysconfdir}/sysconfig/gnokii-smsd
%config(noreplace) %{_sysconfdir}/logrotate.d/gnokii-smsd
%{_initrddir}/gnokii-smsd
%{_bindir}/gnokii-smsd
%{_mandir}/man8/gnokii-smsd.8*
%dir %{_libdir}/smsd/
%{_libdir}/smsd/libsmsd_file.so

%files smsd-pgsql
%defattr(-,root,root,-)
%doc smsd/sms.tables.pq.sql
%{_libdir}/smsd/libsmsd_pq.so

%files smsd-mysql
%defattr(-,root,root,-)
%doc smsd/sms.tables.mysql.sql
%{_libdir}/smsd/libsmsd_mysql.so

%files smsd-sqlite
%defattr(-,root,root,-)
# %doc smsd/sms.tables.sqlite.sql
%{_libdir}/smsd/libsmsd_sqlite.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/gnokii*
%{_libdir}/libgnokii.so
%{_libdir}/pkgconfig/gnokii.pc
%{_libdir}/pkgconfig/xgnokii.pc

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.6.30-2
- 为 Magic 3.0 重建

* Sun Oct 09 2011 Robert Scheck <robert@fedoraproject.org> 0.6.30-1
- Update to 0.6.30 and added SQLite subpackage (#466880, #735717)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 0.6.29-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Bastien Nocera <bnocera@redhat.com> 0.6.29-1
- Update to 0.6.29

* Mon Sep 07 2009 Bastien Nocera <bnocera@redhat.com> 0.6.28-1
- Update to 0.6.28

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.6.27-7
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Ville Skyttä <ville.skytta at iki.fi> - 0.6.27-5
- Build with pcsc-lite and readline support (#430387).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Robert Scheck <robert@fedoraproject.org> 0.6.27-3
- Rebuild for MySQL 5.1

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.27-2
- Fix htmlview patch

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.27-1
- Update to 0.6.27

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.26-3
- Rebuild

* Thu Jun 19 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.26-2
- Rebuild with libical support

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.26-1
- Update to 0.6.26

* Fri May 23 2008 Robert Scheck <robert@fedoraproject.org> 0.6.25-2
- Set empty --vendor rather none for using desktop-file-install
- Fixed initscript as gnokii-smsd stays in /usr/bin not /usr/sbin

* Mon May 19 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.25-1
- Update to 0.6.25

* Thu Mar 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.24-1
- Update to 0.6.24

* Mon Feb 11 2008 - Linus Walleij <triad@df.lth.se> - 0.6.22-3
- Rebuild for GCC 4.3.

* Thu Dec 6 2007 - Linus Walleij <triad@df.lth.se> - 0.6.22-2
- Pick up new libssl .solib version dependency.

* Thu Nov 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.6.22-1
- Update to 0.6.22

* Thu Nov 01 2007 - Bastien Nocera <bnocera@redhat.com> - 0.6.20-1
- Update to 0.6.20

* Sun Oct 28 2007 Jeremy Katz <katzj@redhat.com> - 0.6.18-3
- Even better multilib fixing (#335161)

* Tue Oct 23 2007 - Jeremy Katz <katzj@redhat.com> - 0.6.18-2
- Quick fix to multilib conflict (#335161)

* Fri Aug 17 2007 - Linus Walleij <triad@df.lth.se> - 0.6.18-1
- New upstream release

* Fri Aug 17 2007 - Linus Walleij <triad@df.lth.se> - 0.6.17-2
- Update license field from GPL to GPLv2+

* Wed Jul 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.6.17-1
- New upstream release

* Mon Jul 02 2007 - Bastien Nocera <bnocera@redhat.com> - 0.6.16-1
- New upstream release
- Update smsd name change patch
- ppm2nokia, waitcall and todologo have moved to gnokii-extras, as per
  upstream

* Wed Dec 06 2006 Linus Walleij <triad@df.lth.se> - 0.6.14-3
- Rebuild to pick up new libpq IF

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.6.14-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Linus Walleij <triad@df.lth.se> - 0.6.14-1
- New upstream release.

* Tue Aug 29 2006 Linus Walleij <triad@df.lth.se> - 0.6.13-3
- Rebuild for Fedora Extras 6.

* Fri Aug 11 2006 Linus Walleij <triad@df.lth.se> - 0.6.13-2
- Bump because tagged before committing sources and I just
  dont know how the f* you delete a tag in CVS at the moment
  and it does seem like a too big endavour to find out just
  in order to have a nice release tag.

* Thu Aug 10 2006 Linus Walleij <triad@df.lth.se> - 0.6.13-1
- New upstream release.
- New dependency on libusb for USB serial, DKU no longer needed/wanted
  so now we have that troublesome issue resolved once and for all.
- Remove patches to SQL files: these are now fixed upstream!

* Mon Jun 12 2006 Linus Walleij <triad@df.lth.se> - 0.6.12-4
- Rebuilding due to changed interface on libbluetooth.

* Sun Apr 2 2006 Linus Walleij <triad@df.lth.se> - 0.6.12-4
- Goofed up. Fixit it...

* Sun Apr 2 2006 Linus Walleij <triad@df.lth.se> - 0.6.12-3
- Post-import updates.

* Thu Mar 31 2006 Linus Walleij <triad@df.lth.se> - 0.6.12-2
- Updated after comments from Ville.

* Thu Mar 16 2006 Linus Walleij <triad@df.lth.se> - 0.6.12-1
- New upstream tarball

* Wed Mar 8 2006 Linus Walleij <triad@df.lth.se> - 0.6.11-2
- Updated after comments from Ville.

* Sun Mar 5 2006 Linus Walleij <triad@df.lth.se> - 0.6.11-1
- 0.6.11
- Modified to drop into the Fedora Extras as the nice package it now is
- Based work off Ville's good olde package

* Sun Nov 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.10-0.lvn.1
- 0.6.10.
- Clean up pkgconfig file and -devel dependencies from bits needed only
  for static libs.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.6.9-0.lvn.1
- 0.6.9, desktop entry file included upstream.
- Drop zero Epochs.

* Sat Aug  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.8-0.lvn.1
- 0.6.8.
- Don't ship static libraries.
- Rename smsd to gnokii-smsd to avoid conflicts with smstools.
- Remove not included files instead of using %%exclude.

* Sat Jun  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.7-0.lvn.2
- BuildRequire openssl-devel to work around https://bugzilla.redhat.com/159569

* Thu Jun  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.7-0.lvn.1
- 0.6.7.
- Build unconditionally with bluetooth support.

* Mon May  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.5-0.lvn.1
- 0.6.5.

* Fri Nov  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.4-0.lvn.2
- Rename -smsd-postgresql to -smsd-pgsql for consistency with other similar
  packages in FC/Extras.

* Fri Oct 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.4-0.lvn.1
- Update to 0.6.4, perms and pgsql patches applied upstream.
- Xgnokii help locale symlink hack no longer necessary.
- Don't remove user/group on last erase, move smsd user to -smsd subpackage.
- Add libical support (disabled), rebuild with "--with libical" to enable.

* Mon Jul  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.3-0.lvn.1
- Update to 0.6.3.

* Sun Jun 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.lvn.4
- Improve Xgnokii desktop entry according to GNOME HIG.

* Sun Jun 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.lvn.3
- Remove duplicate gettext build dependency (bug 95).

* Sun Jun  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.lvn.2
- Fix chown syntax in smsd init script.
- Summary and description improvements.
- Trim $RPM_OPT_FLAGS out from gnokii.pc.
- Make -devel require XFree86-devel.

* Sun Apr 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.lvn.1
- Update to 0.6.1.

* Thu Mar 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.0-0.lvn.2
- Make -devel require pkgconfig.

* Mon Feb 23 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.0-0.lvn.1
- Update to 0.6.0.

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.10-0.lvn.1
- Update to 0.5.10.

* Tue Jan 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.9-0.lvn.1
- Update to 0.5.9.
- Specfile cleanups, small init script enhancements.

* Sat Dec 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.7-0.lvn.1
- Update to 0.5.7.
- Move smsd man page into -smsd subpackage.

* Sat Nov 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.6-0.lvn.1
- Update to 0.5.6.
- Include sample action script for forwarding SMSD messages to mail.
- s/fedora/livna/.
- Specfile and init script cleanups.

* Sat Jul 19 2003 Warren Togami <warren@togami.com> - 0:0.5.2-0.fdr.2
- Disable smp flags to prevent build failure

* Sun Jun 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.2-0.fdr.1
- Update to 0.5.2.

* Thu May 29 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.1-0.fdr.1
- Update to 0.5.1.
- Include init script, sysconfig and logrotate config for smsd.

* Tue May 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.0-0.fdr.1
- Update to 0.5.0.

* Sun Nov  3 2002 Ville Skyttä <ville.skytta at iki.fi> 0.4.3-1cr
- RedHat'ified PLD version.
