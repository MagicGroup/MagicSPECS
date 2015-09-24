%global gem_name jmespath

%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global use_tests 0
%else
%global use_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        1.0.2
Release:        3%{?dist}
Summary:        JMESPath - Ruby Edition

Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/trevorrowe/jmespath.rb
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/trevorrowe/jmespath.rb && cd jmespath.rb
# git checkout v1.0.2
# tar -czf rubygem-jmespath-1.0.2-repo.tgz spec/ CHANGELOG.md README.md
Source1:        %{name}-%{version}-repo.tgz
# incompatibility with multi_json <= 1.8 (all unit tests OK, one compliance
# test failing)
# (not intended for upstream)
Patch0:         jmespath-compliance.patch

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?use_tests}
BuildRequires:  rubygem(rspec) >= 3
BuildRequires:  rubygem(rspec) < 4
BuildRequires:  rubygem(multi_json) >= 1.0
BuildRequires:  rubygem(multi_json) < 2
%endif
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Requires:       rubygem(multi_json) >= 1.0
Requires:       rubygem(multi_json) < 2
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Implements JMESPath for Ruby.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a 1
%patch0 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

cp -a CHANGELOG.md README.md %{buildroot}%{gem_instdir}/


%check
%if 0%{?use_tests}
cp -pr spec/ ./%{gem_instdir}
pushd .%{gem_instdir}
# simplecov not really needed
sed -i spec/compliance_spec.rb spec/spec_helper.rb -e '/simplecov\|SimpleCov/d'
rspec -Ilib spec
popd
%endif


%files
%dir %{gem_instdir}/
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 František Dvořák <valtri@civ.zcu.cz> - 1.0.2-2
- Removed rubygem(simplecov) BR
- Cleanups

* Fri Dec 05 2014 František Dvořák <valtri@civ.zcu.cz> - 1.0.2-1
- Initial package
