Name:           perl-SVG
Version:        2.49
Release:        12%{?dist}
Summary:        An extension to generate stand-alone or inline SGV
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/SVG/
Source0:        http://www.cpan.org/authors/id/R/RO/RONAN/SVG-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
SVG.pm is a Perl extension to generate stand-alone or inline SVG
(scaleable vector graphics) images using the W3C SVG XML recommendation

%prep
%setup -q -n SVG-%{version}

# avoid extra dependencies
chmod 644 examples/*

# Fix line-endings
for i in minsvg.pl SVG_02_sample.pl svgtest2.pl sun_text_sample.pl starpath.cgi image_sample.pl inlinesvg.pl yaph5.cgi inline_sample.pl svg.pl; do
    %{__sed} -i 's/\r//' examples/$i
done

# Filter extra non-explicit version provides (SVG::Element)
cat << \EOF > %{_builddir}/SVG-%{version}/%{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(SVG::Element)$/d'
EOF

%define __perl_provides %{_builddir}/SVG-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
# make sure the man page is UTF-8...
cd blib/man3
for i in Element.3pm Manual.3pm ; do
    iconv --from=ISO-8859-1 --to=UTF-8 SVG::$i > new
    mv new SVG::$i
done

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README Changes examples
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.49-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.49-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.49-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.49-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.49-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.49-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.49-1
- Update to upstream 2.49

* Tue Jun  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.44-1
- Update to latest upstream (2.44)
- Fix spec file syntax (#449663)
- Add BR: perl(Test::More)

* Tue Mar 18 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.37-1
- New upstream release (2.37)

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.36-3
- rebuild for new perl

* Sat Oct 13 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.36-2
- Add missing BR: perl(ExtUtils::MakeMaker)

* Sat Oct 13 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.36-1
- Update to 2.36

* Thu Aug 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.34-2
- License tag to GPL+ or Artistic as per new guidelines.

* Sat Aug 18 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.34-1
- Update to latest upstream

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.33-2
- Filter extra non-explicit (SVG::Element) provides

* Wed Mar 14 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.33-1
- Update to 2.33
- Fix rpmlint issues

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 2.32-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 2.32-1
- Initial packaging.
