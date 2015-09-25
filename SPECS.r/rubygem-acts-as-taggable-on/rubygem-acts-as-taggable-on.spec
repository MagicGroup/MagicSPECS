%global gem_name acts-as-taggable-on

Name: rubygem-%{gem_name}
Version: 3.5.0
Release: 3%{?dist}
Summary: Advanced tagging for Rails
Group: Development/Languages
License: MIT
URL: https://github.com/mbleigh/acts-as-taggable-on
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: rubygem-acts-as-taggable-on-spec-database.yml
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(activerecord) >= 3.2
Requires: rubygem(activerecord) < 5
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(activerecord) >= 3.2
BuildRequires: rubygem(activerecord) < 5
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(rspec-rails)
BuildRequires: rubygem(rspec-its)
BuildRequires: rubygem(rspec)
# barrier is not yet available in Fedora
#BuildRequires: rubygem(barrier)
BuildRequires: rubygem(database_cleaner)
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
With ActsAsTaggableOn, you can tag a single model on several contexts, such as
skills, interests, and awards. It also provides other advanced functionality.


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
for f in .gitignore .rspec .travis.yml Gemfile Guardfile \
Rakefile Appraisals; do
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
  # Set up sqlite database configuration for tests
  cp %{SOURCE1} spec/database.yml
  # The tests require rubygem-barrier which is not yet in Fedora.
  rspec -Ilib spec || :
popd

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/gemfiles
%{gem_instdir}/db

%files doc
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/UPGRADING.md
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.5.0-1
- Update to latest upstream release (RHBZ #1198108)
- Use %%license macro

* Sun Feb 15 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.4.4-1
- Update to latest upstream release (RHBZ #1192390)

* Tue Jan 13 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.4.3-1
- Update to latest upstream release (RHBZ #1180516)
- BR: rubygem-rspec-its
- Remove Fedora 19 compatibility macros

* Sat Dec 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.4.2-2
- Add missing sources

* Sat Dec 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.4.2-1
- Update to latest upstream release (RHBZ #1101237)
- Drop unnecessary ammeter patch

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.3-1
- Update to latest upstream release (RHBZ #1100755)

* Fri May 16 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.2.1-1
- Update to latest upstream release (RHBZ #1083983)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Unconditionally pass tests during %%check, since we don't yet have the
  rubygem-rspec-its package available in Fedora.

* Fri Mar 14 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.2-1
- Update to latest upstream release (RHBZ #1076583)

* Thu Jan 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.1-1
- Update to latest upstream release (RHBZ #1047836)
- Remove dot-files during %%prep
- Submit ammeter patch upstream

* Thu Oct 03 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.4.1-2
- Remove BR: ruby (this is redundant with the other BRs)
- Do not ship Gemfile, Guardfile, Rakefile, and Appraisals files
- Move README to main package

* Mon Jul 29 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.4.1-1
- Update to 2.4.1, with gem2rpm 0.9.2

* Sat Aug 04 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.3.3-1
- Initial package, created by gem2rpm 0.8.1
