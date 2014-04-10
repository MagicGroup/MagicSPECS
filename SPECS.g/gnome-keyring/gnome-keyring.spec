%define glib2_version 2.32.0
%define gcr_version 3.5.3
%define dbus_version 1.0
%define gcrypt_version 1.2.2
%define libtasn1_version 0.3.4

Summary: Framework for managing passwords and other secrets
Summary(zh_CN.UTF-8): 管理密码和其它秘密的框架
Name: gnome-keyring
Version:	3.12.0
Release: 1%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
#VCS: git:git://git.gnome.org/gnome-keyring
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/gnome-keyring/%{majorver}/gnome-keyring-%{version}.tar.xz
URL: http://www.gnome.org

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gcr-devel >= %{gcr_version}
BuildRequires: dbus-devel >= %{dbus_version}
BuildRequires: libgcrypt-devel >= %{gcrypt_version}
BuildRequires: libtasn1-devel >= %{libtasn1_version}
BuildRequires: pam-devel
BuildRequires: autoconf, automake, libtool
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libtasn1-tools
BuildRequires: gtk-doc
BuildRequires: libcap-ng-devel
BuildRequires: p11-kit-devel
BuildRequires: gcr-devel

# we no longer have a devel subpackage
Obsoletes: %{name}-devel < 3.3.0
Provides:  %{name}-devel = 3.3.0

%description
The gnome-keyring session daemon manages passwords and other types of
secrets for the user, storing them encrypted with a main password.
Applications can use the gnome-keyring library to integrate with the keyring.

%description -l zh_CN.UTF-8
这个服务管理密码和其它类型的秘密，以一个主密码加密存储它们。
可以和应用程序集成。

%package pam
Summary: Pam module for unlocking keyrings
Summary(zh_CN.UTF-8): 解锁密钥的 pam 模块
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
# for /lib/security
Requires: pam

%description pam
The gnome-keyring-pam package contains a pam module that can
automatically unlock the "login" keyring when the user logs in.

%description pam -l zh_CN.UTF-8
解锁密钥的 pam 模块。

%prep
%setup -q -n gnome-keyring-%{version}

%build
%configure \
           --with-pam-dir=/%{_lib}/security \
           --enable-pam

