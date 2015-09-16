Name:           perl-bioperl
Version:	1.6.924
Release:	4%{?dist}
Summary:        Perl tools for computational molecular biology
Summary(zh_CN.UTF-8): 用于计算分子生物学的 Perl 工具

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://www.bioperl.org/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CJ/CJFIELDS/BioPerl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Ace)
BuildRequires:  perl(Class::AutoClass) >= 1
BuildRequires:  perl(Clone)
BuildRequires:  perl(Convert::Binary::C)
BuildRequires:  perl(Data::Stag::XMLWriter)
BuildRequires:  perl(DBD::mysql)
BuildRequires:  perl(DBD::Pg)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(GD) >= 1.3
BuildRequires:  perl(GD::SVG)
BuildRequires:  perl(Graph)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(IO::Stringy)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(PostScript::TextBlock)
BuildRequires:  perl(Set::Scalar)
BuildRequires:  perl(SOAP::Lite)
BuildRequires:  perl(Spreadsheet::ParseExcel)
BuildRequires:  perl(Storable)
BuildRequires:  perl(SVG) >= 2.26
BuildRequires:  perl(SVG::Graph) >= 0.01
BuildRequires:  perl(Text::Shellwords)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(XML::DOM::XPath) >= 0.13
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(XML::Parser::PerlSAX)
BuildRequires:  perl(XML::SAX) >= 0.14
BuildRequires:  perl(XML::SAX::Writer)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(XML::Twig)
BuildRequires:  perl(XML::Writer) > 0.4
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Array::Compare)
BuildRequires:  perl(GraphViz)
# disable the following BRs until they are packaged for Fedora
#BuildRequires:	perl(Math::Random)
#BuildRequires:	perl(Algorithm::Munkres)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Filter unwanted dependency
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(Bio::Expression::FeatureSet\\)

# Packages perl-bioperl and perl-bioperl-run require each other.  To break
# this circular edependency (e.g., for bootstrapping), filter out all
# Bio::Tools::Run::* module requirements; they are either self-satisfied
# (and thus redundant) or they bring dependency on perl-bioperl-run.
%if %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Bio::Tools::Run::
%endif

%description
BioPerl is a toolkit of Perl modules useful in building bioinformatics
solutions in Perl. It is built in an object-oriented manner so that
many modules depend on each other to achieve a task.

%description -l zh_CN.UTF-8
用于计算分子生物学的 Perl 工具。

%prep
%setup -q -n BioPerl-%{version}

# temporarily remove PhyloNetwork before compiling until upstream says
# they are ready for primetime and deps Math::Random and
# Algorithm::Munkres are also packaged
rm -r Bio/PhyloNetwork*
rm -r t/Tree/PhyloNetwork

# remove all execute bits from the doc stuff
find examples -type f -exec chmod -x {} ';'

%build
%{__perl} Build.PL --installdirs vendor << EOF
n
a
n
EOF

./Build

# make sure the man page is UTF-8...
cd blib/libdoc
for i in Bio::Tools::GuessSeqFormat.3pm Bio::Tools::Geneid.3pm; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > new
    mv new $i
done


%install
rm -rf $RPM_BUILD_ROOT
#make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
perl Build pure_install --destdir=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
# remove errant execute bit from the .pm's
find $RPM_BUILD_ROOT -type f -name '*.pm' -exec chmod -x {} 2>/dev/null ';'
# correct all binaries in /usr/bin to be 0755
# find $RPM_BUILD_ROOT/%{_bindir} -type f -name '*.pl' -exec chmod 0755 {} 2>/dev/null ';'
magic_rpm_clean.sh

%check
%{?_with_check:./Build test || :}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
## don't distribute "doc" subdirectory,  doesn't contain docs
%doc examples models 
%doc AUTHORS BUGS Changes DEPRECATED INSTALL LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*    

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.6.924-4
- 为 Magic 3.0 重建

* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 1.6.924-3
- 为 Magic 3.0 重建

* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 1.6.924-2
- 为 Magic 3.0 重建

* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 1.6.924-1
- 更新到 1.6.924

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-30
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-29
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-28
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.6.1-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.6.1-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.6.1-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.6.1-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.6.1-16
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.6.1-14
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jul 04 2012 Petr Pisar <ppisar@redhat.com> - 1.6.1-13
- Perl 5.16 rebuild

* Tue Jul 03 2012 Petr Pisar <ppisar@redhat.com> - 1.6.1-12
- Perl 5.16 rebuild
- Break cycle on bootstrapping perl

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 1.6.1-10
- RPM 4.9 dependency filtering added

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.6.1-9
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.6.1-8
- Perl mass rebuild

* Tue Feb 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.1-7
- fix filter for RPM4.9

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.1-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.1-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-3
- rebuild against perl 5.10.1

* Thu Nov 12 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-2
- use the new filtering macros (cf #537138)

* Wed Nov  4 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.6.1-1
- Update to latest upstream 1.6.1
- Add BR: perl(XML::Simple), perl(DBD:SQLite) for new modules
- Disable ExtUtils::Manifest build requirement, don't require a MANIFEST
- Fix doc distributed

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.6.0-1
- Update to 1.6.0 final release

* Thu Jan 22 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.5.4
- Update to 1.6.0 release candidate 4

* Sun Jan 18 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.4.3
- Update to 1.6.0 release candidate 3

* Wed Jan  7 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.3.2
- Update to 1.6.0 release candidate 2
- Remove filter for Bio::Graphics*, upstream removed them from the
  tarball

* Sun Dec 28 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.2.1
- Filter unwanted Requires: Bio::Graphics and Bio::Graphics::Panel
  fixes broken deps until the .pl demo scripts remove them to the
  appropriate module

* Fri Dec 26 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.1.1
- Update to latest upstream, 1.5.9, which is release candidate 1 for 1.6.0
- Add BuildRequires for perl(Array::Compare) and perl(GraphViz).
- Fix patch to apply to new release.
- Remove Bio::PhyloNetwork from installation, currently has unfilled
  deps and not ready for primetime according to upstream.

* Thu Sep 25 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.2_102-13
- Fix patch fuzz

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-12
- bootstrapping done, building normally

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11.2
- missed one

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11.1
- actually disable bioperl-run requires for bootstrapping

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11
- disable bioperl-run requires for bootstrapping

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-10
- rebuild for new perl

* Mon Oct 15 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-9
- Add missing BR: perl(Test::More)
- Clarified license terms: GPL+ or Artistic

* Thu May 07 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-8
- Spec file cleanups.
- Improve description.

* Thu Apr 19 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-7
- Fix 'perl Build' command so that it does not attempt CPAN downloads.

* Thu Apr 19 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-6
- Enable scripts, now that bioperl-run is in the repository.

* Tue Apr 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-5
- Fix changelog

* Tue Apr 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-4
- Disable tests because many of them require network access, add
  _with_check macro so they can be enabled during testing.

* Mon Apr 02 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-3
- Remove BuildRequires: perl(Bio::ASN1::EntrezGene), creates a
  circular dependency, the dependency is still found at install-time.

* Thu Mar 29 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-2
- Add all BRs listed as 'recommends' in Build.PL so that it never
  needs to get packages from CPAN.
- Remove unnecessary filtering of Requires

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-1
- Update to 1.5.2_102
- Review suggestions from Steven Pritchard
- BR: perl(IO::String)
- Disable scripts for now as they require bioperl-run (not yet packaged)
- Don't mark non-documentation files as documentation.

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 1.5.0-3
- Review suggestions from José Pedro Oliveira

* Mon Apr 01 2005 Hunter Matthews <thm@duke.edu> 1.5.0-2
- Added buildrequires and improved documention entries from FE mailing list.

* Mon Mar 21 2005 Hunter Matthews <thm@duke.edu> 1.5.0-1
- Initial build. I started with the biolinux.org rpm, but broke out 
  most of the deps and built them seperately.
