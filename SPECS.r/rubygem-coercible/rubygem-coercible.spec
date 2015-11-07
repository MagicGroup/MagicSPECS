%global gem_name coercible

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 5%{?dist}
Summary: Powerful, flexible and configurable coercion library
Group: Development/Languages
License: MIT
URL: https://github.com/solnic/coercible
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(descendants_tracker) => 0.0.1
Requires: rubygem(descendants_tracker) < 0.1
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(descendants_tracker) => 0.0.1
BuildRequires: rubygem(descendants_tracker) < 0.1
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Powerful, flexible and configurable coercion library.


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
for f in .gitignore .rspec .travis.yml Gemfile Gemfile.devtools \
Guardfile Rakefile; do
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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Changelog.md
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/config

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.0-4
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.0-2
- Remove dependency on backports gem to align with upstream gemspec

* Tue Dec 10 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.0-1
- Update to coercible 1.0.0
- Remove dot-files during %%prep

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.0-1
- Initial package
