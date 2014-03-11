
%define snap 20111207
#define pre rc1

Summary: Basic desktop integration functions 
Name:    xdg-utils
Version: 1.1.0
Release: 0.12.%{snap}%{?dist}

URL:     http://portland.freedesktop.org/ 
%if 0%{?snap:1}
Source0: xdg-utils-%{version}-%{snap}git.tar.gz
Source1: xdg-utils-git_checkout.sh
%else
Source0: http://portland.freedesktop.org/download/xdg-utils-%{version}%{?pre:-%{pre}}.tar.gz
%endif
License: MIT 
Group:   System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%if 0%{?snap}
BuildRequires: gawk
BuildRequires: xmlto
%endif

Requires: coreutils
Requires: desktop-file-utils
Requires: which

%if 0%{?fedora} && 0%{?fedora} < 16
Obsoletes: htmlview <= 4.0.0
%endif

%description
The %{name} package is a set of simple scripts that provide basic
desktop integration functions for any Free Desktop, such as Linux.
They are intended to provide a set of defacto standards.  
This means that:
*  Third party software developers can rely on these xdg-utils
   for all of their simple integration needs.
*  Developers of desktop environments can make sure that their
   environments are well supported
*  Distribution vendors can provide custom versions of these utilities

The following scripts are provided at this time:
* xdg-desktop-icon      Install icons to the desktop
* xdg-desktop-menu      Install desktop menu items
* xdg-email             Send mail using the user's preferred e-mail composer
* xdg-icon-resource     Install icon resources
* xdg-mime              Query information about file type handling and
                        install descriptions for new file types
* xdg-open              Open a file or URL in the user's preferred application
* xdg-screensaver       Control the screensaver
* xdg-settings          Get various settings from the desktop environment


%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}


%build
%configure

%if 0%{?snap:1}
make scripts-clean -C scripts 
make man scripts %{?_smp_mflags} -C scripts
%endif
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{_bindir}/xdg-desktop-icon
%{_bindir}/xdg-desktop-menu
%{_bindir}/xdg-email
%{_bindir}/xdg-icon-resource
%{_bindir}/xdg-mime
%{_bindir}/xdg-open
%{_bindir}/xdg-screensaver
%{_bindir}/xdg-settings
%{_mandir}/man1/xdg-desktop-icon.1*
%{_mandir}/man1/xdg-desktop-menu.1*
%{_mandir}/man1/xdg-email.1*
%{_mandir}/man1/xdg-icon-resource.1*
%{_mandir}/man1/xdg-mime.1*
%{_mandir}/man1/xdg-open.1*
%{_mandir}/man1/xdg-screensaver.1*
%{_mandir}/man1/xdg-settings.1*


%clean
rm -rf %{buildroot}


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.0-0.12.20111207
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.11.20111207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.10.20110714git
- fix gnome-screensaver detection bogosity (#702540,#736159)
- xdg-open: x-www-browser: command not found (#755553)
- drop htmlview hackage

* Thu Jul 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.9.20110714
- 20110714 snapshot
- xdg-mime : use 'file --mime-type' instead of 'file -i'

* Thu Jun 16 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.8.20110510
- rebuild

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.7.20110510
- fix gnome3 detection, gnome-default-applications-properties error output

* Thu May 05 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.6.20110505
- Error in xdg-open script (#702347)

* Wed May 04 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.5.20110504
- 20110504 snapshot
- xdg-email does not work (#690840)

* Fri Apr 08 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.4.20110408
- 20110408 snapshot
- Shouldn't use user's defaults.list (#678656)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.3.20110201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.2.20110201
- 20110201 snapshot
- add gnome3 support, make default browser work again for xdg-settings (#654746)

* Mon Jan 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-0.1.rc1
- xdg-utils-1.1.0-rc1

* Thu Oct 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-21.20101028
- lxde support (#580835, fdo#26058))

* Fri Jul 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-20.20100709
- xdg-screensaver: consider gnome-screensaver a separate DE (fdo#20027)

* Fri Jul 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-19.20100709
- xdg-open man page needs updating to include FILE and SEE ALSO (#603841)
- xdg-open should call mimeopen with -L option (#430072)
- xdg-desktop-icon :  use localized desktop folder name (fdo#19011)

* Fri Apr 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-18.20100409
- xdg-settings fixes (#580715, fdo#26284)

* Mon Jan 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-17.20100118cvs
- xdg-screensaver resume activates the screensaver on KDE4 (fdo#26085) 

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-16.20091217cvs
- xdg-mime: line 531: kde-config: command not found (#545702)
- xdg-email calls gconftool which doesn't exist (#548529)

* Mon Nov 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-15.20091016cvs
- add Obsoletes: htmlview (#541179, f13+)

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-14.20091016cvs
- prefer gvfs-open over gnome-open (#529287)
- DE=gnome, if org.gnome.SessionManager exists on dbus (#529287)

* Mon Sep 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-13.20090928cvs
- xdg-open: use kde-open

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-12.20090921cvs
- suppress stderr from kde-config (#524724)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-11.20090913cvs
- 20090913cvs snapshot
- xdg-open in xdg-utils expects xprop to be available (#506857)

* Mon Aug 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-10.20090824cvs
- 20090824cvs snapshot

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9.20081121cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-8.20081121cvs
- revert.  kfmclient openURL is largely useless 

* Wed Apr 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-7.20081121cvs
- xdg-open: s/kfmclient exec/kfmclient openURL/ (CVE-2009-0068, rh#472010, fdo#19377)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6.20081121cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-5.20081121cvs
- upstreamed a few more patches, rebase to cvs snapshot

* Fri Jan 25 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.0.2-4
- Fix for CVE-2008-0386 (#429513)

* Fri Jan 18 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-3
- fix mimeopen support (#429280)
- spec cosmetics: cleanup macro usage

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-2
- Requires: which (#312601)

* Sun Jun 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-1
- xdg-utils-1.0.2

* Mon Apr 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-3
- add htmlview,links to browser fallbacks

* Tue Dec 19 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-2
- fix typo in xdg-icon-resource manpage

* Mon Nov 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.1-1
- xdg-utils-1.0.1

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net 1.0-3
- actually *use* mimeopen patch (#210797)

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-2
- prefer mimeopen as generic default (#210797)

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-1
- 1.0(final)

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.9.rc1
- update %%description (#208926)

* Wed Sep 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.8.rc1
- 1.0rc1

* Fri Sep 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.7.beta4
- 1.0beta4

* Mon Aug 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.6.beta3
- 1.0beta3

* Thu Jul 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.5.20060721
- Release: append/use %%{?dist}

* Wed Jul 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.4.20060721
- specfile cosmetics, tabs -> spaces
- %%makeinstall -> make install DESTDIR=...

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.3.20060721
- 20060721 snapshot
- optgnome.patch

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.2.beta1
- Requires: desktop-file-utils

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.1.beta1
- 1.0beta1

