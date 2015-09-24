%global gem_name just_paginate

Name: rubygem-%{gem_name}
Version: 0.2.2
Release: 5%{?dist}
Summary: Paginating collections of things for the web
Group: Development/Languages
License: MIT
URL: https://gitorious.org/gitorious/just_paginate
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Framework-agnostic support for paginating collections of things, and linking
to paginated things in your webpage


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

# Remove dependency on bundler
sed -e '\|require "bundler/setup"|d' -i test/test_helper.rb

# Remove developer-only files.
for f in .gitignore Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove extra gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -I'lib:test' test/just_paginate_test.rb
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.2-3
- Update %%check to work with Minitest 5
- Remove Gemfile, Rakefile and .gitignore during %%prep

* Mon Nov 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.2-2
- Exclude the Gemfile, Rakefile, and tests from the binary package

* Thu Sep 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.2-1
- Update to 0.2.2

* Thu Sep 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.1-1
- Initial package
