Name:           perl-AnyEvent-XMPP
Version:	0.55
Release:	4%{?dist}
Summary:        Implementation of the XMPP Protocol
Summary(zh_CN.UTF-8): XMPP 协议的实现
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/AnyEvent-XMPP/
Source0:        http://www.cpan.org/authors/id/M/MS/MSTPLBG/AnyEvent-XMPP-%{version}.tar.gz
Patch0:         AnyEvent-XMPP-0.51-timezone.patch
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(AnyEvent)
BuildRequires:  perl(AnyEvent::Handle)
BuildRequires:  perl(AnyEvent::Socket)
BuildRequires:  perl(Authen::SASL)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Net::LibIDN)
BuildRequires:  perl(Object::Event)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(XML::Parser::Expat)
BuildRequires:  perl(XML::Writer)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
AnyEvent::XMPP - An implementation of the XMPP Protocol.

%description -l zh_CN.UTF-8
XMPP 协议的实现。

%prep
%setup -q -n AnyEvent-XMPP-%{version}
%patch0 -p1 -b .timezone
for file in samples/*; do
    sed -i 's/#!.*perl/\/usr\/bin\/perl/' ${file}
    chmod a-x ${file}
done

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh


%check


%files
%doc Changes CONTRIBUTORS README TODO samples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.55-4
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.55-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.55-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.55-1
- 更新到 0.55

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.52-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.52-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.52-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.52-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.52-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.52-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.52-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.52-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.52-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.52-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.52-3
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 0.52-2
- 为 Magic 3.0 重建

* Tue Jan 24 2012 Petr Šabata <contyk@redhat.com> - 0.52-1
- 0.52 bump
- Spec cleanup, remove useless Requires filters
- Adding samples to doc (and thus adding default_filter to avoid redundant
  dependency generation, rpm #783442)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.51-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.51-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.51-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.51-2
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Allisson Azevedo <allisson@gmail.com> - 0.51-1
- Update to 0.51

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.4-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Allisson Azevedo <allisson@gmail.com> 0.4-1
- Initial rpm release.
