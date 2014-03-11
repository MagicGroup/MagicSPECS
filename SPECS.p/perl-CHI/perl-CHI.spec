Name:           perl-CHI
Version:        0.50
Release:        4%{?dist}
Summary:        Unified cache handling interface
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CHI/
Source0:        http://www.cpan.org/authors/id/J/JS/JSWARTZ/CHI-%{version}.tar.gz
BuildArch:      noarch

%bcond_without author_tests

%bcond_without smoke_tests

BuildRequires:  perl(Carp::Assert) >= 0.20
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Data::UUID)
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(Digest::JHash)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(Hash::MoreUtils)
BuildRequires:  perl(JSON)
BuildRequires:  perl(List::MoreUtils) >= 0.13
BuildRequires:  perl(Log::Any) >= 0.08
BuildRequires:  perl(Log::Any::Adapter::Dispatch) >= 0.05
BuildRequires:  perl(Module::Load::Conditional)
BuildRequires:  perl(Moose) >= 0.66
BuildRequires:  perl(Storable)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Class)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Log::Dispatch)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Time::Duration) >= 1.06
BuildRequires:  perl(Time::Duration::Parse) >= 0.03
BuildRequires:  perl(Try::Tiny) >= 0.05

%if %{with author_tests}
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Module::Mask)
%endif

%if %{with smoke_tests}
BuildRequires:	perl(Cache::FileCache)
BuildRequires:	perl(Cache::FastMmap)
%endif

%{?perl_filter_default}

# RPM 4.8 style
%{?filter_setup:
%filter_from_provides /^perl(Bar)/d
%filter_from_provides /^perl(Baz)/d
%filter_from_provides /^perl(DummySerializer)/d
%filter_from_provides /^perl(Foo)/d
# Replace unversioned dependencies with versioned ones.
%filter_from_requires s/^perl(Carp::Assert)$/perl(Carp::Assert) >= 0.20/
%filter_from_requires s/^perl(List::MoreUtils)$/perl(List::MoreUtils) >= 0.13/
%filter_from_requires s/^perl(Log::Any)$/perl(Log::Any) >= 0.06/
%filter_from_requires s/^perl(Moose)$/perl(Moose) >= 0.66/
%filter_from_requires s/^perl(Time::Duration)$/perl(Time::Duration) >= 1.06/
%filter_from_requires s/^perl(Time::Duration::Parse)$/perl(Time::Duration::Parse) >= 0.03/
%filter_setup
}
# RPM 4.9 style
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(Bar\\)
%global __provides_exclude %__provides_exclude|^perl\\(DummySerializer\\)
%global __provides_exclude %__provides_exclude|^perl\\(Foo\\)
# Replace unversioned dependencies with versioned ones.
# Already auto-discovered. In addition, RPM 4.9 does not offer replacing.

%description
CHI provides a unified caching API, designed to assist a developer in
persisting data for a specified period of time.

%package Test
Group:          Development/Libraries
Summary:        CHI::Test module
Requires:       perl-CHI = %{version}-%{release}

# rpm misses these:
Requires:       perl(Test::Deep)
Requires:	perl(Test::Exception)

%description Test
CHI::Test and CHI::t perl modules

%prep
%setup -q -n CHI-%{version}
# Fix bogus permissions
find lib \( -type f -a -executable \) -exec chmod -x {} \;

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor --skipdeps
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
 %{?with_author_tests:AUTHOR_TESTING=1} %{?with_smoke_tests:AUTOMATED_TESTING=1}

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%dir %{perl_vendorlib}/CHI
%{perl_vendorlib}/CHI.pm
%{perl_vendorlib}/CHI/Benchmarks.pod
%{perl_vendorlib}/CHI/CacheObject.pm
%{perl_vendorlib}/CHI/Constants.pm
%{perl_vendorlib}/CHI/Driver*
%{perl_vendorlib}/CHI/Serializer
%{perl_vendorlib}/CHI/Stats.pm
%{perl_vendorlib}/CHI/Types.pm
%{perl_vendorlib}/CHI/Util.pm
%{_mandir}/man3/*

%files Test
%defattr(-,root,root,-)
%dir %{perl_vendorlib}/CHI
%{perl_vendorlib}/CHI/t
%{perl_vendorlib}/CHI/Test*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.50-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.50-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.50-2
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.50-1
- Abandon fedora < 15.
- Add BR: perl(Digest::MD5).
- Upstream update.
- Reflect upstream having abandoned htdocs.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 0.44-6
- RPM 4.9 dependency filtering added

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.44-5
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.44-4
- Perl mass rebuild

* Thu Mar 31 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.44-3
- Add R: perl(Test::Deep) and R: perl(Test::Exception).

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.44-2
- Change %%bcond_with author_tests into %%bcond_without author_tests.

* Tue Mar 29 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.44-1
- Upstream update.
- Extend provides-filter to filter versioned perl(Foo), 
  perl(Bar), perl(Baz), perl(DummySerializer).
- Add %%bcond_with author_tests and %%bcond_without smoke_tests.
- Split out CHI::Test and CHI::t into separate sub-package.

* Mon Mar 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.42-1
- Upstream update.

* Mon Feb 07 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.36-1
- Initial Fedora package.
