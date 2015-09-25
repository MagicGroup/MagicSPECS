# Generated from audited-activerecord-3.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name audited-activerecord

Name: rubygem-%{gem_name}
Version: 4.2.0
Release: 2%{?dist}
Summary: Log all changes to your ActiveRecord models
Group: Development/Languages
License: MIT
URL: https://github.com/collectiveidea/audited
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Hopefully the tests will be included in the gem in the future.
# https://github.com/collectiveidea/audited/pull/125
#
# git clone https://github.com/collectiveidea/audited.git && cd audited && git checkout v4.2.0
# tar czvf audited-activerecord-4.2.0-tests.tgz spec/audited/adapters/active_record \
#   spec/rails_app spec/support/active_record spec/*.rb test
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(audited) = 4.2.0
BuildRequires: rubygem(actionmailer)
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(protected_attributes)
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
Log all changes to your ActiveRecord models.


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
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

rspec spec
ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.2.0-2
- 为 Magic 3.0 重建

* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 4.2.0-1
- Update to audited-activerecord 4.2.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Vít Ondruch <vondruch@redhat.com> - 4.0.0-1
- Update to audited-activerecord 4.0.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.0-1
- Initial package
