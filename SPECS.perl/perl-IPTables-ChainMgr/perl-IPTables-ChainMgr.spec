Name:           perl-IPTables-ChainMgr
Version:        0.9
Release:        14%{?dist}
Summary:        Perl extension for manipulating iptables policies
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://www.cipherdyne.org/modules/
Source0:        http://www.cipherdyne.org/modules/IPTables-ChainMgr-%{version}.tar.bz2
Source1:        http://www.cipherdyne.org/modules/IPTables-ChainMgr-%{version}.tar.bz2.asc
Patch0:         IPTables-ChainMgr-0.9-qw.patch
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IPTables::Parse), perl(Net::IPv4Addr)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The IPTables::ChainMgr package provides an interface to manipulate iptables
policies on Linux systems through the direct execution of iptables
commands. Although making a perl extension of libiptc provided by the iptables
project is possible, it is easy to just execute iptables commands directly in
order to both parse and change the configuration of the policy. Further, this
simplifies installation since the only external requirement is (in the spirit
of scripting) to be able to point IPTables::ChainMgr at an installed iptables
binary instead of having to compile against a library.

%prep
%setup -q -n IPTables-ChainMgr-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.9-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.9-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.9-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.9-10
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Miloslav Trmač <mitr@redhat.com> - 0.9-9
- Avoid deprecated use of qw()
  Resolves: #771781

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com>
- Mass rebuild with perl-5.12.0

- Drop no longer required references to BuildRoot

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Miloslav Trmač <mitr@redhat.com> - 0.9-1
- Update to IPTables-ChainMgr-0.9.

* Tue Oct 21 2008 Miloslav Trmač <mitr@redhat.com> - 0.8-1
- Update to IPTables-ChainMgr-0.8.

* Wed Jul 30 2008 Miloslav Trmač <mitr@redhat.com> 0.7-1
- Initial package.
