%global gem_name safe_yaml
# Although there are tests
# the dependancies aren't in Fedora yet
%global enable_tests 0

Summary:       Parse YAML safely
Name:          rubygem-%{gem_name}
Version:       1.0.4
Release:       3%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://dtao.github.com/safe_yaml/
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:      ruby(release)
Requires:      ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{?enable_tests}
BuildRequires: rubygem(hashie)
BuildRequires: rubygem(heredoc_unindent)
BuildRequires: rubygem(ostruct)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(yaml)
%endif
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
The SafeYAML gem provides an alternative implementation of 
YAML.load suitable for accepting user input in Ruby applications. 
Unlike Ruby's built-in implementation of YAML.load, SafeYAML's 
version will not expose apps to arbitrary code execution exploits.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/{.rvmrc,.document,.require_paths,.gitignore,.travis.yml,.rspec,.gemtest,.yard*}
rm -rf %{buildroot}%{gem_instdir}/%{gem_name}.gemspec
rm -rf %{buildroot}%{gem_instdir}/bundle_install_all_ruby_versions.sh

%if 0%{?enable_tests}
%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd
%endif

%files
%{_bindir}/safe_yaml
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/run_specs_all_ruby_versions.sh
%{gem_instdir}/spec



%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 27 2014 Troy Dawson <tdawson@redhat.com> - 1.0.4-1
- Updated to latest release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Troy Dawson <tdawson@redhat.com> - 1.0.3-1
- Updated to version 1.0.3

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.0.1-1
- Updated to version 1.0.1

* Mon Jul 22 2013  Troy Dawson <tdawson@redhat.com> - 0.9.4-2
- Updated tests

* Wed Jul 17 2013  Troy Dawson <tdawson@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Fri Jun 14 2013  Troy Dawson <tdawson@redhat.com> - 0.9.3-1
- Initial package
