%global gem_name rspec-its

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 3%{?dist}
Summary: Provides "its" method formally part of rspec-core
Group: Development/Languages
License: MIT
URL: https://github.com/rspec/rspec-its
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rspec-core) >= 2.99.0.beta1
Requires: rubygem(rspec-expectations) >= 2.99.0.beta1
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec-core) >= 2.99.0.beta1
BuildRequires: rubygem(rspec-expectations) >= 2.99.0.beta1
# cucumber tests are non-functional during RPM build
#BuildRequires: rubygem(cucumber) => 1.3.8
#BuildRequires: rubygem(cucumber) < 1.4
#BuildRequires: rubygem(aruba) => 0.5
#BuildRequires: rubygem(aruba) < 1
BuildArch: noarch
%if 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
RSpec extension gem for attribute matching.

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
for f in .gitignore .rspec .travis.yml Gemfile Rakefile \
script/test_all cucumber.yml; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
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
  # cucumber tests are non-functional during RPM build
  #cucumber -Ilib features/*.feature
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%doc %{gem_instdir}/Changelog.md
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/cucumber.yml
%exclude %{gem_instdir}/features
%exclude %{gem_instdir}/spec


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- Update to rspec-its 1.1.0 (RHBZ #1168743)
- Correct %%license file (RHBZ #1168743)
- Remove f19 and f20 dist conditionals, since we'll only ship on f22 and later.
  (RHBZ #1168743)

* Thu Nov 27 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-2
- Initial package
