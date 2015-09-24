%global gem_name bogus

Name: rubygem-%{gem_name}
Version: 0.1.6
Release: 2%{?dist}
Summary: Create fakes to make your isolated unit tests reliable
Group: Development/Languages
License: MIT
URL: https://github.com/psyho/bogus
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(dependor) >= 0.0.4
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(dependor) >= 0.0.4
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(activerecord-nulldb-adapter)
BuildRequires: rubygem(simplecov)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Decreases the need to write integration tests by ensuring that the things you
stub or mock actually exist.


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
for f in .gitignore .pelusa.yml .rspec .travis.yml Gemfile Guardfile \
Guardfile.cucumber pelusa.sh Rakefile rbs.sh; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
  # TODO: cucumber feature tests
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/license.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/features

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 04 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.6-1
- Update to latest upstream release (RHBZ #1178431)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.5-1
- Update to bogus 0.1.5

* Mon Feb 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-2
- Enable rspec tests, now that rubygem-activerecord-nulldb-adapter is in
  Fedora

* Mon Dec 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-1
- Initial package
