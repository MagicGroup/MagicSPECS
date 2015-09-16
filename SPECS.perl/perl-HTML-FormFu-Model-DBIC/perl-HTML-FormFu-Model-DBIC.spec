Name:           perl-HTML-FormFu-Model-DBIC
Summary:        Integrate HTML::FormFu with DBIx::Class
Version:	2.00
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/C/CF/CFRANKS/HTML-FormFu-Model-DBIC-%{version}.tar.gz
URL:            http://search.cpan.org/dist/HTML-FormFu-Model-DBIC
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(DateTime::Format::SQLite)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(DBIx::Class) >= 0.08108
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(HTML::FormFu) >= 0.09000
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(SQL::Translator)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::MockObject)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(YAML::Syck)

Requires:       perl(DBIx::Class) >= 0.08108
Requires:       perl(HTML::FormFu) >= 0.09000


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
Integrate your HTML::FormFu forms with a DBIx::Class model.


%prep
%setup -q -n HTML-FormFu-Model-DBIC-%{version}
sed -i -e 's/\r//' t/update/null_if_empty.t

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
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.00-1
- 更新到 2.00

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-13
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09002-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.09002-11
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.09002-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.09002-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.09002-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09002-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09002-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09002-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09002-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09002-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.09002-2
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.09002-1
- Update to 0.09002
- Remove the defattr macro (no longer used)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.09000-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.09000-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.09000-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08002-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Dec 09 2010 Iain Arnell <iarnell@gmail.com> 0.08002-1
- update to latest upstream version
- fixes FTBFS RHBZ#660763
- clean up spec for modern rpmbuild

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06000-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.06000-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.06000)
- altered br on perl(DBIx::Class) (0.08106 => 0.08108)
- added a new br on perl(SQL::Translator) (version 0)
- altered req on perl(DBIx::Class) (0.08106 => 0.08108)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05002-2
- rebuild against perl 5.10.1

* Sat Aug 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05002-1
- auto-update to 0.05002 (by cpan-spec-update 0.01)
- altered br on perl(DBIx::Class) (0.08002 => 0.08106)
- added a new br on perl(DateTime::Format::SQLite) (version 0)
- altered br on perl(HTML::FormFu) (0.03007 => 0.05000)
- added a new br on perl(List::MoreUtils) (version 0)
- added a new req on perl(DBD::SQLite) (version 0)
- altered req on perl(DBIx::Class) (0 => 0.08106)
- added a new req on perl(HTML::FormFu) (version 0.05000)
- added a new req on perl(List::MoreUtils) (version 0)
- added a new req on perl(Task::Weaken) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03007-1
- touch up for submission

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.03007-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
