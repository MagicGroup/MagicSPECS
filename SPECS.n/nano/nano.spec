Summary:         A small text editor
Name:            nano
Version:         2.3.2
Release:         2%{?dist}
License:         GPLv3+
Group:           Applications/Editors
URL:             http://www.nano-editor.org
Source:          http://www.nano-editor.org/dist/v2.3/%{name}-%{version}.tar.gz
Source2:         nanorc
Patch0:          nano-2.3.2-warnings.patch

# http://lists.gnu.org/archive/html/nano-devel/2010-08/msg00004.html
Patch1:          0001-check-stat-s-result-and-avoid-calling-stat-on-a-NULL.patch

# http://lists.gnu.org/archive/html/nano-devel/2010-08/msg00005.html
Patch2:          0002-use-futimens-if-available-instead-of-utime.patch

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:   autoconf
BuildRequires:   file-devel
BuildRequires:   gettext-devel
BuildRequires:   groff
BuildRequires:   ncurses-devel
BuildRequires:   sed
Conflicts:       filesystem < 3
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
GNU nano is a small and friendly text editor.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

for f in doc/man/fr/{nano.1,nanorc.5,rnano.1} ; do
  iconv -f iso-8859-1 -t utf-8 -o $f.tmp $f && mv $f.tmp $f
  touch $f.html
done

# do not run autotools, we have already reflected the configure.ac
# changes in configure and config.h.in
touch -c aclocal.m4 config.h.in configure Makefile.in

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" install
#ln -s nano %{buildroot}%{_bindir}/pico
rm -f %{buildroot}%{_infodir}/dir
cp %{SOURCE2} ./nanorc

# disable line wrapping by default and set hunspell as the default spell-checker
sed -e 's/# set nowrap/set nowrap/' \
    -e 's/^#.*set speller.*$/set speller "hunspell"/' \
    doc/nanorc.sample >> ./nanorc
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 ./nanorc %{buildroot}%{_sysconfdir}/nanorc

%find_lang %{name}

%post
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi
exit 0

%preun
if [ $1 -eq 0 ]; then
  if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
  fi
fi
exit 0

%files -f %{name}.lang
%doc AUTHORS BUGS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc doc/nanorc.sample
%doc doc/faq.html
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nanorc
%{_mandir}/man*/*
%lang(fr) %{_mandir}/fr/man*/*
%{_infodir}/nano.info*
%{_datadir}/nano

%changelog
* Wed Mar 27 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-2
- add "BuildRequires: file-devel" to build libmagic support (#927994)

* Tue Mar 26 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 2.3.1-5
- fix specfile issues reported by the fedora-review script

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.3.1-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.1-1
- new upstream release

* Thu Mar 03 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.0-1
- new upstream release (#680736)
- use hunspell as default spell-checker (#681000)
- fix for http://thread.gmane.org/gmane.editors.nano.devel/2911

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-2
- fix bugs introduced by patches added in 2.2.6-1 (#657875)

* Mon Nov 22 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-1
- new upstream release (#655978)
- increase code robustness (patches related to CVE-2010-1160, CVE-2010-1161)

* Sat Aug 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.5-1
- new upstream release (#621857)

* Thu Apr 15 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.4-1
- new upstream release
- CVE-2010-1160, CVE-2010-1161 (#582739)

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.3-1
- new upstream release

* Fri Jan 29 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.2-1
- new upstream release

* Sun Dec 27 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.1-1
- new upstream release

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.0-1
- new upstream release

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-7
- sanitize specfile according to Fedora Packaging Guidelines 

* Thu Oct 15 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-6
- use nanorc.sample as base of /etc/nanorc

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-5
- fix build failure of the last build

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-4
- ship a system-wide configuration file along with the nano package
- disable line wrapping by default (#528359)

* Mon Sep 21 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-3
- suppress warnings for __attribute__((warn_unused_result)) (#523951)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-2
- install binaries to /bin (#168340)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-1
- new upstream release
- dropped patch no longer needed (possible change in behavior though negligible)
- fixed broken HTML doc in FR locales (#523951)

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.6-8
- do process install-info only without --excludedocs(#515943)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.0.6-5
- Mark localized man pages with %%lang, fix French nanorc(5) (#322271).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.6-4
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.6-3
- Pass rnano.1 through iconv to silence the final rpmlint complaint
  and finish up the merge review.

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.6-2
- Update licence
- Fix open(O_CREAT) calls without mode

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 2.0.6-1
- update to 2.0.6

* Mon Feb 05 2007 Florian La Roche <laroche@redhat.com> - 2.0.3-1
- update to 2.0.3
- update spec file syntax, fix scripts rh#220527

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.12-1.1
- rebuild

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.12-1
- Update to 1.3.12

* Tue May 16 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.11-1
- Update to 1.3.11
- BuildRequires: groff (#191946)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 5 2005 David Woodhouse <dwmw2@redhat.com> 1.3.8-1
- 1.3.8

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.3.5-0.20050302
- Update to post-1.3.5 CVS tree to get UTF-8 support.

* Wed Aug 04 2004 David Woodhouse <dwmw2@redhat.com> 1.2.4-1
- 1.2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.2.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 11 2003 Bill Nottingham <notting@redhat.com> 1.2.1-4
- build in different environment

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Bill Nottingham <notting@redhat.com> 1.2.1-2
- description tweaks

* Mon May  5 2003 Bill Nottingham <notting@redhat.com> 1.2.1-1
- initial build, tweak upstream spec file
