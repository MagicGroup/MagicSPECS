%global gem_name nenv

# tests require rspec >= 3.1
%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global with_tests 0
%else
%global with_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        0.2.0
Release:        5%{?dist}
Summary:        Convenience wrapper for Ruby's ENV

Group:          Development/Languages
License:        MIT
URL:            https://github.com/e2/nenv
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/e2/nenv && cd nenv
# git checkout v0.2.0
# tar -czf rubygem-nenv-0.2.0-specs.tgz spec/
Source1:        %{name}-%{version}-specs.tgz

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?with_tests}
BuildRequires:  rubygem(coveralls)
BuildRequires:  rubygem(rspec) => 3.1
BuildRequires:  rubygem(rspec) < 4
%endif
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Using ENV is like using raw SQL statements in your code. We all know how that
ends...


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
%if 0%{?with_tests}
cp -pr spec/ .%{gem_instdir}
pushd .%{gem_instdir}
rspec -r spec_helper
rm -rf spec
popd
%endif


%files
%dir %{gem_instdir}/
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}/


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.2.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 07 2015 František Dvořák <valtri@civ.zcu.cz> - 0.2.0-2
- Move README.md to the main package
- EPEL support

* Mon Mar 09 2015 František Dvořák <valtri@civ.zcu.cz> - 0.2.0-1
- Initial package
