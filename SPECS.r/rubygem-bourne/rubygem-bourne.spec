%global gem_name bourne

Name: rubygem-%{gem_name}
Version: 1.6.0
Release: 4%{?dist}
Summary: Adds test spies to mocha
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/bourne
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Minitest 5 support
# A variation of this patch has been submitted upstream at
# https://github.com/thoughtbot/bourne/pull/33
Patch0: rubygem-bourne-1.5.0-minitest.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(mocha) < 2
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest) >= 5
BuildRequires: rubygem(mocha) < 2
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Extends mocha to allow detailed tracking and querying of
stub and mock invocations. Allows test spies using the have_received rspec
matcher and assert_received for Test::Unit. Extracted from the
jferris-mocha fork.


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

# Minitest 5 support
# https://github.com/thoughtbot/bourne/pull/33
%patch0 -p1

# Mocha 1.0 support
# https://github.com/thoughtbot/bourne/pull/32
# (We just drop the version numbers here altogether and let the packaging
# system handle the versions.)
sed -i "/mocha/{s/\(_dependency([^,]*\), .*/\1)/}" %{gem_name}.gemspec

# Remove developer-only files.
for f in .gitignore .travis.yml Gemfile Rakefile; do
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
  ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/NEWS.md
%exclude %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.6.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.6.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Nov 27 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.6.0-1
- Update to bourne 1.6.0

* Thu Jul 17 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-5
- Update for Mocha 1.0 compatibility

* Tue Jun 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-4
- Use HTTPS URL
- Remove dot files during %%prep
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Patch for Minitest 5
- Use %%license designation for LICENSE file

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 31 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.5.0-2
- Remove unnecessary comments
- Remove BR: ruby (redundant)
- Move README to main package
- Delete Gemfile and Rakefile in %%prep
- Exclude tests from binary pkgs

* Sat Jul 27 2013 ktdreyer@ktdreyer.com - 1.5.0-1
- Update to 1.5.0
