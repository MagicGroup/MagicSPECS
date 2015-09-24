%global gem_name middleware

Name: rubygem-%{gem_name}
Version: 0.1.0
Release: 3%{?dist}
Summary: Generalized implementation of the middleware abstraction for Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/mitchellh/middleware
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch to fix the test suite, cherry-picked from upstream's master Git branch.
# Not released in 0.1.0.
Patch0: rubygem-middleware-0.1.0-tests.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Generalized implementation of the middleware abstraction for Ruby.


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
for f in .gitignore .travis.yml .yardopts Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
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
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/user_guide.md
%exclude %{gem_instdir}/spec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.0-1
- Initial package
