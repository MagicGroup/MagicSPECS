%global gem_name json_spec

Name:           rubygem-%{gem_name}
Version:        1.1.4
Release:        4%{?dist}
Summary:        Easily handle JSON in RSpec and Cucumber

Group:          Development/Languages
License:        MIT
URL:            https://github.com/collectiveidea/json_spec
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(cucumber)
BuildRequires:  rubygem(multi_json)
BuildRequires:  rubygem(rspec)

%description
RSpec matchers and Cucumber steps for testing JSON content.


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

# Remove developer-only files
for f in .gitignore .travis.yml Gemfile Rakefile gemfiles/*; do
  rm $f
  sed -i "s|\"$f\",\?||g" %{gem_name}.gemspec
done


%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
rspec -Ilib spec
cucumber --tags ~@fail
popd


%files
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/features/
%{gem_instdir}/spec/


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.4-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 13 2014 František Dvořák <valtri@civ.zcu.cz> - 1.1.4-1
- Update to 1.1.4
- Distribute testsuite in -doc subpackage

* Tue Aug 5 2014 František Dvořák <valtri@civ.zcu.cz> - 1.1.2-1
- Initial package
