Name:           perl-Tk-Getopt
Version:        0.50
Release:        13%{?dist}
Summary:        User configuration window for Tk with interface to Getopt::Long
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Tk-Getopt/
Source0:        http://www.cpan.org/authors/id/S/SR/SREZIC/Tk-Getopt-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Tk) >= 804
# Optional      perl(Tk::Balloon)
BuildRequires:  perl(Tk::BrowseEntry)
BuildRequires:  perl(Tk::CmdLine)
# Optional fall back  perl(Tk::DirSelect)
BuildRequires:  perl(Tk::DirTree)
# Optional  perl(Tk::FileDialog) is old and buggy. Tk::FileSelect is fall-back
BuildRequires:  perl(Tk::FileSelect)
BuildRequires:  perl(Tk::Font)
# Optional not yet packaged  perl(Tk::FontDialog)
# Optional      perl(Tk::NoteBook)
BuildRequires:  perl(Tk::Optionmenu)
# Optional not yet packaged  perl(Tk::PathEntry)
BuildRequires:  perl(Tk::Photo)
BuildRequires:  perl(Tk::Pixmap)
BuildRequires:  perl(Tk::Tiler)
# Tests
BuildRequires:  perl(Test::More)
# Optional tests
BuildRequires:  perl(File::Temp)
# Optional not yet packaged  perl(Tk::Dial)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Cwd)
Requires:       perl(Data::Dumper)
Requires:       perl(File::Basename)
Requires:       perl(Getopt::Long)
Requires:       perl(Safe)
Requires:       perl(Tk) >= 804
# Optional      perl(Tk::Balloon)
Requires:       perl(Tk::BrowseEntry)
Requires:       perl(Tk::CmdLine)
# Optional fall back  perl(Tk::DirSelect)
Requires:       perl(Tk::DirTree)
# Optional  perl(Tk::FileDialog) is old and buggy. Tk::FileSelect is fall-back
Requires:       perl(Tk::FileSelect)
Requires:       perl(Tk::Font)
# Optional not yet packaged  perl(Tk::FontDialog)
# Optional      perl(Tk::NoteBook)
Requires:       perl(Tk::Optionmenu)
# Optional not yet packaged  perl(Tk::PathEntry)
Requires:       perl(Tk::Photo)
Requires:       perl(Tk::Pixmap)
Requires:       perl(Tk::Tiler)

# Filter optional not yet packaged  perl(Tk::PathEntry)
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(Tk::PathEntry\\)

%description
Tk::Getopt provides an interface to access command line options via
Getopt::Long and editing with a graphical user interface via a Tk window.

%prep
%setup -q -n Tk-Getopt-%{version}
chmod -x demos/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%doc Changes demos README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.50-13
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.50-12
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.50-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.50-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.50-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.50-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.50-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.50-2
- Perl 5.16 rebuild

* Wed Feb 22 2012 Petr Pisar <ppisar@redhat.com> 0.50-1
- Specfile autogenerated by cpanspec 1.78.
