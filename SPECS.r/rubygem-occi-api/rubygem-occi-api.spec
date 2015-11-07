%global gem_name occi-api

Name:           rubygem-%{gem_name}
Version:        4.3.2
Release:        3%{?dist}
Summary:        OCCI development library providing a high-level client API

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/EGI-FCTF/rOCCI-api
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  ruby(release) >= 1.9.3
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(httparty)
BuildRequires:  rubygem(occi-core) => 4.3.2
BuildRequires:  rubygem(occi-core) < 5
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(vcr)
# upstream: webmock ~> 1.9.3
BuildRequires:  rubygem(webmock) >= 1.9.0
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release) >= 1.9.3
Requires:       ruby(rubygems)
Requires:       rubygem(occi-core) => 4.3.2
Requires:       rubygem(occi-core) < 5
Requires:       rubygem(httparty)
Requires:       rubygem(json)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
This gem provides ready-to-use client classes to simplify the integration of
OCCI into your application.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# relax dependencies
sed -i -e 's|\(%q<httparty>,\) \[.*\]|\1 [">= 0.10.0"]|' %{gem_name}.gemspec
sed -i -e 's|\(%q<json>,\) \[.*\]|\1 [">= 1.7.7"]|' %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd


%files
%doc %{gem_instdir}/AUTHORS
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%{gem_libdir}/
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/.yardopts
%exclude %{gem_instdir}/spec/
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_spec}

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/examples/
%doc %{gem_instdir}/README.md


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.3.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.3.2-2
- 为 Magic 3.0 重建

* Wed Jun 17 2015 František Dvořák <valtri@civ.zcu.cz> - 4.3.2-1
- Update to 4.3.2 (#1232529)

* Mon Dec 01 2014 František Dvořák <valtri@civ.zcu.cz> - 4.3.1-1
- Update to 4.3.1
- The license file marked by %%license macro
- Removed tests and build files

* Sun Sep 14 2014 František Dvořák <valtri@civ.zcu.cz> - 4.2.6-1
- Initial package
