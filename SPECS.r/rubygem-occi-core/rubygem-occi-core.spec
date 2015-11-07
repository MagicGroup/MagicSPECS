%global gem_name occi-core

Name:           rubygem-%{gem_name}
Version:        4.3.2
Release:        4%{?dist}
Summary:        OCCI toolkit

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/EGI-FCTF/rOCCI-core
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  ruby(release) >= 1.9.3
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(activesupport) => 4.0.0
BuildRequires:  rubygem(hashie)
BuildRequires:  rubygem(json_spec)
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(settingslogic) >= 2.0.9
BuildRequires:  rubygem(uuidtools) >= 2.1.3
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release) >= 1.9.3
Requires:       ruby(rubygems)
Requires:       rubygem(activesupport) => 4.0.0
Requires:       rubygem(hashie)
Requires:       rubygem(json)
Requires:       rubygem(settingslogic) >= 2.0.9
Requires:       rubygem(uuidtools) >= 2.1.3
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
OCCI is a collection of classes to simplify the implementation of the Open
Cloud Computing API in Ruby.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# relax dependencies
sed -i -e 's|\(%q<hashie>,\) \[.*\]|\1 [">= 2.0.0"]|' %{gem_name}.gemspec
sed -i -e 's|\(%q<json>,\) \[.*\]|\1 [">= 1.7.7"]|' %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
# UTF-8 characters in test scripts
# https://github.com/EGI-FCTF/rOCCI-core/issues/20
pushd .%{gem_instdir}
LANG=cs_CZ.UTF-8 rspec -Ilib spec
popd


%files
%doc %{gem_instdir}/AUTHORS
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/config
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.3.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.3.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 01 2014 František Dvořák <valtri@civ.zcu.cz> - 4.3.2-1
- Update to 4.3.2
- Removed rails >= 4.1 compatibility patch
- The license file marked by %%license macro
- Removed tests and build files

* Thu Sep 4 2014 František Dvořák <valtri@civ.zcu.cz> - 4.2.16-1
- Initial package
