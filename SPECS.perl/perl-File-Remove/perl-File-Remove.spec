Name:		perl-File-Remove
Version:	1.52
Release:	9%{?dist}
Summary:	Convenience module for removing files and directories
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/File-Remove/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/File-Remove-%{version}.tar.gz

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(File::Spec) >= 3.29
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Glob)

BuildArch:	noarch

%description
%{summary}

%prep
%setup -q -n File-Remove-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.52-9
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.52-8
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.52-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.52-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.52-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.52-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.52-2
- Perl 5.16 rebuild

* Tue Mar 20 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.52-1
- Upstream update.
- Remove File-Remove-1.51.diff.
- BR: perl(File::Spec) >= 3.29.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.51-1
- Upstream update.
- Add File-Remove-1.51.diff/Remove File-Remove-1.50.diff.

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 1.50-2
- Perl mass rebuild

* Sun Jul 17 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.50-1
- Upstream update.
- Add File-Remove-1.50.diff/Remove File-Remove-1.49.diff.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.49-2
- Perl mass rebuild

* Mon Mar 28 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.49-1
- Upstream update.
- Add File-Remove-1.49.diff/Remove File-Remove-1.46.diff.
- Spec file cleanup.

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46-1
- Upstream update.
- Remove xt-tests's deps (Upstream doesn't want us to test their works).
- Work around rpm-/perl-version conflicts.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-7
- Rebuild with perl-5.12.0.

* Sun May 09 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.42-6
- Let META.yml require perl 5.006 (Fix perl-5.12.0 build breakdown).
- Revert 2010-05-01 changes.

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.42-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.42-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 10 2008 Ralf Corsepius <rc040203@freenet.de> - 1.42-1
- Upstream update.

* Tue Jun 10 2008 Ralf Corsepius <rc040203@freenet.de> - 1.41-1
- Upstream update.

* Thu Mar 13 2008 Ralf Corsepius <rc040203@freenet.de> - 1.40-1
- Upstream update.

* Thu Feb 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-7
- Rebuild normally, second pass

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-6
- Rebuild for perl 5.10 (again), first pass

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-5
- rebuild normally, second pass

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-4.1
- rebuild, first pass, without TMV, tests

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.39-4
- rebuild for new perl

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-3
- Really BR: perl(Test::MinimumVersion).

* Sun Nov 25 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-2
- Add BR: perl(Test::MinimumVersion).

* Tue Nov 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.39-1
- Upstream update.

* Wed Oct 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.38-1
- Upstream update.

* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.37-2
- Update license tag.

* Tue Jul 10 2007 Ralf Corsépius <rc040203@freenet.de> - 0.37-1
- Upstream update.

* Mon Jul 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.36-2
- Increment release due to koji suckage.

* Mon Jul 02 2007 Ralf Corsépius <rc040203@freenet.de> - 0.36-1
- Upsteam update.
- BR: perl(ExtUtils::MakeMaker).
- BR: perl(Test::More).

* Mon Nov 27 2006 Ralf Corsépius <rc040203@freenet.de> - 0.34-1
- Upstream update.
- Fix URL in Source0.

* Fri Nov 03 2006 Ralf Corsépius <rc040203@freenet.de> - 0.33-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.31-3
- Mass rebuild.

* Wed Mar 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.31-2
- Rebuild for perl-5.8.8.

* Wed Jan 11 2006 Ralf Corsepius <rc040203@freenet.de> - 0.31-1
- Upstream update.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.30-2
- Change %%summary according to Ville's preference.

* Tue Sep 13 2005 Ralf Corsepius <rc040203@freenet.de> - 0.30-1
- FE submission.
