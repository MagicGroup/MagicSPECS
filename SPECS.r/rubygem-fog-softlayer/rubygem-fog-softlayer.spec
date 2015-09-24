# Generated from fog-softlayer-0.3.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-softlayer

Name: rubygem-%{gem_name}
Version: 0.4.1
Release: 2%{?dist}
Summary: Module for the 'fog' gem to support SoftLayer Cloud
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-softlayer
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Workaround test suite errors.
# https://github.com/fog/fog-softlayer/commit/c9bfa7698fc2036cb7ca6b3d7775199429076768
patch0: rubygem-fog-softlayer-0.4.1-Update-server-model-so-the-build-isnt-broken.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(shindo)
BuildArch: noarch

%description
This library can be used as a module for `fog` or as standalone provider to
use the SoftLayer Cloud in applications.


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

%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
pushd .%{gem_instdir}
# Ignore code coverage.
sed -i "/require 'simplecov'/ s/^/#/" tests/helper.rb

FOG_MOCK=true shindont
ruby -Ilib -e 'Dir.glob "./spec/**/*_spec.rb", &method(:require)'
popd

%files
%license %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs
%doc %{gem_instdir}/examples
%{gem_instdir}/fog-softlayer.gemspec
%{gem_instdir}/gemfiles
%{gem_instdir}/spec
%{gem_instdir}/tests

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Vít Ondruch <vondruch@redhat.com> - 0.4.1-1
- Update to fog-softlayer 0.4.1.

* Tue Jan 06 2015 Brett Lentz <blentz@redhat.com> - 0.3.26-1
- New upstream release

* Mon Sep 29 2014 Brett Lentz <blentz@redhat.com> - 0.3.18-1
- New upstream release

* Thu Jul 31 2014 Vít Ondruch <vondruch@redhat.com> - 0.3.11-1
- Initial package
