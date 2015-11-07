# Generated from net-ldap-0.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name net-ldap

Name: rubygem-%{gem_name}
Version: 0.11
Release: 4%{?dist}
Summary: Net::LDAP for Ruby implements client access LDAP protocol
Group: Development/Languages
License: MIT
URL: http://github.com/ruby-ldap/ruby-net-ldap
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
# specs need metaid gem that is not in Fedora yet
# BuildRequires: rubygem(metaid)
# BuildRequires: rubygem(rspec-core)
BuildRequires: rubygem(flexmock)
BuildRequires: rubygem(test-unit)
BuildArch: noarch
# this package obsoletes rubygem-ruby-net-ldap
Provides: rubygem-ruby-net-ldap = %{version}-%{release}
Obsoletes: rubygem-ruby-net-ldap < 0.0.4-7

%description
Net::LDAP for Ruby (also called net-ldap) implements client access for the
Lightweight Directory Access Protocol (LDAP), an IETF standard protocol for
accessing distributed directory services. Net::LDAP is written completely in
Ruby with no external dependencies. It supports most LDAP client features and
a subset of server features as well.
Net::LDAP has been tested against modern popular LDAP servers including
OpenLDAP and Active Directory. The current release is mostly compliant with
earlier versions of the IETF LDAP RFCs (2251–2256, 2829–2830, 3377, and
3771).
Our roadmap for Net::LDAP 1.0 is to gain full client compliance with
the most recent LDAP RFCs (4510–4519, plus portions of 4520–4532).


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove meaningless shebang.
# https://github.com/ruby-ldap/ruby-net-ldap/pull/200
sed -i "/#!/ d" %{buildroot}%{gem_instdir}/Rakefile

%check
pushd .%{gem_instdir}
ruby -Ilib:test -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/License.rdoc
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/Contributors.rdoc
%doc %{gem_instdir}/Hacking.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/script
%{gem_instdir}/test
%exclude %{gem_instdir}/test/support/vm/openldap/.gitignore
%{gem_instdir}/testserver

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.11-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.11-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Vít Ondruch <vondruch@redhat.com> - 0.11-1
- Update to net-ldap 0.11.

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.1-1
- Update to net-ldap 0.6.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.1-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Emanuel Rietveld <codehotter@gmail.com> - 0.3.1-1
- Updated to 0.3.1

* Tue Feb 28 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-3
- Properly obsolete rubygem-ruby-net-ldap (now really).

* Wed Feb 22 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-2
- Properly obsolete rubygem-ruby-net-ldap.

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-1
- Initial package
