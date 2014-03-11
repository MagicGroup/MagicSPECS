Name:           perl-Imager
Version:        0.87
Release:        3%{?dist}
Summary:        Perl extension for Generating 24 bit Images
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Imager/
Source0:        http://www.cpan.org/authors/id/T/TO/TONYC/Imager-%{version}.tar.gz
BuildRequires:  perl(Affix::Infix2Postfix)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Image::Math::Constrain)
BuildRequires:  perl(Inline)
BuildRequires:  perl(Parse::RecDescent)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08

BuildRequires:  freetype-devel
BuildRequires:  giflib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  t1lib-devel
# rgb.txt, c.f. lib/Imager/Color.pm
BuildRequires:  rgb

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Imager is a module for creating and altering images. It can read and
write various image formats, draw primitive shapes like lines,and
polygons, blend multiple images together in various ways, scale, crop,
render text and more.

%prep
%setup -q -n Imager-%{version}
# fix permissions
find \( -executable -a -type f \) -exec chmod -x {} \;
# Adjust shebang
sed -i -e "s,#!perl,#! %{__perl}," samples/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README samples
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Imager*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.87-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.87-2
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> 0.87-1
- Upstream update.

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 0.86-1
- Update to latest upstream version

* Tue Sep 06 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.85-1
- Upstream update.

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.84-2
- Perl mass rebuild

* Mon Jun 27 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.84-1
- Upstream update.
- Modernize spec-file.

* Sun May 22 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.83-1
- Upstream update.

* Wed Mar 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.82-1
- Upstream update.

* Fri Feb 18 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.81-1
- Upstream update.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.80-1
- Upstream update.
- BR: giflib-devel instead of libungif-devel.
- spec file massage.
- Add perl_default_filter.

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.79-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Steven Pritchard <steve@kspei.com> 0.79-1
- Update to 0.79.

* Fri Dec 10 2010 Steven Pritchard <steve@kspei.com> 0.78-1
- Update to 0.78.

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.67-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.67-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Steven Pritchard <steve@kspei.com> 0.67-1
- Update to 0.67.

* Sat May 31 2008 Steven Pritchard <steve@kspei.com> 0.65-1
- Update to 0.65.

* Thu Apr 24 2008 Steven Pritchard <steve@kspei.com> 0.64-2
- Rebuild.

* Thu Apr 24 2008 Steven Pritchard <steve@kspei.com> 0.64-1
- Update to 0.64 (CVE-2008-1928).
- Add versioned Test::More BR.

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.62-3
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.62-2
- Autorebuild for GCC 4.3

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 0.62-1
- Update to 0.62.
- Update License tag.

* Mon Sep 17 2007 Steven Pritchard <steve@kspei.com> 0.60-1
- Update to 0.60.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.59-2
- Rebuild for selinux ppc32 issue.

* Tue Jun 26 2007 Steven Pritchard <steve@kspei.com> 0.59-1
- Update to 0.59.

* Fri May 18 2007 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- Drop hack to change location of rgb.txt (fixed upstream).
- BR Image::Math::Constrain and Affix::Infix2Postfix for better test coverage.

* Tue May 01 2007 Steven Pritchard <steve@kspei.com> 0.57-1
- Update to 0.57.
- BR gdbm-devel.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 0.56-2
- BR Inline, Test::Pod, and Test::Pod::Coverage perl modules and rgb
  (for rgb.txt) for better test coverage.
- Fix path to rgb.txt in lib/Imager/Color.pm and t/t15color.t.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 0.56-1
- Update to 0.56.
- BR ExtUtils::MakeMaker.

* Tue Dec 26 2006 Steven Pritchard <steve@kspei.com> 0.55-1
- Update to 0.55.
- Cleanup to more closely resemble current cpanspec output.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.54-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 0.54-1
- Update to 0.54.
- Fix find option order.

* Fri Apr 07 2006 Gavin Henry <ghenry[AT]suretecsystems.com> - 0.50-1
- Updated version for security fix

* Tue Feb 28 2006 Gavin Henry <ghenry[AT]suretecsystems.com> - 0.47-1
- Updated version

* Wed Sep 14 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 0.45-2
- Applied Steven Pritchard's kind patch to cleanup -
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=166254

* Thu Aug 18 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 0.45-1
- First build.
