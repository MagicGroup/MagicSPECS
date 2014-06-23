
Name:		perl-GO-TermFinder
Version:	0.82
Release:	14%{?dist}
Summary:	Identify GO nodes that annotate a group of genes with a significant p-value
License:	MIT
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Go-TermFinder/
Source0:	http://www.cpan.org/authors/id/S/SH/SHERLOCK/GO-TermFinder-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires:	perl(GD), perl(GraphViz)

Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(Storable), perl(GD), perl(GraphViz), perl(CGI)

# Filter out perl(Hang) and perl(NullHang) auto-provides.
Source99:	GO-TermFinder-filter-provides.sh

%global real_perl_provides %{__perl_provides}
%define __perl_provides %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)-filter-provides

%description
This package is intended to provide a method whereby the P-values of a set
of GO annotations can be determined for a set of genes, based on the number
of genes that exist in the particular genome (or in a selected background
distribution from the genome), and their annotation, and the frequency with
which the GO nodes are annotated across the provided set of genes. The
P-value is simply calculated using the hypergeometric distribution as the
probability of x or more out of n genes having a given annotation, given
that G of N have that annotation in the genome in general. We chose the
hypergeometric distribution (sampling without replacement) since it is more
accurate, though slower to calculate, than the binomial distribution
(sampling with replacement).

%prep
%setup -q -n GO-TermFinder-%{version}
chmod a-x lib/GO/TermFinder.pm Changes README

sed -e 's,@@PERL_PROV@@,%{real_perl_provides},' %{SOURCE99} > %{__perl_provides}
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.bs" -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
find $RPM_BUILD_ROOT -type f -name "*.pm" -exec chmod 644 {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# this test seems to have issues with being unable to resolve the builder's
# hostname inside mock.
%{?!_with_termfinder_native: rm t/GO-TermFinder-Native.t }


%clean
rm -rf $RPM_BUILD_ROOT %{__perl_provides}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.82-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.82-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.82-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.82-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.82-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.82-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.82-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.82-2
- Add suggested BuildRequires as per review (#447559)

* Tue May 20 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.82-1
- Initial packaging
