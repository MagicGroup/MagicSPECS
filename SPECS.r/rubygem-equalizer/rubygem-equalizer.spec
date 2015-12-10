%global gem_name equalizer

Name: rubygem-%{gem_name}
Version: 0.0.11
Release: 5%{?dist}
Summary: Module to define equality, equivalence and inspection methods
Group: Development/Languages
License: MIT
URL: https://github.com/dkubb/equalizer
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Module to define equality, equivalence and inspection methods


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove developer-only files.
for f in .gitignore .rspec .rubocop.yml .ruby-gemset .ruby-version \
.travis.yml .yardstick.yml Gemfile Rakefile config/*; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
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
%doc %{gem_instdir}/CONTRIBUTING.md
%exclude %{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.0.11-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.11-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.11-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.11-1
- Update to 0.0.11 (RHBZ #1204120)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 26 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.9-1
- Update to 0.0.9

* Tue Dec 03 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.8-1
- Update to 0.0.8
- Remove dot-files during %%prep

* Tue Nov 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.7-2
- Adjust .rspec to work on F19

* Fri Oct 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.7-1
- Initial package
