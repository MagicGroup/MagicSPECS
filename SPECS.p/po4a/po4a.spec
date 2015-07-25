%define num 4134
Name: po4a
Version:	0.46
Release:	1%{?dist}
Summary: A tool maintaining translations anywhere
Summary(zh_CN.UTF-8): 在任何地方处理翻译的工具
License: GPL+
URL: http://alioth.debian.org/projects/po4a/

Source0: http://alioth.debian.org/frs/download.php/%{num}/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: perl(Locale::gettext) >= 1.01
BuildRequires: perl(Module::Build)
BuildRequires: perl(Pod::Parser)
BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(Term::ReadKey)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(Unicode::GCString)
BuildRequires: /usr/bin/xsltproc
BuildRequires: gettext
BuildRequires: docbook-style-xsl

# Requires a pod2man which supports --utf8
# Seemingly added in perl-5.10.1
BuildRequires: perl >= 4:5.10.1

# Required by the tests.
BuildRequires: perl(Test::More)
BuildRequires: /usr/bin/kpsewhich
# Work-around to texlive-kpseas-bin missing deps 
BuildRequires: /usr/share/texlive/texmf-dist/web2c/texmf.cnf

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: gettext

# Optional, used by Locale/Po4a/TeX.pm
# Requires: /usr/bin/kpsewhich
# Optional, used by po4a-build
# Requires: /usr/bin/xsltproc
# Optional, but package is quite useless without
Requires: perl(Locale::gettext) >= 1.01

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%description -l zh_CN.UTF-8
在任何地方处理翻译的工具。

%prep
%setup -q -n %{name}-%{version}

chmod +x scripts/*

# Fix bang path /usr/bin/env perl -> %{_bindir}/perl (RHBZ#987035).
%{__perl} -p -i -e 's,#!\s*/usr/bin/env perl,#!%{_bindir}/perl,' \
  $(find . -type f -executable |
    xargs grep -l "/usr/bin/env perl")

%build
export PO4AFLAGS="-v -v -v"
%{__perl} ./Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh
%find_lang %{name}

%check
./Build test


%files -f %{name}.lang
%doc README* COPYING TODO
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%{_mandir}/man3/Locale::Po4a::*.3*
%{_mandir}/man5/po4a-build.conf*.5*
%{_mandir}/man7/po4a-runtime.7*
%{_mandir}/man7/po4a.7*

%changelog
* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 0.46-1
- 更新到 0.46

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 0.45-2
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.44-11
- Perl 5.18 rebuild

* Tue Jul 30 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.44-10
- Add BR: /usr/share/texlive/texmf-dist/web2c/texmf.cnf.
- Re-enable t/24-tex.t (Cause for breakdown is texlive packing mess).
- Add BR: perl(Unicode::GCString).
- Move shebang fixing into %%build.
- Fix Source0-URL.
- Spec-file cosmetics.

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 0.44-9
- Fix bang path /usr/bin/env perl -> %{_bindir}/perl (RHBZ#987035).
- Increase verbosity of po4a when building to help diagnose build errors.
- +BR Pod::Parser.
- Disable 24-tex.t which does not run and does not produce any
  useful diagnostics either.

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.44-2
- Perl 5.18 rebuild

* Wed Apr 17 2013 Richard W.M. Jones <rjones@redhat.com> - 0.44-1
- New upstream version 0.44.
- Fix incorrect use of File::Temp->tempfile (RHBZ#953066).
- Tidy up the spec file.
- po4a-build.conf.5 and po4a-runtime.7 man pages are no longer
  installed in the English version for some (unknown) reason.

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.42-3
- Add 0001-Remove-defined-anachronism.patch.
- Modernize spec.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.42-1
- Upstream update.

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.41-5
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.41-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.41-1
- Upstream update.
- Reflect upstream having changed to Module::Build.
- Remove po4a-0.40.1.diff.

* Fri Oct 15 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.40.1-1
- Upstream update.
- Add po4a-v0.40.1.diff (add missing file t/compare-po.pl)
- Make testsuite working.
- Spec overhaul.
- Eliminate /usr/bin/env perl.
- Require perl >= 5.10.1

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.35-15
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-14
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.35-11
- Update to 0.35.

* Tue Jan 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.34-10
- Add BuildRequires: perl(Test::More), BuildRequires: docbook-dtds.
- Activate tests.
- Fix Source0:-URL.
- Spec file cosmetics.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.34-9
- Update to 0.34.

* Sun Jun 01 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-8
- Let package own %%{perl_vendorlib}/Locale (BZ 449258).

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-7
- Remove || : in %%check due to rpm not accepting it anymore.

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-6
- Add: "Requires: perl(:MODULE_COMPAT_...)" (BZ 442548).

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-5
- fix license tag

* Mon Aug 20 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.32-4
- Update to 0.32.
- fixes a possible race condition under /tmp (no CVE yet).

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.29-3
- Update to 0.29.

* Sat Feb 18 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

