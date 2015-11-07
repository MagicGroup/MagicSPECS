# Generated from fog-brightbox-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-brightbox

Name: rubygem-%{gem_name}
Version: 0.7.1
Release: 4%{?dist}
Summary: Module for `fog` or standalone provider to use the Brightbox Cloud
Group: Development/Languages
License: MIT
URL: https://github.com/brightbox/fog-brightbox
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix "uninitialized constant {Fog::Brightbox::ModelHelper,
# StockStorageResponses}" issues.
# https://github.com/fog/fog-brightbox/pull/22
Patch0: rubygem-fog-brightbox-0.7.1-Fix-specs.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-json)
BuildRequires: rubygem(inflecto)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(webmock)
BuildArch: noarch

%description
Module for the 'fog' gem to support Brightbox Cloud.


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
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
ruby -Ilib:spec -e 'Dir.glob "./spec/**/*_spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/fog-brightbox.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/gemfiles
%{gem_instdir}/spec


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.7.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.1-1
- Update to fog-brightbox 0.7.1.

* Fri May 23 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.2-1
- Initial package
