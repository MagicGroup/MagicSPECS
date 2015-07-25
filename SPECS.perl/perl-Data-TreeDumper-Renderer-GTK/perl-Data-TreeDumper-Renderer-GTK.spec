Name:       perl-Data-TreeDumper-Renderer-GTK 
Version:    0.02
Release:    18%{?dist}
# see GTK.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Gtk2::TreeView renderer for Data::TreeDumper 
Source:     http://search.cpan.org/CPAN/authors/id/N/NK/NKH/Data-TreeDumper-Renderer-GTK-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Data-TreeDumper-Renderer-GTK
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Cairo)
BuildRequires: perl(Data::TreeDumper) >= 0.33
BuildRequires: perl(Glib)
BuildRequires: perl(Gtk2)
BuildRequires: perl(Term::Size)

%{?perl_default_filter}
# not picked up due to use base -- and not "provided" by perl-Gtk2
# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /perl(Gtk2::TreeView)/d
%filter_setup
}
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}perl\\(Gtk2::TreeView\\)

%description
GTK-perl renderer for *Data::TreeDumper*. 

This widget is the gui equivalent of Data::TreeDumper; it will display a
perl data structure in a TreeView, allowing you to fold and unfold child
data structures and get a quick feel for what's where. Right-clicking
anywhere in the view brings up a context menu, from which the user can
choose to expand or collapse all items.


%prep
%setup -q -n Data-TreeDumper-Renderer-GTK-%{version}

find . -type f -exec chmod -c -x {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

find %{buildroot} -type f -name '*.pl' -exec rm -v {} +

%check
%{?_with_display_tests: make test }

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README Changes gtk_test.pl 
%{perl_vendorlib}/* 
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-18
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.02-17
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.02-15
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 0.02-13
- RPM 4.9 dependency filtering added

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.02-12
- Perl mass rebuild

* Fri Feb 25 2011 Iain Arnell <iarnell@gmail.com> 0.02-11
- explicity filter Gtk2::TreeView from requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.02-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-4
- drop a require on Gtk2::TreeView -- not "provided" by perl-Gtk2 (bug?)

* Sun Dec 14 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-3
- bump

* Mon Dec 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-2
- add br perl(Term::Size)
- only enable tests when _with_display_tests; they require $DISPLAY

* Sat Nov 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-1
- update for submission

* Sat Nov 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.02-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

