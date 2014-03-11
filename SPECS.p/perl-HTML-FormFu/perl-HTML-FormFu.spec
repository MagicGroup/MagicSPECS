Name:           perl-HTML-FormFu
Version:        0.09005
Release:        4%{?dist}
Summary:        HTML Form Creation, Rendering and Validation Framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/HTML-FormFu/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PERLER/HTML-FormFu-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Captcha::reCAPTCHA) >= 0.93
BuildRequires:  perl(CGI) >= 3.37
BuildRequires:  perl(CGI::Simple)
BuildRequires:  perl(Class::Accessor::Chained::Fast)
BuildRequires:  perl(Class::MOP::Method)
BuildRequires:  perl(Clone)
BuildRequires:  perl(Config::Any) >= 0.18
BuildRequires:  perl(Crypt::CBC)
BuildRequires:  perl(Crypt::DES)
BuildRequires:  perl(Data::Visitor) >= 0.26
BuildRequires:  perl(Date::Calc)
BuildRequires:  perl(DateTime) >= 0.38
BuildRequires:  perl(DateTime::Format::Builder) >= 0.80
BuildRequires:  perl(DateTime::Format::Natural)
BuildRequires:  perl(DateTime::Format::Strptime) >= 1.2000
BuildRequires:  perl(DateTime::Locale) >= 0.45
BuildRequires:  perl(Email::Valid)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(Hash::Flatten)
BuildRequires:  perl(HTML::Scrubber)
BuildRequires:  perl(HTML::TokeParser::Simple) >= 3.14
BuildRequires:  perl(HTTP::Headers) >= 1.64
BuildRequires:  perl(IO::File)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Locale::Maketext)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(Moose) >= 1.00
BuildRequires:  perl(Moose::Meta::Attribute::Custom::Trait::Chained)
BuildRequires:  perl(MooseX::Aliases)
BuildRequires:  perl(MooseX::ChainedAccessors::Accessor) >= 0.02
BuildRequires:  perl(MooseX::SetOnce)
BuildRequires:  perl(Number::Format)
BuildRequires:  perl(Path::Class::File)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Regexp::Common)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test::Aggregate::Nested)
BuildRequires:  perl(Test::More) >= 0.92
BuildRequires:  perl(YAML::XS) >= 0.32
Requires:       perl(Captcha::reCAPTCHA) >= 0.93
Requires:       perl(Class::Accessor::Chained::Fast)
Requires:       perl(Config::Any) >= 0.18
Requires:       perl(Crypt::DES)
Requires:       perl(Data::Visitor) >= 0.26
Requires:       perl(Date::Calc)
Requires:       perl(DateTime) >= 0.38
Requires:       perl(DateTime::Format::Builder) >= 0.80
Requires:       perl(HTML::TokeParser::Simple) >= 3.14
Requires:       perl(HTTP::Headers) >= 1.64
Requires:       perl(Moose::Meta::Attribute::Custom::Trait::Chained)
Requires:       perl(MooseX::ChainedAccessors::Accessor) >= 0.02
Requires:       perl(Template)
Requires:       perl(YAML::XS) >= 0.32
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter:
%filter_from_provides /perl(unicode/d
%filter_from_requires /perl(Catalyst/d; /perl(default/d; /perl(model_config)/d;
%perl_default_filter
}

%description
HTML::FormFu is a HTML form framework which aims to be as easy as possible
to use for basic web forms, but with the power and flexibility to do
anything else you might want to do (as long as it involves forms).

%prep
%setup -q -n HTML-FormFu-%{version}

find examples -type f | xargs chmod 644
find examples -type f | xargs sed -i -e 's/\r//'


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

rm -rf $RPM_BUILD_ROOT/blib

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README examples
%{perl_vendorlib}/*
%{_bindir}/*.pl
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09005-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.09005-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 0.09005-1
- update to latest upstream version

* Sun Aug 28 2011 Iain Arnell <iarnell@gmail.com> 0.09004-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.09003-2
- Perl mass rebuild

* Thu May 12 2011 Iain Arnell <iarnell@gmail.com> 0.09003-1
- update to latest upstream version

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.09002-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 25 2010 Iain Arnell <iarnell@gmail.com> 0.08002-1
- update to latest upstream
- clean up spec for modern rpmbuild

* Tue Sep 07 2010 Iain Arnell <iarnell@gmail.com> 0.07003-1
- update to latest upstream version
- bump Captcha::reCAPTCHA requirement to 0.93

* Fri Jun 25 2010 Iain Arnell <iarnell@gmail.com> 0.07002-1
- update to latest upstream
- bump DateTime::Format::Strptime and DateTime::Locale BRs

* Fri Jun 18 2010 Iain Arnell <iarnell@gmail.com> 0.07001-3
- bump for build against perl-5.12

* Fri Jun 18 2010 Iain Arnell <iarnell@gmail.com> 0.07001-2
- doesn't BR perl(Regexp::Copy) any more

* Mon May 17 2010 Iain Arnell <iarnell@gmail.com> 0.07001-1
- update to latest upstream version
- re-enable tests
- tweak buildrequires

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06001-2
- Mass rebuild with perl-5.12.0

* Mon Jan 11 2010 Iain Arnell <iarnell@gmail.com> 0.06001-1
- update to latest upstream version
- update requires

* Fri Dec 18 2009 Iain Arnell <iarnell@gmail.com> 0.05004-2
- fix silly typo in requires filtering

* Tue Dec 08 2009 Iain Arnell <iarnell@gmail.com> 0.05004-1
- update to latest upstream version
- use perl_default_filter

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05001-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 Iain Arnell <iarnell@gmail.com> 0.05001-1
- update to latest upstream version

* Wed May 27 2009 Iain Arnell <iarnell@gmail.com> 0.05000-1
- update to latest upstream
- R/BR Data::Visitor >= 0.23 to avoid Squirrel warnings

* Sun May 10 2009 Iain Arnell <iarnell@gmail.com> 0.04002-1
- update to latest upstream version

* Wed Apr 15 2009 Iain Arnell <iarnell@gmail.com> 0.04001-1
- update to latest upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 08 2008 Iain Arnell <iarnell@gmail.com> 0.03007-1
- update to 030007

* Sat Dec 06 2008 Iain Arnell <iarnell@gmail.com> 0.03005-4
- remove wrongly detected requires (defaults and model_config)

* Sat Nov 29 2008 Iain Arnell <iarnell@gmail.com> 0.03005-3
- remove more unnecessary requires
- requires Exporter >= 5.57

* Sat Nov 29 2008 Iain Arnell <iarnell@gmail.com> 0.03005-2
- remove unnecessary explicit requires

* Wed Nov 26 2008 Iain Arnell <iarnell@gmail.com> 0.03005-1
- Specfile autogenerated by cpanspec 1.77.
