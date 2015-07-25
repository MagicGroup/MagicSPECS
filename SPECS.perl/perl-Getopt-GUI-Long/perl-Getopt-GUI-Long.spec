Name:           perl-Getopt-GUI-Long
Version:        0.91
Release:        11%{?dist}
Summary:        A wrapper around Getopt::Long to provide a GUI to applications
License:        GPL+ or Artistic 
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Getopt-GUI-Long/
Source0:        http://www.cpan.org/authors/id/H/HA/HARDAKER/Getopt-GUI-Long-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
# These are not auto-detected since they're technically optional
# (they're the best of the alternative choices available on linux)
Requires:       perl(QWizard)
Requires:       perl(Gtk2)

# neither are picked up automagically.
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is a wrapper around Getopt::Long that extends the value of
the original Getopt::Long module to:

1) add a simple graphical user interface option screen if no arguments
   are passed to the program.  Thus, the arguments to actually use are
   built based on the results of the user interface. If arguments were
   passed to the program, the user interface is not shown and the
   program executes as it normally would and acts just as if
   Getopt::Long::GetOptions had been called instead.  This requires
   the QWizard and Gtk2 or Tk interfaces to be installed too.

2) provide an auto-help mechanism such that -h and --help are
   handled automatically.  In fact, calling your program with -h
   will default to showing the user a list of short-style arguments
   when one exists for the option.  Similarly --help will show the
   user a list of long-style when possible.  --help-full will list
   all potential arguments for an option (short and long both).

It's designed to make the creation of graphical shells trivial
without the programmer having to think about it much as well as
providing automatic good-looking usage output without the
programmer needing to write usage() functions.

%prep
%setup -q -n Getopt-GUI-Long-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

# rpm doc examples shouldn't be executable
chmod a-x examples/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc examples/
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.91-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.91-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.91-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.91-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.91-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.91-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.91-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Wes Hardaker <wjhns174@hardakers.net> - 0.91-1
- Update to 0.91

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8-2
Rebuild for new perl

* Wed Dec 19 2007 Wes Hardaker <wjhns174@hardakers.net> - 0.8-1
- initial version

