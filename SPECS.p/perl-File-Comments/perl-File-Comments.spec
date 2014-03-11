# Need to tweak provides filter differently if we have rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+)\\.(\\d+).*/sprintf("%d.%03d%03d",$1,$2,$3) ge 4.009 ? 1 : 0/e')

Summary:	Recognizes file formats and extracts format-specific comments
Name:		perl-File-Comments
Version:	0.08
Release:	7%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/File-Comments/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MS/MSCHILLI/File-Comments-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Archive::Tar) >= 1.22
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(HTML::TokeParser) >= 2.28
BuildRequires:	perl(HTML::TreeBuilder)
BuildRequires:	perl(Log::Log4perl) >= 0.50
BuildRequires:	perl(Module::Pluggable) >= 2.4
BuildRequires:	perl(Pod::Parser) >= 1.14
BuildRequires:	perl(PPI) >= 1.115
BuildRequires:	perl(Sysadm::Install) >= 0.11
# For test suite
BuildRequires:	perl(Test::More)
# Runtime requirements not automatically picked up
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(HTML::TreeBuilder)
Requires:	perl(Module::Pluggable) >= 2.4
Requires:	perl(Pod::Parser) >= 1.14
Requires:	perl(PPI) >= 1.115

%description
File::Comments guesses the type of a given file, determines the format
used for comments, extracts all comments, and returns them as a
reference to an array of chunks. Alternatively, it strips all comments
from a file.

Currently supported are Perl scripts, C/C++ programs, Java, makefiles,
JavaScript, Python and PHP.

%prep
%setup -q -n File-Comments-%{version}

# Note: not turning off exec bits in examples because they don't
# introduce any unwanted dependencies (nor any dependencies that
# are not satisfied by packages that are already required)

# Remove provide for local package not in regular search path
%if %{rpm49}
%global __provides_exclude ^perl\\(PodExtractor\\)
%else
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Fvx 'perl(PodExtractor)'"
%define __perl_provides %{provfilt}
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
 TEST_VERBOSE=1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README eg
%{perl_vendorlib}/File/
%{_mandir}/man3/File::Comments.3pm*
%{_mandir}/man3/File::Comments::Plugin.3pm*
%{_mandir}/man3/File::Comments::Plugin::C.3pm*
%{_mandir}/man3/File::Comments::Plugin::HTML.3pm*
%{_mandir}/man3/File::Comments::Plugin::Java.3pm*
%{_mandir}/man3/File::Comments::Plugin::JavaScript.3pm*
%{_mandir}/man3/File::Comments::Plugin::Makefile.3pm*
%{_mandir}/man3/File::Comments::Plugin::PHP.3pm*
%{_mandir}/man3/File::Comments::Plugin::Perl.3pm*
%{_mandir}/man3/File::Comments::Plugin::Python.3pm*
%{_mandir}/man3/File::Comments::Plugin::Shell.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.08-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.08-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.08-5
- Spec clean-up:
  - Nobody else likes macros for commands
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Update provides filter to work with rpm ≥ 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.08-4
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Dec 10 2010 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08
  - Adapt to HTML::Element >=4 change that omits trailing newline in generated
    HTML (CPAN RT#63788)
- Resolves FTBFS issue in Rawhide (#661088)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-7
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.07-5
- Rebuild against perl 5.10.1

* Fri Sep 18 2009 Paul Howarth <paul@city-fan.org> 0.07-4
- Add runtime dependencies not determined automatically by RPM

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  9 2008 Paul Howarth <paul@city-fan.org> 0.07-1
- Initial RPM version
