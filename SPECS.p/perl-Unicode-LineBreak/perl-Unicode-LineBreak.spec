Name:           perl-Unicode-LineBreak
Version:        2013.11
Release:        1%{?dist}
Summary:        UAX #14 Unicode Line Breaking Algorithm
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Unicode-LineBreak/
Source0:        http://search.cpan.org/CPAN/authors/id/N/NE/NEZUMI/Unicode-LineBreak-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# libthai is not available (yet) on EL5 and earlier.
%if 0%{?rhel} > 5 || 0%{?fedora}
BuildRequires:  libthai-devel
%endif
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  pkgconfig
BuildRequires:  sombok-devel
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode) >= 1.98
BuildRequires:  perl(Exporter)
BuildRequires:  perl(MIME::Charset) >= 1.006.2
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(Test::More) >= 0.45
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Encode) >= 1.98
Requires:       perl(MIME::Charset) >= 1.006.2


%if 0%{?rhel} > 5
%filter_from_provides /^perl(Unicode::LineBreak)$/d
%filter_from_requires /^perl(Unicode::LineBreak::Constants)$/d
%{?perl_default_filter}
%endif

%if 0%{?fedora} > 14
%{?filter_setup:
%filter_from_requires /perl(Unicode::LineBreak::Constants)/d
%filter_from_provides /^perl(Unicode::LineBreak)$/d
}
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Unicode::LineBreak::Constants\\)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Unicode::LineBreak\\)$
%endif


%description
Unicode::LineBreak performs Line Breaking Algorithm described in Unicode
Standards Annex #14 [UAX #14]. East_Asian_Width informative properties
defined by Annex #11 [UAX #11] will be concerned to determine breaking
positions.


%prep
%setup -q -n Unicode-LineBreak-%{version}
# Remove bundled library
rm -rf sombok
sed -i -e '/^sombok/d' MANIFEST


%if 0%{?rhel} == 5
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/^perl(Unicode::LineBreak)$/d'
EOF
%define __perl_provides %{_builddir}/Unicode-LineBreak-%{version}/%{name}-prov
chmod +x %{__perl_provides}
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/^perl(Unicode::LineBreak::Constants)$/d'
EOF
%define __perl_requires %{_builddir}/Unicode-LineBreak-%{version}/%{name}-req
chmod +x %{__perl_requires}
%endif


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

mkdir -p $RPM_BUILD_ROOT%{_mandir}/ja/man3
for mod in Text::LineFold Unicode::GCString Unicode::LineBreak; do
  mv $RPM_BUILD_ROOT%{_mandir}/man3/POD2::JA::$mod.3pm \
     $RPM_BUILD_ROOT%{_mandir}/ja/man3/$mod.3pm
done

%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ARTISTIC Changes Changes.REL1 GPL README Todo.REL1
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Unicode*
%{perl_vendorarch}/Text
%{perl_vendorarch}/POD2
%{_mandir}/man3/*
%{_mandir}/ja/man3/*


%changelog
* Mon Dec 02 2013 Xavier Bachelot <xavier@bachelot.org> 2013.11-1
- Update to 2013.11.

* Mon Oct 21 2013 Xavier Bachelot <xavier@bachelot.org> 2013.10-1
- Update to 2013.10.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 2012.06-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 2012.06-2
- Perl 5.16 rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2012.06-1
- 2012.06 bump (to fix building)

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 2011.11-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Xavier Bachelot <xavier@bachelot.org> 2011.11-2
- Filter out bad requires perl(Unicode::LineBreak::Constants).
- Adapt provides and requires filtering to handle all 3 variants
  (EL5; F14/EL6; F15+).

* Fri Nov 18 2011 Xavier Bachelot <xavier@bachelot.org> 2011.11-1
- Update to 2011.11.

* Mon Oct 17 2011 Xavier Bachelot <xavier@bachelot.org> 2011.05-4
- Drop patch and revert to stricter provides filtering.

* Mon Oct 10 2011 Xavier Bachelot <xavier@bachelot.org> 2011.05-3
- Add patch to fix provides.
- Fix provides filtering.

* Mon Aug 01 2011 Xavier Bachelot <xavier@bachelot.org> 2011.05-2
- Filter provides.

* Tue May 17 2011 Xavier Bachelot <xavier@bachelot.org> 2011.05-1
- Spec clean up.
- Add a BR: on sombok-devel.

* Mon May 02 2011 Xavier Bachelot <xavier@bachelot.org> 2011.04.26-1
- Specfile autogenerated by cpanspec 1.78.
