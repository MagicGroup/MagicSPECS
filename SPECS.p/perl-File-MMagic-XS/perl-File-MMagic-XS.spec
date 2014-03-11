Name:           perl-File-MMagic-XS
Version:        0.09006
Release:        10%{?dist}
Summary:        Guess file type with XS
Group:          Development/Libraries
License:        ASL 2.0 and (GPL+ or Artistic)
URL:            http://search.cpan.org/dist/File-MMagic-XS
Source0:        http://search.cpan.org/CPAN/authors/id/D/DM/DMAKI/File-MMagic-XS-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(File::MMagic), gdbm-devel, perl(Test::More)
Requires:  perl(File::MMagic)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a port of Apache2 mod_mime_magic.c in Perl, written in XS with the aim 
of being efficient and fast especially for applications that need to be run for
an extended amount of time.

%prep
%setup -q -n File-MMagic-XS-%{version}

cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
    sed -e '/^perl(File::MMagic::XS)$/d'
EOF
%define __perl_provides %{_builddir}/File-MMagic-XS-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/auto/File/
%{perl_vendorarch}/File/
%{_mandir}/man3/*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09006-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09006-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.09006-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.09006-6
- Own vendor_perl/File dirs.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09006-5
- Perl mass rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09006-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09006-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09006-1
- update to 0.09006

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09003-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09003-7
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09003-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.09003-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.09003-3
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.09003-2
- rebuild for new perl

* Mon Dec 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.09003-1
- bump to 0.09003

* Sun Aug 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.09002-2
- license tag fix
- rebuild in devel for ppc32

* Thu Jul 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.09002-1.1
- BR: perl(Test::More)

* Thu Jul 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.09002-1
- hate hate hate perl versioning

* Sun Sep 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- filter out extra perl(File::MMagic::XS) provides
- fix license descriptor to make rpmlint happy

* Thu Aug  3 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-1
- initial package for Fedora Extras
