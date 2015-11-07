# Generated from fog-core-1.22.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fog-core

Name: rubygem-%{gem_name}
Version: 1.29.0
Release: 4%{?dist}
Summary: Shared classes and tests for fog providers and services
Group: Development/Languages
License: MIT
URL: https://github.com/fog/fog-core
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(excon)
BuildRequires: rubygem(formatador)
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(minitest-stub-const)
BuildArch: noarch

%description
Shared classes and tests for fog providers and services.


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
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ispec -e 'Dir.glob "./spec/**/*_spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUT*
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/changelog.md
%{gem_instdir}/fog-core.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tests

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.29.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.29.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Vít Ondruch <vondruch@redhat.com> - 1.29.0-1
- Update to fog-core 1.29.0.

* Tue Jan 06 2015 Brett Lentz <blentz@redhat.com> - 1.27.2-1
- upstream release 1.27.2

* Mon Sep 29 2014 Brett Lentz <blentz@redhat.com> - 1.24.0-1
- upstream release 1.24.0

* Tue Jul 29 2014 Brett Lentz <blentz@redhat.com> - 1.23.0-1
- upstream release 1.23.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Vít Ondruch <vondruch@redhat.com> - 1.22.0-1
- Initial package
