# Generated from fog-atmos-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-atmos

Name: rubygem-%{gem_name}
Version: 0.1.0
Release: 2%{?dist}
Summary: Module for the 'fog' gem to support Atmos
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-atmos
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-xml)
BuildRequires: rubygem(shindo)
BuildArch: noarch

%description
This library can be used as a module for `fog` or as standalone provider
to use the Atmos in applications.


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




# Run the test suite
%check
pushd .%{gem_instdir}
FOG_MOCK=true shindo
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/fog-atmos.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/tests


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Vít Ondruch <vondruch@redhat.com> - 0.1.0-1
- Initial package
