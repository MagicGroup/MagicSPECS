Name:		perl-Cwd-Guard
Version:	0.04
Release:	7%{?dist}
Summary:	Temporarily change the current directory
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Cwd-Guard/
Source0:	http://search.cpan.org/CPAN/authors/id/K/KA/KAZEBURO/Cwd-Guard-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(utf8)
# Module Runtime
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(if)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Test::More) >= 0.88
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Cwd::Guard can change the current directory (chdir) using a limited scope.

  use Cwd::Guard qw/cwd_guard/;
  use Cwd;
 
  my $dir = getcwd;
  MYBLOCK: {
    my $guard = cwd_guard('/tmp/xxxxx') or die
      "failed chdir: $Cwd::Guard::Error";
    ... # chdir to /tmp/xxxxx
  }
  ... # back to $dir

%prep
%setup -q -n Cwd-Guard-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
./Build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Cwd/
%{_mandir}/man3/Cwd::Guard.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.04-7
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.04-6
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.04-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-3
- Perl 5.22 rebuild

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 0.04-2
- Sanitize for Fedora submission

* Sat Oct  4 2014 Paul Howarth <paul@city-fan.org> - 0.04-1
- Initial RPM version
