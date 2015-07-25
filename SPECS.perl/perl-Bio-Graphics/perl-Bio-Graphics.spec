Name:           perl-Bio-Graphics
Version:	2.39
Release:	1%{?dist}
Summary:        Generate GD images of Bio::Seq objects
Summary(zh_CN.UTF-8): Bio::Seq 对象生成 GD 图像
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Bio-Graphics/
Source0:        http://www.cpan.org/authors/id/L/LD/LDS/Bio-Graphics-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Bio::Root::Version) >= 1.005009
BuildRequires:  perl(GD) >= 2.3
BuildRequires:  perl(GD::SVG)
BuildRequires:  perl(Statistics::Descriptive) >= 2.6
BuildRequires:  perl(Module::Build)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Bio::Graphics is a simple GD-based renderer (diagram drawer) for DNA
and protein sequences.  The Bio::Graphics::Panel class provides
drawing and formatting services for any object that implements the
Bio::SeqFeatureI interface, including Ace::Sequence::Feature,
Das::Segment::Feature and Bio::DB::Graphics objects.  It can be used
to draw sequence annotations, physical (contig) maps, protein domains,
or any other type of map in which a set of discrete ranges need to be
laid out on the number line

%description -l zh_CN.UTF-8
Bio::Seq 对象生成 GD 图像。

# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /^perl(colors)/d; /perl(Bio::DB::BigWig)/d
%{?perl_default_filter}
}
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}(perl\\(colors\\)|perl\\(Bio::DB::BigWig\\))

%prep
%setup -q -n Bio-Graphics-%{version}

# temporarily remove modules Bio/Graphics/Glyph/trace.pm until the dependency:
# Bio::SCF is packaged
rm lib/Bio/Graphics/Glyph/trace.pm

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
#./Build test

%files
%doc Changes DISCLAIMER.txt README README.bioperl
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 2.39-1
- 更新到 2.39

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.25-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.25-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.25-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.25-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.25-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.25-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.25-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.25-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.25-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.25-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.25-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.25-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 2.25-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.25-2
- Filter Bio::DB::BigWig dependency for 4.8 and 4.9:  as per:
  http://fedoraproject.org/wiki/User:Tibbs/AutoProvidesAndRequiresFiltering
  should not be a hard-dependency (#745537).

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.25-1
- 2.25

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 2.14-5
- RPM 4.9 dependency filtering added

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.14-4
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.14-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.14-2
- Perl mass rebuild

* Fri Feb 25 2011 Marcela Maslanova <mmaslano@redhat.com> - 2.14-1
- filter requires
- update

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.11-3
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Aug  9 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.11-2
- remove file which needs missing Bio::Graphics

* Fri Aug  6 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.11-1
- update, tests pass fine

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.994-3
- Mass rebuild with perl-5.12.0

* Tue Dec 22 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.994-2
- Fix disabling of tests

* Tue Dec 22 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.994-1
- Update to upstream 1.994

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.97-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.97-1
- Update to latest upstream (1.97) to fix FTBFS (#511633) and disable
  tests temporarily (reported upstream: 
  http://rt.cpan.org/Public/Bug/Display.html?id=47935)

* Tue May  5 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.94-1
- Update to latest upstream (1.94)
- Drop patch for disabling tests

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.84-1
- Update to upstream that fixes the bogus dependency on perl(GBrowse).
- Add BR: Statistics::Descriptive
- Continue to leave out the optional package
  Bio::Graphics::Glyph::trace until Bio::SCF is packaged

* Tue Jan 27 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.83-3
- Temporarily remove Bio::Graphics::Wiggle::Loader and
  Bio::Graphics::Glyph::trace modules from being installed until their
  deps are packaged

* Mon Jan 26 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.83-2
- Patch to disable some tests (image tests currently don't work)
- Fix file list to include scripts

* Mon Jan 26 2009 Alex Lancaster <alexlan[AT]fedoraproject org> 1.83-1
- Specfile autogenerated by cpanspec 1.77.
