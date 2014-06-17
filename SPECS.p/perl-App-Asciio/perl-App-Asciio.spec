Name:       perl-App-Asciio 
Version:    1.02.71 
Release:    20%{?dist}
# see lib/App/Asciio.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Asciio back-end libraries 
Source:     http://search.cpan.org/CPAN/authors/id/N/NK/NKH/App-Asciio-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/App-Asciio
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

# non-perl
BuildRequires: desktop-file-utils

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Module::Build::Compat)
BuildRequires: perl(Algorithm::Diff)
BuildRequires: perl(Clone)
BuildRequires: perl(Compress::Bzip2)
BuildRequires: perl(Cwd)
BuildRequires: perl(Data::Compare)
BuildRequires: perl(Data::TreeDumper)
BuildRequires: perl(Data::TreeDumper::Renderer::GTK)
BuildRequires: perl(Directory::Scratch)
BuildRequires: perl(Directory::Scratch::Structured)
BuildRequires: perl(Eval::Context)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Slurp)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Glib)
BuildRequires: perl(Gtk2)
BuildRequires: perl(Gtk2::Gdk::Keysyms)
BuildRequires: perl(List::MoreUtils)
BuildRequires: perl(List::Util)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Module::Util)
BuildRequires: perl(Readonly)
BuildRequires: perl(Sub::Exporter)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Block)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Test::NoWarnings)
BuildRequires: perl(Test::Strict)
BuildRequires: perl(Test::Warn)
BuildRequires: perl(version) >= 0.5

# keep rpmlint happy 
Requires:      perl(lib)

# this package has a rather basic way of mixing-in functionalities that leads
# rpm to believe that it doesn't actually provide these
Provides: perl(App::Asciio::Actions)     = %{version}
Provides: perl(App::Asciio::Ascii)       = %{version}
Provides: perl(App::Asciio::Connections) = %{version}
Provides: perl(App::Asciio::Dialogs)     = %{version}
Provides: perl(App::Asciio::Elements)    = %{version}
Provides: perl(App::Asciio::Io)          = %{version}
Provides: perl(App::Asciio::Menues)      = %{version}
Provides: perl(App::Asciio::Options)     = %{version}
Provides: perl(App::Asciio::Setup)       = %{version}
Provides: perl(App::Asciio::Undo)        = %{version}

%{?perl_default_filter}

%description
This gtk2-perl application allows you to draw ASCII diagrams in a modern
(but simple) graphical application. The ASCII graphs can be saved as ASCII
or in a format that allows you to modify them later.

This package contains the back-end libraries needed to implement asciio.  For
the actual application itself, please install the 'asciio' package.

%package -n asciio
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Draw ascii art quickly and easily!
Requires:   %{name} = %{version}-%{release}

%description -n asciio
This application allows you to draw ASCII diagrams in a modern (but simple)
graphical application. The ASCII graphs can be saved as ASCII or in a format
that allows you to modify them later.

Think: Visio for ASCII :-)

%prep
%setup -q -n App-Asciio-%{version}

# generate our menu entry
cat << \EOF > asciio.desktop
[Desktop Entry] 
Name=Asciio
GenericName=Ascii diagrams editor
Comment=Ascii diagrams editor
Exec=%{_bindir}/asciio
#Icon= no icon currently
Terminal=false
Type=Application
Categories=Graphics;
Version=0.9.4
EOF

# fix perms
find . -type f -exec chmod -c -x {} +

# filter out unwanted (unversioned) provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
sed -e '/^perl(App::Asciio)$/d'
EOF

%define __perl_provides %{_builddir}/App-Asciio-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

# desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications asciio.desktop

%check
# passes outside of rpm, but fails in rpmbuild F-10+ (no $DISPLAY)
#make test

%files
%doc README Changes documentation/ 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%files -n asciio
%defattr(-,root,root,-)
%doc README
%{_bindir}/*
%{_datadir}/applications/*


%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.02.71-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.02.71-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.02.71-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.02.71-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.02.71-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.02.71-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.02.71-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.71-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Petr Pisar <ppisar@redhat.com> - 1.02.71-12
- Perl 5.16 rebuild

* Sun Mar 11 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr - 1.02.71-11
- Add perl default filter
- Clean up spec file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.71-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.02.71-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.71-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02.71-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.02.71-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.02.71-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.02.71-2
- update per RHBZ#483676, comment #3

* Mon Jan 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.02.71-1
- update to 1.02.71

* Sat Nov 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.01-2
- update for submission
- break out into asciio subpackage

* Sun Oct 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.01-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)

