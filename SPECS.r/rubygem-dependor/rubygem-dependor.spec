%global gem_name dependor

Name: rubygem-%{gem_name}
Version: 1.0.1
Release: 3%{?dist}
Summary: Simplify dependency injection in Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/psyho/dependor
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-dependor-1.0.1-optional-deps.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Dependor is not a framework for Dependency Injection, but something that
reduces duplication a little bit when doing manual dependency injection in
settings like Rails apps.


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

# Remove developer-only files.
for f in .gitignore .pelusa.yml .travis.yml \
Gemfile Gemfile.lock Guardfile Rakefile pelusa.sh; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Remove dependency on optional deps simplecov and coveralls
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.1-3
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-1
- Initial package
