# Generated from fog-aws-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-aws

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 2%{?dist}
Summary: Module for the 'fog' gem to support Amazon Web Services
Group: Development/Languages
License: MIT
URL: http://github.com/fog/fog-aws
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-xml)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(ipaddress)
BuildRequires: rubygem(shindo)
BuildArch: noarch

%description
This library can be used as a module for `fog` or as standalone provider
to use the Amazon Web Services in applications.


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

# Remove Mac specific files.
# https://github.com/fog/fog-aws/pull/68
find %{buildroot}%{gem_instdir} -name .DS\* | xargs rm

# Remove executable bits.
# https://github.com/fog/fog-aws/pull/69
find %{buildroot}%{gem_libdir} -name \*.rb -executable | xargs chmod a-x



%check
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i '/Bundler/ s/^/#/' tests/helper.rb

FOG_MOCK=true shindo
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.md
%exclude %{gem_instdir}/fog-aws.gemspec
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
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Vít Ondruch <vondruch@redhat.com> - 0.1.1-1
- Initial package
