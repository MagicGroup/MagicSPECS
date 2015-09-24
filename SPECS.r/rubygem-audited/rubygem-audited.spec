# Generated from audited-3.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name audited

Name: rubygem-%{gem_name}
Version: 4.2.0
Release: 1%{?dist}
Summary: Log all changes to your models
Group: Development/Languages
License: MIT
URL: https://github.com/collectiveidea/audited
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
Log all changes to your models.


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


%check
# Unfortunatelly, there doesn't seems to be any test coverage of auditable gem.
# However, there are available test suites for audited's ORM adapters.


%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/.*
# audited-*.gemspec seems to be included by mistake.
# https://github.com/collectiveidea/audited/pull/124
%exclude %{gem_instdir}/audited-*.gemspec
# Seems that spec and test folders are included just by mistake.
# https://github.com/collectiveidea/audited/pull/125
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/test
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles

%changelog
* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 4.2.0-1
- Update to Audited 4.2.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Vít Ondruch <vondruch@redhat.com> - 4.0.0-1
- Update to Audited 4.0.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.0-1
- Initial package
