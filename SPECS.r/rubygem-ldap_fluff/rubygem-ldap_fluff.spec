# Generated from ldap_fluff-0.1.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ldap_fluff

Summary: LDAP querying tools for Active Directory, FreeIPA and POSIX-style
Name: rubygem-%{gem_name}
Version: 0.3.7
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+
URL: https://github.com/theforeman/ldap_fluff
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(net-ldap) >= 0.8.0
BuildArch: noarch

%description
Simple library for binding & group querying on top of various LDAP
implementations


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/test

%changelog
* Mon Jul 27 2015 Dominic Cleal <dcleal@redhat.com> - 0.3.6-1
- Update to ldap_fluff 0.3.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Dominic Cleal <dcleal@redhat.com> - 0.3.5-1
- Update to ldap_fluff 0.3.5

* Mon Nov 10 2014 Dominic Cleal <dcleal@redhat.com> - 0.3.3-1
- Update to ldap_fluff 0.3.3

* Wed Oct 15 2014 Dominic Cleal <dcleal@redhat.com> - 0.3.2-1
- Update to ldap_fluff 0.3.2

* Thu Aug 28 2014 Dominic Cleal <dcleal@redhat.com> - 0.3.1-1
- Update to ldap_fluff 0.3.1
- Update upstream URLs and descriptions

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.2.5-2
- Relax ActiveSupport dependency.

* Fri Jun 13 2014 Vít Ondruch <vondruch@redhat.com> - 0.2.5-1
- Update to ldap_fluff 0.2.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.3-1
- Initial package
