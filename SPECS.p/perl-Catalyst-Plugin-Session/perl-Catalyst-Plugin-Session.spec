Name:           perl-Catalyst-Plugin-Session
Summary:        Catalyst generic session plugin
Version:        0.32
Release:        5%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Catalyst-Plugin-Session-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Catalyst-Plugin-Session/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Runtime) >= 5.71001
BuildRequires:  perl(Digest)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Moose) >= 0.76
BuildRequires:  perl(MooseX::Emulate::Class::Accessor::Fast) >= 0.00801
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(namespace::clean) >= 0.10
BuildRequires:  perl(Object::Signature)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Tie::RefHash) >= 1.34
%if !0%{?perl_bootstrap}
# these cause circular builddeps
BuildRequires:  perl(Catalyst::Plugin::Session::State::Cookie) >= 0.03
BuildRequires:  perl(Test::WWW::Mechanize::Catalyst) >= 0.51
%endif

Requires:       perl(Catalyst::Runtime) >= 5.71001
Requires:       perl(MooseX::Emulate::Class::Accessor::Fast) >= 0.00801

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.32-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This plugin is the base of two related parts of functionality
required for session management in web applications.

The first part, the State, is getting the browser to repeat back a
session key, so that the web application can identify the client and
logically string several requests together into a session.

The second part, the Store, deals with the actual storage of information
about the client. This data is stored so that the it may be revived for
every request made by the same client.

This plugin links the two pieces together.

%prep
%setup -q -n Catalyst-Plugin-Session-%{version}

# test fails - see https://rt.cpan.org/Public/Bug/Display.html?id=71142
rm t/live_verify_address.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.32-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.32-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.32-3
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.32-2
- drop tests subpackage; move tests to main package documentation

* Fri Jan 20 2012 Iain Arnell <iarnell@gmail.com> 0.32-1
- update to latest upstream version
- remove unnecessary explicit dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.31-4
- Perl mass rebuild

* Fri Jul 15 2011 Iain Arnell <iarnell@gmail.com> 0.31-3
- restore circular deps and wrap with perl_bootstrap macro

* Wed Jul 13 2011 Iain Arnell <iarnell@gmail.com> 0.31-2
- drop additional BRs again - they cause circular build deps

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.31-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- BR Catalyst::Plugin::Session::State::Cookie and
  Test::WWW::Mechanize::Catalyst for improved test coverage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-4
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.29-3
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Catalyst)
- dropped old BR on perl(Test::Pod::Coverage)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.29-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- auto-update to 0.29 (by cpan-spec-update 0.01)

* Sat Oct 10 2009 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to 0.27
- remove buildreq on perl(Text::MockObject)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-1
- switch to new filtering system (perl_default_filter)
- auto-update to 0.25 (by cpan-spec-update 0.01)
- added a new req on perl(Catalyst::Runtime) (version 5.71001)
- added a new req on perl(Digest) (version 0)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(File::Temp) (version 0)
- added a new req on perl(MRO::Compat) (version 0)
- added a new req on perl(Moose) (version 0.76)
- altered req on perl(MooseX::Emulate::Class::Accessor::Fast) (0 => 0.00801)
- added a new req on perl(Object::Signature) (version 0)
- added a new req on perl(Tie::RefHash) (version 1.34)
- added a new req on perl(namespace::clean) (version 0.10)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Iain Arnell <iarnell@gmail.com> 0.22-2
- add missing requires perl(MooseX::Emulate::Class::Accessor::Fast)

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- auto-update to 0.22 (by cpan-spec-update 0.01)
- added a new br on perl(File::Temp) (version 0)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(namespace::clean) (version 0.10)
- added a new br on perl(Moose) (version 0.76)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Catalyst::Runtime) (version 5.71001)
- added a new br on perl(MooseX::Emulate::Class::Accessor::Fast) (version 0.00801)

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- update to 0.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.19-2
- bump

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- Specfile autogenerated by cpanspec 1.74.
