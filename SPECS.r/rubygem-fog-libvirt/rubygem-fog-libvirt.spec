# Generated from fog-libvirt-0.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-libvirt

Name: rubygem-%{gem_name}
Version: 0.0.2
Release: 5%{?dist}
Summary: Module for the 'fog' gem to support libvirt
Group: Development/Languages
License: MIT
URL: http://github.com/fog/fog-libvirt
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(ruby-libvirt)
BuildRequires: rubygem(shindo) => 0.3.4
BuildRequires: rubygem(shindo) < 0.4
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha) => 1.1.0
BuildRequires: rubygem(fog-core)
BuildRequires: rubygem(fog-xml)
BuildRequires: rubygem(fog-json)
BuildRequires: libvirt-devel
BuildArch: noarch

%description
This library can be used as a module for 'fog' or as standalone libvirt
provider.


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
set -e
FOG_MOCK=true shindont -Ilib tests
ruby -I.:lib:minitests -e "Dir.glob 'minitests/**/*_test.rb', &method(:require)"
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/fog-libvirt.gemspec
%{gem_instdir}/tests
%{gem_instdir}/minitests

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.0.2-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.2-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Josef Stribny <jstribny@redhat.com> - 0.0.2-2
- Drop libvirt requirement, it should be pulled in via ruby-libvirt

* Mon Jun 29 2015 Josef Stribny <jstribny@redhat.com> - 0.0.2-1
- Update to 0.0.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Josef Stribny <jstribny@redhat.com> - 0.0.1-1
- Initial package
