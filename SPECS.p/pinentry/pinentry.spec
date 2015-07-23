
Name:    pinentry
Version: 0.9.5
Release: 1%{?dist}
Summary: Collection of simple PIN or passphrase entry dialogs

# qt & qt4 subpackage have different license, see subpackage definitions
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

# borrowed from opensuse
Source10: pinentry-wrapper

BuildRequires: gtk2-devel
BuildRequires: libcap-devel
BuildRequires: ncurses-devel
BuildRequires: qt4-devel
BuildRequires: libgpg-error-devel
BuildRequires: libassuan-devel

Requires(pre): %{_sbindir}/update-alternatives
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

Provides: %{name}-curses = %{version}-%{release}

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.

%package gtk
Summary: Passphrase/PIN entry dialog based on GTK+
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Provides: pinentry-gtk2 = %{version}-%{release}
%description gtk
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GTK GUI based version of the PIN entry dialog.

%package qt
Summary: Passphrase/PIN entry dialog based on Qt4
# original code for secstring.cpp doesn't allow GPL versions higher than 3 to be
# used
License: GPLv2 or GPLv3
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Obsoletes: pinentry-qt4 < 0.8.0-2
Provides:  pinentry-qt4 = %{version}-%{release}
%description qt
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the Qt4 GUI based version of the PIN entry dialog.

%package emacs
Summary: Passphrase/PIN entry dialog based on emacs
Requires: %{name} = %{version}-%{release}
%description emacs
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the emacs based version of the PIN entry dialog.

%prep
%setup -q

%build

%if 0%{?fedora} > 22
# FTBFS on f23/gcc5 without this
CXXFLAGS="%{optflags} -std=c++11"
%endif

%configure \
  --disable-rpath \
  --disable-dependency-tracking \
  --without-libcap \
  --enable-pinentry-gtk2 \
  --enable-pinentry-qt4

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Backwards compatibility
ln -s pinentry-gtk-2 $RPM_BUILD_ROOT%{_bindir}/pinentry-gtk
ln -s pinentry-qt4 $RPM_BUILD_ROOT%{_bindir}/pinentry-qt

install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pinentry

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{_infodir}/dir


# alternatives dropped at 0.7.6-3 (use %%trigger instead?)
%pre
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-curses ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gtk ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-emacs ||:

%post
if [ -f %{_infodir}/pinentry.info* ]; then
/sbin/install-info %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi

%preun
if [ $1 -eq 0 -a -f %{_infodir}/pinentry.info* ] ; then
  /sbin/install-info --delete %{_infodir}/pinentry.info %{_infodir}/dir ||:
fi

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/pinentry-curses
%{_bindir}/pinentry
%{_infodir}/pinentry.info*

%files gtk
%{_bindir}/pinentry-gtk
%{_bindir}/pinentry-gtk-2

%files qt
%{_bindir}/pinentry-qt
%{_bindir}/pinentry-qt4

%files emacs
%{_bindir}/pinentry-emacs

%changelog
* Thu Jul 02 2015 Boris Ranto <branto@redhat.com> - 0.9.5-1
- Rebase to latest upstream version
- Removing qt4 pinentry patch -- got merged upstream
- New package pinentry-emacs that hosts pinentry-emacs
- New dependencies on libassuan and libgpg-error (de-bundling)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Boris Ranto <branto@redhat.com> - 0.9.2-1
- Rebase to latest upstream version

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Boris Ranto <branto@redhat.com> - 0.9.1-1
- Rebase to latest upstream version
- There are no longer any moc files so there is no need to patch them

* Fri Mar 13 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.0-3
- fix FTBFS on f23/gcc5
- drop deprecated configure flags

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.9.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Nov 12 2014 Boris Ranto <branto@redhat.com> - 0.9.0-1
- Rebase to latest upstream version

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Boris Ranto <branto@redhat.com> - 0.8.3-6
- fix bogus dates
- upgrade pinentry-wrapper to handle corner cases better

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> - 0.8.3-5
- fix license handling

* Sat Jul 19 2014 Rex Dieter <rdieter@fedoraproject.org> 0.8.3-4
- /usr/bin/pinentry should not check if stderr is opened (#787775)

* Sat Jul 19 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.8.3-3
- .spec cleanup (drop support for old releases)
- -gtk: Provides: pinentry-gtk2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.3-1
- Update to latest upstream version (0.8.3)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-9
- Fix macros expansions so that conditionals work

* Mon Nov 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-8
- Fix up licenses for qt and qt4 subpackages (#875875)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.8.1-5
- Rebuild for new libpng

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-4
- Improve wrapper to fallback to curses even with DISPLAY set (#622077)

* Fri Feb 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-3
- Fix pinentry-curses running as root by disabling capabilities (#677670)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.1-1
- Updated to latest upstream version (0.8.1)

* Fri May  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.0-3
- Fix X11 even race with gtk (#589998)
- Fix qt4 problems with creating window in the background (#589532)

* Thu Apr 29 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- -qt: build as qt4 version, and drop qt3 support (f13+ only)

* Tue Apr 27 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.8.0-1
- pinentry-0.8.0
- pinentry-gtk keyboard grab fail results in SIGABRT (#585422)

* Sun Apr 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-5
- pinentry-gtk -g segfaults on focus change (#520236)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-4
- Errors installing with --excludedocs (#515925)

* Sun Sep 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-3
- drop alternatives, use app-wrapper instead (borrowed from opensuse)
- -qt4 experimental subpkg, -qt includes qt3 version again  (#523488)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-1
- pinentry-0.7.6
- -qt switched qt4 version, where applicable (f9+, rhel6+)
- fixup scriptlets

* Sat Apr 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.5-1
- pinentry-0.7.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-5
- pinentry failed massrebuild attempt for GCC 4.3 (#434400)

* Tue Mar 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.4-4
- s/qt-devel/qt3-devel/ (f9+)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.4-3
- Autorebuild for GCC 4.3

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> - 0.7.4-2
- rebuild against new libcap

* Sun Dec 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.4-1
- pinentry-0.7.4
- BR: libcap-devel

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-2
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.3-1
- pinentry-0.7.3
- License: GPLv2+

* Thu May 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.7.2-15
- respin (for ppc64)

* Mon Dec 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-14
- -14 respin (to help retire ATrpms pinentry pkg)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-3
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.7.2-2
- fc6 respin

* Wed Mar 01 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Oct 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.2-1
- 0.7.2, docs patch applied upstream.
- Switch to GTK2 in -gtk.
- Fine tune dependencies.
- Build with dependency tracking disabled.
- Clean up obsolete pre-FC2 support.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.7.1-4
- rebuilt

* Wed Jun 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.3
- BuildRequires qt-devel >= 3.2.

* Sat May 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.2
- Spec cleanups.

* Sat Apr 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.1-0.fdr.1
- Update to 0.7.1.

* Fri Dec 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Split GTK+ and QT dialogs into subpackages.

* Thu Jul 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.9-0.fdr.1
- Update to 0.6.9.
- Smoother experience with --excludedocs.
- Don't change alternative priorities on upgrade.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.8-0.fdr.1
- Update to current Fedora guidelines.

* Wed Feb 12 2003 Warren Togami <warren@togami.com> 0.6.8-1.fedora.3
- info/dir temporary workaround

* Sat Feb  8 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.6.8-1.fedora.1
- First Fedora release.