# avoid unneeded direct dependencies
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_lib}/security/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/devel/*.la
magic_rpm_clean.sh
%find_lang gnome-keyring

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :


%files -f gnome-keyring.lang
%doc AUTHORS NEWS README COPYING COPYING.LIB
# LGPL
%dir %{_libdir}/gnome-keyring
%dir %{_libdir}/gnome-keyring/devel
%{_libdir}/gnome-keyring/devel/*.so
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/*.so
# GPL
%attr(0755,root,root) %caps(cap_ipc_lock=ep) %{_bindir}/gnome-keyring-daemon
%{_bindir}/gnome-keyring
%{_bindir}/gnome-keyring-3
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/*
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/p11-kit/modules/gnome-keyring.module

%files pam
/%{_lib}/security/*.so


%changelog
* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.12.0-1
- 更新到 3.12.0

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Mon Jan 14 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.7.2-2
- Fix crash on parsing some certificates (#893162)

* Fri Nov 23 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Fri Nov 09 2012 Rex Dieter <rdieter@fedoraproject.org> 3.6.1-2
- WARNING: couldn't connect to: /tmp/keyring-... (#783568, gnome#665961)

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Stef Walter <stefw@redhat.com> - 3.5.5-2
- Update for renamed gnome-keyring.module file
- Update sources

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Wed Mar 26 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Fri Mar  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Wed Jan 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-2
- Fix a problem that prevents the ssh-agent from working

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.3.3.1-3
- Properly obsolete dead -devel subpackage (#771299)

* Mon Dec 26 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.3.3.1-2
- Fix libgnome-keyring dep version syntax.

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-1
- Update to 3.3.3.1
- No more devel package

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Tue May 10 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-2
- Improved libcap-ng patches

* Mon May  9 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Tue Mar 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.92-3
- Update the pam module selinux patch

* Tue Mar 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.92-2
- Set correct SELinux context of daemon started from the pam module (#684225)

* Fri Mar 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.91-1
- Update to 2.91.91

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-7
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-5
- Rebuild against new gtk

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.91.4-4
- Dir ownership fixes.

* Mon Jan 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.4-3
- Use file system based capabilities instead of suid bit (#668831)

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-2
- Rebuild against new gtk

* Mon Jan  3 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild against new gtk

* Tue Nov 30 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Tue Nov  9 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-2
- Rebuild against newer gtk3

* Mon Oct 11 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct  4 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Sat Sep 25 2010 Owen Taylor <otaylor@redhat.com> - 2.31.92-2
- Bump and rebuild for GTK3 ABI changes

* Mon Sep 13 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.92-1
- Update to 2.31.92
- Built against gtk3

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-3
- Co-own /usr/share/gtk-doc (#604359)
- Some spec file cleanups

* Tue Jul 20 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.4-2
- ssh-agent: fix key unlocking (#611642)

* Tue Jun 29 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Thu Jun 24 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.3-1
- Update to 2.30.3

* Mon May  3 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.1-2
- Enable daemon autostart in XFCE
- Fix Networkmanager can no longer find secrets service (#572137)

* Tue Apr 27 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Mar 22 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.92-2
- More robust error display and handling
- [secret-store] Don't save session keyring to disk
- [dbus] Allow unlocking even when always unlock is not available
- [dbus] Hide the automatically unlock check when login not usable
- [login] Fix various issues storing and using auto unlock passwords

* Wed Mar 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Tue Feb 16 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.90-2
- Backport fixes from master related to storing secret value

* Tue Feb  9 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Mon Feb  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.5-4
- Backport some fixes related to password saving

* Mon Feb  1 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.5-3
- Fix hidden entry boxes in the new password prompt (#560345)

* Mon Jan 25 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.5-2
- Fix endless loop when looking for password in login keyring
- Fix undefined reference to S_ISSOCK (#557970)

* Mon Jan 11 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.5-1
- Update to 2.29.5

* Thu Jan  7 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.4-1
- Update to 2.29.4

* Mon Sep 21 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Thu Jul  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-2
- Rebuild

* Sun Apr 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-keyring/2.26/gnome-keyring-2.26.1.news

* Wed Apr  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-4
- Fix service activation

* Tue Apr  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-3
- Revert the previous patch since it causes crashes

* Thu Apr 02 2009 Richard Hughes  <rhughes@redhat.com> - 2.26.0-2
- Fix a nasty bug that's been fixed upstream where gnome-keyring-daemon
  would hang when re-allocating from a pool of secure memory.

* Mon Mar 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-4
- Update to 2.25.90

* Tue Jan 20 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Thu Jan  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4.2-1
- Update to 2.25.4.2

* Tue Jan  6 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.4.1-1
- Update to 2.25.4.1

* Mon Jan  5 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Sat Dec 20 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-3
- Init dbus later (fixes ssh-agent,
  patch from Yanko Kaneti, bug 476300)

* Fri Dec 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-2
- Update to 2.25.2

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Tweak description

* Mon Nov 10 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Sun Oct 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Update to 2.24.0

* Sun Sep  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Thu Sep  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Wed Aug 20 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Mon Aug 11 2008 Colin Walters <walters@redhat.com> - 2.22.3.6-2
- Add --disable-acl-prompts; you can't try to maintain integrity
  between two processes with the same UID and no other form of
  access control.

* Mon Aug  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Thu May 29 2008 Colin Walters <walters@redhat.com> - 2.22.2-2
- Add patch to nuke allow-deny dialog, see linked upstream bug
  for discussion

* Tue May 27 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Sun Feb 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91
- Drop upstreamed patch

* Wed Feb  6 2008 Ray Strode <rstrode@redhat.com> - 2.21.90-2
- Fix problem in patch for bug 430525

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 28 2008 Ray Strode <rstrode@redhat.com> - 2.21.5-3
- Don't ask for a password...ever (bug 430525)

* Mon Jan 21 2008 Matthew Barnes  <mbarnes@redhat.com> - 2.21.5-2
- Fix a race condition that was causing Evolution to hang (#429097)

* Mon Jan 14 2008 Matthias Clasen  <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen  <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Fri Dec  7 2007 Matthias Clasen  <mclasen@redhat.com> - 2.21.3.2-1
- Update to 2.21.3.2

* Fri Nov 30 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20.2-2
- Reenable auto-unlock

* Mon Nov 26 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20.2-1
- Update to 2.20.2

* Sun Nov 11 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20.1-4
- Don't ship a .la file (#370531)

* Thu Oct 25 2007 Christopher Aillon <caillon@redhat.com> - 2.20.1-3
- Rebuild

* Mon Oct 15 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20.1-2
- Disable the auto-unlock question for now (#312531)

* Mon Oct 15 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1
- Drop obsolete patches
- Add bug ref for selinux patch

* Tue Oct  9 2007 Matthias Clasen  <mclasen@redhat.com> - 2.20-6
- Avoid undefined symbols in the pam module

* Mon Oct  8 2007 Alexander Larsson <alexl@redhat.com> - 2.20-5
- Fixed minor issue with pam-selinux issue pointed out by stef

* Thu Oct  4 2007 Alexander Larsson <alexl@redhat.com> - 2.20-4
- Have the pam module tell the daemon to init the login keyring 
  without using the socket as selinux limits access to that

* Thu Oct  4 2007 Alexander Larsson <alexl@redhat.com> - 2.20-3
- Add NO_MATCH error patch from svn. Will fix apps that
  can't handle empty list matches

* Mon Oct 3 2007 Alexander Larsson <alexl@redhat.com> - 2.20-2
- Backport fix from svn where newly created keyrings weren't
  found
- Don't unset default keyring on daemon shutdown

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20-1
- Update to 2.20

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Sun Aug 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6.1-2
- Update License fields

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6.1-1
- Update to 2.19.6.1

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Backport a fix from upstream

* Fri Jul 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6
- Add a pam subpackage

* Mon Jul  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8

* Sat Feb 24 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.92-1
- Update to 0.7.92

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.91-1
- Update to 0.7.91

* Thu Feb  8 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.3-2
- Package review cleanup

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Mon Nov  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Sep  4 2006 Alexander Larsson <alexl@redhat.com> - 0.6.0-1
- update to 0.6.0

* Wed Aug 23 2006 Dan Williams <dcbw@redhat.com> - 0.5.2-2.fc6
- Fix null pointer dereference (Gnome.org #352587)

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.2-1.fc6
- Update to 0.5.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Mon May 29 2006 Alexander Larsson <alexl@redhat.com> - 0.4.9-2
- buildrequire gettext (#193377)

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.9-1
- Update to 0.4.9

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.8-1
- Update to 0.4.8

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.7-1
- Update to 0.4.7

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.4.6-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.4.6-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> 0.4.6-1
- Update to 0.4.6

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> 0.4.5-1
- Update to 0.4.5

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 0.4.4-1
- Update to 0.4.4

* Tue Aug 16 2005 David Zeuthen <davidz@redhat.com> 0.4.3-2
- Rebuilt

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> 0.4.3-1
- New upstream version

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> 0.4.2-1
- New upstream version

* Wed Mar  2 2005 Alex Larsson <alexl@redhat.com> 0.4.1-2
- Rebuild

* Tue Feb  1 2005 Matthias Clasen <mclasen@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Mon Sep 13 2004 Alexander Larsson <alexl@redhat.com> - 0.4.0-1
- update to 0.4.0

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 0.3.3-1
- update to 0.3.3

* Thu Aug 12 2004 Alexander Larsson <alexl@redhat.com> - 0.3.2-1
- update to 0.3.2

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 0.2.0-1
- update to 0.2.0

* Wed Mar 10 2004 Alexander Larsson <alexl@redhat.com> 0.1.90-1
- update to 0.1.90

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Alexander Larsson <alexl@redhat.com> 0.1.4-1
- update to 0.1.4

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 0.1.3-1
- update to 0.1.3

* Mon Jan 26 2004 Bill Nottingham <notting@redhat.com>
- tweak summary

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 0.1.2-2
- devel package only needs glib2-devel, not gtk2-devel

* Fri Jan 23 2004 Alexander Larsson <alexl@redhat.com> 0.1.2-1
- First version
