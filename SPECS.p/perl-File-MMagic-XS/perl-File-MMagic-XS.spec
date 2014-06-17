Name:           perl-File-MMagic-XS
Version:        0.09006
Release:        17%{?dist}
Summary:        Guess file type with XS
Group:          Development/Libraries
License:        ASL 2.0 and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/File-MMagic-XS
Source0:        http://search.cpan.org/CPAN/authors/id/D/DM/DMAKI/File-MMagic-XS-%{version}.tar.gz
# Perl 5.18 compatibility, CPAN RT#63048
Patch0:         File-MMagic-XS-0.09006-qw-does-not-produce-array-context-anymore.patch
Patch1:		perl-File-MMagic-XS-format-security.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:  gdbm-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::MMagic)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::MMagic)
Requires:       perl(File::Spec)

# Avoid unwanted shared object provides
%{?perl_default_filter}

%description
This is a port of Apache2 mod_mime_magic.c in Perl, written in XS with the aim 
of being efficient and fast especially for applications that need to be run for
an extended amount of time.

%prep
%setup -q -n File-MMagic-XS-%{version}
%patch0 -p1
%patch1 -p1 -b .format-security

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes
%{perl_vendorarch}/auto/File/
%{perl_vendorarch}/File/
%{_mandir}/man3/File::MMagic::XS.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09006-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09006-16
- 为 Magic 3.0 重建


