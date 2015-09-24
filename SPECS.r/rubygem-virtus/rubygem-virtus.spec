%global gem_name virtus

Name: rubygem-%{gem_name}
Version: 1.0.5
Release: 1%{?dist}
Summary: Attributes on Steroids for Plain Old Ruby Objects
Group: Development/Languages
License: MIT
URL: https://github.com/solnic/virtus
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(descendants_tracker) < 1
Requires: rubygem(descendants_tracker) >= 0.0.3
Requires: rubygem(equalizer) < 1
Requires: rubygem(equalizer) >= 0.0.9
Requires: rubygem(coercible) => 1.0
Requires: rubygem(coercible) < 2
Requires: rubygem(axiom-types) => 0.1
Requires: rubygem(axiom-types) < 1
Requires: rubygem(inflecto)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(descendants_tracker) => 0.0.3
BuildRequires: rubygem(descendants_tracker) < 1
BuildRequires: rubygem(equalizer) => 0.0.9
BuildRequires: rubygem(equalizer) < 1
BuildRequires: rubygem(coercible) => 1.0
BuildRequires: rubygem(coercible) < 2
BuildRequires: rubygem(axiom-types) => 0.1
BuildRequires: rubygem(axiom-types) < 1
BuildRequires: rubygem(inflecto)
BuildRequires: rubygem(bogus)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Attributes on Steroids for Plain Old Ruby Objects.


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
for f in .gitignore .pelusa.yml .rspec .ruby-gemset .ruby-version .travis.yml \
.yardopts Gemfile Guardfile Rakefile; do
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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Changelog.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/TODO.md
%doc %{gem_instdir}/CONTRIBUTING.md
%exclude %{gem_instdir}/config
%exclude %{gem_instdir}/spec


%changelog
* Wed Mar 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.5-1
- Update to latest upstream version (RHBZ #1203258)

* Sun Jan 04 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.4-1
- Update to latest upstream version (RHBZ #1178430)

* Wed Dec 17 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-3
- rspec-its is now available (RHBZ #1168743). Re-enable tests during %%check.

* Sat Nov 29 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-2
- Simplify %%check section

* Sat Nov 29 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-1
- Update to latest upstream version (RHBZ #1124269)
- Use %%license macro for LICENSE
- Unconditionally pass tests (rspec 3 does not have "its" available)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.2-1
- Update to latest upstream version (RHBZ #1076588)

* Mon Feb 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-4
- Adjust comments to reflect that activerecord-nulldb-adapter is now in Fedora
  and bogus is the latest missing dependency for the test suite.
- Adjust axiom-types dependency to allow latest version in Rawhide.

* Wed Feb 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-3
- Adjust comments to reflect that dependor is now in Fedora and
  activerecord-nulldb-adapter is the latest missing dependency for the bogus
  gem.

* Tue Dec 10 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-2
- Adjust coercible version dependency specification to match upstream gemspec

* Tue Dec 10 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-1
- Initial package
