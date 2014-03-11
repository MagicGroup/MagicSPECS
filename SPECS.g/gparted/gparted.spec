Summary:	Gnome Partition Editor
Name:		gparted
Version:	0.13.1
Release:	2%{?dist}
Group:		Applications/System
License:	GPLv2+
URL:		http://gparted.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	gparted-console.apps
Source2:	gparted-pam.d
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gtkmm24-devel parted-devel 
BuildRequires:	libuuid-devel gettext perl(XML::Parser) 
BuildRequires:	desktop-file-utils gnome-doc-utils intltool
BuildRequires:  rarian-compat
BuildRequires:  pkgconfig

%description
GParted stands for Gnome Partition Editor and is a graphical frontend to
libparted. Among other features it supports creating, resizing, moving
and copying of partitions. Also several (optional) filesystem tools provide
support for filesystems not included in libparted. These optional packages
will be detected at runtime and don't require a rebuild of GParted

%prep
%setup -q

%build
%configure --enable-libparted-dmraid
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

sed -i 's#_X-GNOME-FullName#X-GNOME-FullName#' %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --delete-original			\
        --vendor fedora					\
        --dir %{buildroot}%{_datadir}/applications	\
	--mode 0644					\
        --add-category X-Fedora				\
        --add-category GTK				\
        %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's#sbin#bin#' %{buildroot}%{_datadir}/applications/fedora-%{name}.desktop

