Name:           perl-forks
Version:	0.36
Release:	1%{?dist}
Summary:        A drop-in replacement for Perl threads using fork()

Group:          Development/Libraries
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic)
URL:            http://search.cpan.org/~rybskej/%{name}-%{version}/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RY/RYBSKEJ/forks-%{version}.tar.gz
# https://bugzilla.novell.com/show_bug.cgi?id=527537
# https://bugzillafiles.novell.org/attachment.cgi?id=313860
# http://rt.cpan.org/Public/Bug/Display.html?id=49878
Patch0:         perl-forks-assertion.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker), perl(List::MoreUtils)
BuildRequires:  perl(Sys::SigAction) >= 0.11, perl(Acme::Damn)
BuildRequires:  perl(Devel::Symdump), perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# This provides is not getting picked up
Provides:       perl(forks::Devel::Symdump) = %{version}

%description
The forks.pm module is a drop-in replacement for threads.pm.  It has the
same syntax as the threads.pm module (it even takes over its namespace) but
has some significant differences:

- you do _not_ need a special (threaded) version of Perl
- it is _much_ more economic with memory usage on OS's that support COW
- it is more efficient in the startup of threads
- it is slightly less efficient in the stopping of threads
- it is less efficient in inter-thread communication

If for nothing else, it allows you to use the Perl threading model in
non-threaded Perl builds and in older versions of Perl (5.6.0 and
higher are supported).


%prep
%setup -q -n forks-%{version}

# see comments above for origin and upstream bug report
%patch0 -p1 -b .perl-forks-assertion


%build
find . -type f -print | xargs chmod a-x
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.36-1
- 更新到 0.36

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.34-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.34-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.34-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.34-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.34-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.34-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.34-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.34-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.34-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.34-6
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.34-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jun 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-1
- update because https://rt.cpan.org/Public/Bug/Display.html?id=56263

* Sun May 02 2010 Bernard Johnson <bjohnson@symetrix.com> - 0.33-5
- always apply assertion patch

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.33-4
- Mass rebuild with perl-5.12.0

* Sun Jan 31 2010 Bernard Johnson <bjohnson@symetrix.com> - 0.33-3
- fix permissions in build to squelch rpmlint complaints
- add version to provides

* Tue Jan 19 2010 Bernard Johnson <bjohnson@symetrix.com> - 0.33-2
- fix BR
- add patch from novell site to fix assertion in fedora < 13
- change references of forks::Devel::Symdump to Devel::Symdump

* Fri Jun 06 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.33-1
- initial release
