Name:           perl-Fedora-Bugzilla
Version:        0.13
Release:        11%{?dist}
Summary:        Access Fedora's Bugzilla

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://camelus.fedorahosted.org
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSRCHBOY/Fedora-Bugzilla-%{version}.tar.gz
Patch0:         perl-Fedora-Bugzilla-0.13-no-CascadeClear.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)

BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(Crypt::SSLeay)
BuildRequires:  perl(DateTime::Format::Pg)
BuildRequires:  perl(Email::Address)
BuildRequires:  perl(HTTP::Cookies)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(RPC::XML::Client)
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::AttributeHelpers)
BuildRequires:  perl(MooseX::MultiInitArg)
BuildRequires:  perl(MooseX::StrictConstructor)
BuildRequires:  perl(MooseX::CascadeClearing)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(MooseX::Types::DateTime)
BuildRequires:  perl(MooseX::Types::Path::Class)
BuildRequires:  perl(MooseX::Types::URI)
BuildRequires:  perl(Regexp::Common)
BuildRequires:  perl(URI::Fetch)
BuildRequires:  perl(URI::Find)
BuildRequires:  perl(XML::Twig)

# We don't actually use CPAN, but it will error out if it isn't present.
BuildRequires:  perl(CPAN)

# tests
BuildRequires:  perl(MooseX::Types::DateTimeX)
BuildRequires:  perl(Test::More)

# not automagically picked up atm (grrr)
Requires:       perl(Crypt::SSLeay)
Requires:       perl(MooseX::MultiInitArg)
Requires:       perl(RPC::XML::Client)

%description
The XML-RPC interface to bugzilla is quite useful, and while Bugzilla 3.x 
is starting to flesh their interface out a bit more (see, e.g.,
L<WWW::Bugzilla3>), Fedora's Bugzilla implementation has a large number of
custom methods.  This module aims to expose them, in a kinder, gentler way.

In addition to the XML-RPC methods Bugzilla makes available, there are also
some things we only seem to be able to access via the web/XML interfaces.
(See, e.g., the flags, attachments and comments functionality.)  This package
works to expose those as well.


%prep
%setup -q -n Fedora-Bugzilla-%{version}
%patch0 -p1 -b .no-CascadeClear

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*


%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README Changes TODO COPYING
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-10
- 为 Magic 3.0 重建

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.13-9
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.13-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-6
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 16 2010 Petr Pisar <ppisar@redhat.com> - 0.13-5
- Add perl(RPC::XML::Client) requires (related to bug #529172)
- Add perl(MooseX::Types::DateTimeX) build requires because of tests
  (bug #600026)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-2
- drop hardcoded requires on MooseX::Traits::Attribute::CascadeClear

* Fri Jan 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-1
- update to 0.13, change BR from MooseX::Traits::Attribute::CascadeClear to MooseX::CascadeClearing

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.10-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- update to 0.10
- alter source0 to point to the CPAN

* Sun Mar 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08

* Tue Feb 24 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05

* Thu Feb 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- add an explicit requires on perl(MooseX::MultiInitArg)

* Wed Jan 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- update to 0.04
- update source0 to URL

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- bump release for submission (prereq for reviewtool)

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03-0.1
- update to 0.03

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- update to 0.02
- add requires on Crypt::SSLeay

* Mon Jan 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-0.2
- add requires on perl(MooseX::Traits::Attribute::CascadeClear) 

* Sat Jan 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-0.1
- initial packaging
