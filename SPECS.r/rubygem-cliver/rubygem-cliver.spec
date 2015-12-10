# Generated from cliver-0.3.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cliver

Name: rubygem-%{gem_name}
Version: 0.3.2
Release: 6%{?dist}
Summary: Cross-platform version constraints for cli tools
Group: Development/Languages
License: MIT
URL: https://www.github.com/yaauie/cliver
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec) < 3.0
BuildArch: noarch

%if 0%{?fedora} <= 20
Requires: ruby(release)
Requires: ruby(rubygems) 
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Assertions for command-line dependencies.


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
rspec2 -Ilib spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.githooks/*
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.2-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.2-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.2-4
- 为 Magic 3.0 重建

* Thu Aug 06 2015 Josef Stribny <jstribny@redhat.com> - 0.3.2-3
- Fix FTBFS: Run tests with RSpec2 bin

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.3.2-1
- Initial package
