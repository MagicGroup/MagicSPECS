# Generated from dotenv-0.7.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name dotenv

Name: rubygem-%{gem_name}
Version: 0.8.0
Release: 5%{?dist}
Summary: Loads environment variables from `.env`
Group: Development/Languages
License: MIT
URL: https://github.com/bkeepers/dotenv
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygem(rspec)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Loads environment variables from `.env`.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Changelog.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/%{gem_name}-rails.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.8.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.0-4
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 09 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 0.8.0-2
- Fix gemspec declaration

* Fri Aug 09 2013 Axilleas Pipinellis - 0.8.0-1
- Version bump

* Tue May 14 2013 Anuj More - 0.7.0-1
- Initial package
