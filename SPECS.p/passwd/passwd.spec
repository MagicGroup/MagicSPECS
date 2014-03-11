%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 0
%endif
%if %{?WITH_AUDIT:0}%{!?WITH_AUDIT:1}
%define WITH_AUDIT 0
%endif
Summary: An utility for setting or changing passwords using PAM
Name: passwd
Version: 0.78
Release: 5%{?dist}
License: BSD or GPLv2+
Group: System Environment/Base
URL: http://fedorahosted.org/passwd
Source: https://fedorahosted.org/releases/p/a/%{name}/%{name}-%{version}.tar.bz2
Patch1: passwd-0.78-postlogin.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: pam >= 1.1.3-7, /etc/pam.d/system-auth
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
BuildRequires: glib2-devel, libuser-devel, pam-devel, libuser >= 0.53-1
BuildRequires: gettext, popt-devel
%if %{WITH_AUDIT}
BuildRequires: audit-libs-devel >= 1.0.14
Requires: audit-libs >= 1.0.14
%endif

%description
This package contains a system utility (passwd) which sets
or changes passwords, using PAM (Pluggable Authentication
Modules) library.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .postlogin

%build
%configure \
%if %{WITH_SELINUX}
        --with-selinux \
%else
        --without-selinux \
%endif
%if %{WITH_AUDIT}
        --with-audit
%else
        --without-audit
%endif
make DEBUG= RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
install -m 644 passwd.pamd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/passwd
%find_lang %{name}
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
    dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
    lang=$(basename $dir)
    echo "%%lang($lang) $dir/man*/*" >> %{name}.lang
done


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/passwd
%attr(4755,root,root) %{_bindir}/passwd
%{_mandir}/man1/passwd.1*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.78-5
- 为 Magic 3.0 重建

* Sat Jan 21 2012 Liu Di <liudidi@gmail.com> - 0.78-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Tomas Mraz <tmraz@redhat.com> 0.78-3
- add the postlogin substack to the PAM configuration (#665063)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 16 2010 Tomas Mraz <tmraz@redhat.com> 0.78-1
- added japanese translation of the man page (#611692)
- updated translations

* Tue Apr  6 2010 Tomas Mraz <tmraz@redhat.com> 0.77-5
- first part of fix for pam_gnome_keyring prompting (#578624)
  needs support for use_authtok to be added to pam_gnome_keyring

* Thu Jan 28 2010 Tomas Mraz <tmraz@redhat.com> 0.77-4
- add COPYING and other things to doc
- correct the licence field

* Mon Sep 14 2009 Tomas Mraz <tmraz@redhat.com> 0.77-1
- updated translations
- improved manual page

* Wed Feb 11 2009 Tomas Mraz <tmraz@redhat.com> 0.76-1
- identify SHA-256 and SHA-512 password hashes (#484994)

* Tue Apr  8 2008 Tomas Mraz <tmraz@redhat.com> 0.75-2
- add optional pam_gnome_keyring module to passwd pam
  config (#441225)

* Wed Feb 20 2008 Tomas Mraz <tmraz@redhat.com> 0.75-1
- fix disabling SELinux and audit in spec (#433284)
- remove obsolete no.po (#332121)
- updated translations

* Tue Sep 25 2007 Tomas Mraz <tmraz@redhat.com> 0.74-5
- buildrequires popt-devel

* Wed Aug 22 2007 Tomas Mraz <tmraz@redhat.com> 0.74-4
- spec file cleanups

* Thu Apr  5 2007 Tomas Mraz <tmraz@redhat.com> 0.74-3
- use std buildroot, add dist tag (#226232)

* Tue Jan 30 2007 Tomas Mraz <tmraz@redhat.com> 0.74-2
- do not explicitly strip the binary

* Tue Dec 12 2006 Tomas Mraz <tmraz@redhat.com> 0.74-1
- minor fixes in error reporting
- localize messages (#204022)

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> 0.73-1
- fixed broken logic from the last change (#196851)

* Fri Jul 14 2006 Tomas Mraz <tmraz@redhat.com> 0.72-1
- merged audit patch to upstream cvs
- improved passwd -S output (#170344)
- make passwd -d work with stripped down proc (#196851)
- corrected link to pam docs (#193084)
- spec file cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.71-3.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.71-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.71-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Steve Grubb <sgrubb@redhat.com> 0.71-3
- Adjust audit patch so it builds without libaudit

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct 25 2005 Steve Grubb <sgrubb@redhat.com> 0.71-2
- adjust audit communication to use common logging functions

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com> 0.71-1
- use include instead of pam_stack in pam config

* Fri Jun 17 2005 Tomas Mraz <tmraz@redhat.com> 0.70-1
- replace laus with audit
- auto* build changes

* Fri Jan 28 2005 Jindrich Novy <jnovy@redhat.com> 0.69-1
- spec file fixes
- add libuser >= 0.53-1 BuildPrereq (#139331)

* Tue Jan 25 2005 Dan Walsh <dwalsh@redhat.com>
- improve SELinux priv checking

* Mon Aug 23 2004 Jindrich Novy <jnovy@redhat.com>
- applied cleanup patch from Steve Grubb #120060
- fixed man page #115380
- added libselinux-devel to BuildPrereq #123750, #119416

* Wed Aug 19 2004 Jindrich Novy <jnovy@redhat.com> 0.68-10
- moved to 0.68-10 to fix problem with RHEL4-Alpha4 #129548
- updated GNU build scripts and file structure to recent style

* Wed Feb 4 2004 Dan Walsh <dwalsh@redhat.com> 0.68-8
- add check for enforcing mode

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 0.68-7
- fix is_selinux_enabled

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 0.68-6
- turn off selinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 0.68-5.sel
- Add SELinux support

* Mon Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 0.68-4
- Add SELinux support

* Thu Feb 13 2003 Nalin Dahyabhai <nalin@redhat.com> 0.68-3
- add aging adjustment flags to passwd(1)'s synopsis, were just in the
  reference section before

* Mon Jan 27 2003 Nalin Dahyabhai <nalin@redhat.com> 0.68-2
- rebuild

* Mon Dec  9 2002 Nalin Dahyabhai <nalin@redhat.com> 0.68-1
- implement aging adjustments for pwdb

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.67-4
- modify default PAM configuration file to not specify directories, so that
  the same configuration can be used for all arches on multilib systems
- fix BuildPrereq on glib-devel to specify glib2-devel instead
- remove unpackaged files in %%install phase

* Tue May 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.67-3
- rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.67-2
- rebuild in new environment

* Wed Mar 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.67-1
- add the -i, -n, -w, and -x options to passwd

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.65-5
- rebuild

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.65-4
- rebuild

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 0.65-3
- rebuild

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.65-2
- rebuild to get dependencies right

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.65-1
- change dependency from pwdb to libuser

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.64.1-9
- rebuild

* Thu Aug 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.64.1-8
- man page fix (-r is the opposite of -l, not --stdin, which precedes it)
  from Felipe Gustavo de Almeida

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com> 0.64.1-7
- fix unguarded printf() (noted by Chris Evans)
- add missing build dependency on pwdb and pam-devel (#49550)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages to _mandir

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth
- modify for building as non-root users

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- fix manpage links

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- document --stdin in man page
- fix for gzipped man pages

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- first build from the new source code base.
