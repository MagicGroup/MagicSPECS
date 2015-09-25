%global gem_name settingslogic

Name:           rubygem-%{gem_name}
Version:        2.0.9
Release:        6%{?dist}
Summary:        Simple settings solution for Ruby

Group:          Development/Languages
License:        MIT
URL:            https://github.com/binarylogic/settingslogic
Source0:        http://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch:      noarch
# to avoid jruby
BuildRequires:  ruby
BuildRequires:  rubygems-devel
# old :should syntax
BuildRequires:  rubygem(rspec) < 3

%description
Settingslogic is a simple configuration and settings solution that uses an ERB
enabled YAML file. Settingslogic works with Rails, Sinatra, or any Ruby
project.


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


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
rspec2 -Ilib spec
popd


%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Gemfile.lock
%exclude %{gem_instdir}/Rakefile
%{gem_spec}


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.9-6
- 为 Magic 3.0 重建

* Fri Jun 19 2015 František Dvořák <valtri@civ.zcu.cz> - 2.0.9-5
- Workaround jruby
- Cleanups
- Not compatible with rspec 3 (for Fedora 23)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 28 2014 František Dvořák <valtri@civ.zcu.cz> - 2.0.9-3
- Added README.rdoc
- Move EPEL and Fedora <= 20 changes to the according branches

* Sun Jul 27 2014 František Dvořák <valtri@civ.zcu.cz> - 2.0.9-2
- Update BR/R for EPEL and Fedora <= 20
- Remove development files before build
- Run tests inside %%{gem_instdir}

* Sun Mar 16 2014 František Dvořák <valtri@civ.zcu.cz> - 2.0.9-1
- Initial package
