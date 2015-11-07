Name:       perl-srpm-macros    
Version:    1
Release:    8%{?dist}
Summary:    RPM macros for building Perl source package from source repository
Group:      Development/Libraries
License:    GPLv3+
Source0:    macros.perl-srpm
BuildArch:  noarch

%description
These RPM macros are used for building Perl source packages from source
repositories. They influence build-requires set into the source package.

%install
install -m 644 -D "%{SOURCE0}" \
    "$RPM_BUILD_ROOT/%{_sysconfdir}/rpm/macros.perl-srpm"

%files
%config %{_sysconfdir}/rpm/macros.perl-srpm

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1-8
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1-4
- Disable perl_bootstrap for perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1-3
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1-2
- Enable perl_bootstrap for perl 5.16 rebuild

* Tue May 15 2012 Petr Pisar <ppisar@redhat.com> - 1-1
- Introduce Perl SRPM macros as a standalone package


