%global gem_name shellany

# rspec 3 required
%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global use_tests 0
%else
%global use_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        0.0.1
Release:        3%{?dist}
Summary:        Simple, somewhat portable command capturing

Group:          Development/Languages
License:        MIT
URL:            https://github.com/guard/shellany
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?use_tests}
BuildRequires:  rubygem(rspec) >= 3.1
BuildRequires:  rubygem(rspec) < 4
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(rubygems)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
MRI+JRuby compatible command output capturing.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

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
%if 0%{?use_tests}
pushd .%{gem_instdir}
rspec -Ilib --require shellany spec
popd
%endif


%files
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}/
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_instdir}/spec/
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/shellany.gemspec
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}/


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.0.1-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.1-2
- 为 Magic 3.0 重建

* Tue Aug 11 2015 František Dvořák <valtri@civ.zcu.cz> - 0.0.1-1
- Initial package