#### consolehelper stuff
mkdir -p %{buildroot}%{_bindir}
ln -s consolehelper %{buildroot}%{_bindir}/gparted

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/security/console.apps/gparted

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/gparted

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/gparted
%{_sbindir}/gparted
%{_sbindir}/gpartedbin
%{_datadir}/applications/fedora-gparted.desktop
%{_datadir}/icons/hicolor/*/apps/gparted.*
%{_datadir}/gnome/help/gparted/
%{_datadir}/omf/gparted/
%{_mandir}/man8/gparted.*
%config(noreplace) %{_sysconfdir}/pam.d/gparted
%config(noreplace) %{_sysconfdir}/security/console.apps/gparted

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.13.1-2
- 为 Magic 3.0 重建

* Mon Sep 24 2012 Deji Akingunola <dakingun@gmail.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.12.0-3
- rebuild (parted)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-2
- Rebuilt for c++ ABI breakage

* Wed Feb 22 2012 Deji Akingunola <dakingun@gmail.com> - 0.12.0-1
- Update to version 0.12.0

* Fri Jan 27 2012 Deji Akingunola <dakingun@gmail.com> - 0.11.0-1
- Update to version 0.11.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.0-1
- Update to version 0.10.0

* Wed Oct 19 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.1-1
- Update to version 0.9.1

* Wed Jul 20 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.0-1
- Update to version 0.9.0

* Mon Jul 04 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.1-2
- Apply upstream patch to build with parted-3.0
- Enable parted dmraid support

* Sun Jun 26 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.1-1
- Update to version 0.8.1

* Thu Feb 17 2011 Deji Akingunola <dakingun@gmail.com> - 0.8.0-1
- Update to version 0.8.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.1-1
- Update to version 0.7.1

* Fri Oct 29 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.0-1
- Update to version 0.7.0

* Sun Oct 17 2010 Deji Akingunola <dakingun@gmail.com> - 0.6.4-1
- Update to version 0.6.4

* Fri Aug 06 2010 Deji Akingunola <dakingun@gmail.com> - 0.6.2-1
- Update to version 0.6.2

* Mon Jun 21 2010 Deji Akingunola <dakingun@gmail.com> - 0.6.0-1
- Update to version 0.6.0

* Thu Apr 01 2010 Mike McGrath <mmcgrath@redhat.com> - 0.5.2-1.1
- Rebuilt to fix broken parted dep

* Fri Mar 12 2010 Deji Akingunola <dakingun@gmail.com> - 0.5.2-1
- Update to version 0.5.2

* Tue Jan 26 2010 Deji Akingunola <dakingun@gmail.com> - 0.5.1-1
- Update to version 0.5.1

* Wed Jan 13 2010 Deji Akingunola <dakingun@gmail.com> - 0.5.0-1
- Update to version 0.5.0

* Mon Nov 16 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.8-1
- New upstream version

* Mon Aug 10 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.6-1
- New upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.5-2
- Change e2fsprog-devel BR to libuuid-devel, and rebuild for parted soname bump

* Sat May 09 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.5-1
- New upstream version

* Mon Apr 06 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.4-1
- New upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.3-1
- New upstream version, fixes the automounting bug (RH #468953)

* Tue Feb 10 2009 Deji Akingunola <dakingun@gmail.com> - 0.4.2-1
- New upstream version

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 0.4.1-1
- New upstream version

* Mon Sep 22 2008 Deji Akingunola <dakingun@gmail.com> - 0.3.9-1
- New upstream version
- Finally removed the 'preun' call that ensures the old gparted fdi (pre-FC6)
  file is removed on update

* Sun Jul 13 2008 Deji Akingunola <dakingun@gmail.com> - 0.3.8-1
- New upstream version

* Wed Apr 30 2008 Deji Akingunola <dakingun@gmail.com> - 0.3.7-1
- New upstream version

* Fri Mar 28 2008 Deji Akingunola <dakingun@gmail.com> - 0.3.6-1
- New upstream version

* Thu Feb 07 2008 Deji Akingunola <dakingun@gmail.com> - 0.3.5-1
- New upstream version

* Thu Nov 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-14
- Fix to detect full path to device/partition pathname (Bug #395071)

* Tue Oct 30 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-13
- Fix crash after refresh bug (Bug #309251, patch by Jim Hayward)
- Fix to use realpath properly (Bug #313281, patch by Jim Hayward)

* Wed Aug 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-12
- Rebuild

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-12
- License tag update

* Mon Jun 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-11
- Apply patch to only detect real devices, useful for correcting gparted slow 
 startup in situations when floppy drives don't exist but are enabled in bios
 (BZ #208821).

* Wed Apr 18 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-10
- Fix another typos in the run-gparted script

* Mon Apr 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-9
- Fix the typos and stupidity in the consolehelper and hal-lock files

* Mon Apr 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-8
- Explicitly require hal >= 0.5.9
- Remove the hal policy file created by gparted (if it's still there) on upgrade

* Mon Apr 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-7
- Patch gparted to not create a hal fdi file but use hal-lock instead, this will hopefully fix BZ #215657
- Clean up the spec file

* Wed Mar 21 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-6
- Rebuild for GNU parted-1.8.6

* Tue Mar 20 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-5
- Rebuild for GNU parted-1.8.5

* Wed Jan 24 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-4
- Re-write the consolehelpher stuff to work with latest pam

* Tue Jan 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-3
- The new parted is back, rebuild again

* Sat Jan 13 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.3-2
- Rebuild for new parted

* Thu Dec 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.3-1
- Bug fix release

* Tue Dec 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.2-1
- New release

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-5
- Add more BRs

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-4
- Complete fix for parted check and apply patch on configure.in

* Wed Nov 23 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-3
- Backport a fix from cvs to properly check for libparted version

* Mon Nov 21 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-2
- Rebuild for new parted

* Wed Sep 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.3.1-1
- New version 0.3.1

* Tue Sep 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.3-1
- New version 0.3

* Mon Aug 28 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-3
- Rebuild for FC6

* Mon May 22 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-2
- Rebuild

* Mon May 22 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.5-1
- Update to version 0.2.5

* Mon Apr 17 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.4-2
- Rebuild for new parted

* Wed Apr 12 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.4-1
- Update to newer version

* Thu Mar 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.3-1
- Update to newer version

* Mon Mar 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.2-1
- New release

* Mon Feb 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.2-2
- Rebuild for Fedora Extras 5

* Mon Jan 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.2-1
- New release

* Wed Jan 11 2006 Deji Akingunola <dakingun@gmail.com> - 0.1-1
- New release

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-3
- Use correct source url

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-2
- Add more buildrequires and cleanup spec file

* Fri Nov 25 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.9-1 
- Update to latest released version

* Wed Oct 26 2005 Deji Akingunola <dakingun@gmail.com> - 0.0.8-1
- initial Extras release
