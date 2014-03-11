Name:           perl-Catalyst-Engine-PSGI
Summary:        PSGI engine for Catalyst
Version:        0.13
Release:        8%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/Catalyst-Engine-PSGI-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Catalyst-Engine-PSGI
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Action::RenderView)
BuildRequires:  perl(Catalyst::Runtime) >= 5.80007
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(URI)

#Tests dependencies:
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Catalyst)
BuildRequires:  perl(Catalyst::Request)                                                                                                                      
BuildRequires:  perl(Catalyst::Request::Upload)                                                                                                              
BuildRequires:  perl(Catalyst::Restarter)                                                                                                                    
BuildRequires:  perl(Catalyst::Utils)                                                                                                                        
BuildRequires:  perl(CGI::Simple::Cookie)                                                                                                                    
BuildRequires:  perl(Data::Dumper)                                                                                                                           
BuildRequires:  perl(FindBin)                                                                                                                                
BuildRequires:  perl(Getopt::Long)                                                                                                                           
BuildRequires:  perl(HTML::Entities)                                                                                                                         
BuildRequires:  perl(HTTP::Body::OctetStream)                                                                                                                
BuildRequires:  perl(HTTP::Headers)                                                                                                                          
BuildRequires:  perl(HTTP::Headers::Util)                                                                                                                    
BuildRequires:  perl(HTTP::Request::Common)                                                                                                                  
BuildRequires:  perl(lib)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Moose::Role)
#BuildRequires:  perl(Moose::Utils)
BuildRequires:  perl(MooseX::MethodAttributes)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(Path::Class::Dir)
BuildRequires:  perl(Plack::Loader)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(YAML)

Requires:       perl(Catalyst::Action::RenderView)
Requires:       perl(Catalyst::Runtime) >= 5.80007
Requires:       perl(Filter::Util::Call)

%{?perl_default_filter}

%description
Catalyst::Engine::PSGI is a Catalyst Engine that adapts Catalyst into the PSGI
gateway protocol.

%prep
%setup -q -n Catalyst-Engine-PSGI-%{version}

rm -rf inc/Test

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-5
- 为 Magic 3.0 重建

* Mon Jan 16 2012 Marcela Mašláňová <mmaslano@redhat.com> 0.13-4
- remove Catalyst::Engine::HTTP which is obsoleted in new versions of Catalyst

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.13-2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.13-1
- update to 0.13

* Tue Jan 11 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.12-1
- update to 0.12

* Mon Nov 15 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.11-1
- specfile by Fedora::App::MaintainerTools 0.006


