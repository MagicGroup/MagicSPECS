# Generated from fog-sakuracloud-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-sakuracloud

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 2%{?dist}
Summary: Module for the 'fog' gem to support Sakura no Cloud
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-sakuracloud
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(shindo)
BuildArch: noarch

%description
Module for the 'fog' gem to support Sakura no Cloud.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
FOG_MOCK=true CI=true shindo
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.txt
%exclude %{gem_instdir}/fog-sakuracloud.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/tests/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
