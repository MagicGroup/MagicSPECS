%global gem_name ice_nine

Name: rubygem-%{gem_name}
Version: 0.11.1
Release: 5%{?dist}
Summary: Deep Freeze Ruby Objects
Group: Development/Languages
License: MIT
URL: https://github.com/dkubb/ice_nine
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Deep Freeze Ruby Objects.


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

# Remove requirement on "devtools" (not yet packaged).
# Note that this is not the "devtools" on rubygems.org, but the gem at
# https://github.com/rom-rb/devtools. Upstream will rename this to "develry".
# https://github.com/rom-rb/devtools/pull/39
sed -e "\|require 'devtools/spec_helper'|d" -i spec/spec_helper.rb

# devtools/spec_helper loads the shared examples. Since we've removed devtools
# above, we must load the examples ourselves.
echo "
Dir[File.expand_path('../shared/*.rb', __FILE__)].each { |file| require file }
" >> spec/spec_helper.rb

# Remove developer-only files.
for f in .gitignore .pelusa.yml .rspec .rubocop.yml .ruby-gemset \
  .travis.yml .yardopts Gemfile Gemfile.devtools Guardfile Rakefile; do
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
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/TODO
%exclude %{gem_instdir}/benchmarks
%exclude %{gem_instdir}/config
%exclude %{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.11.1-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.11.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.11.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Dec 06 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.11.1-1
- Update to ice_nine 0.11.1 (RHBZ #1171087)
- Re-enable tests
- Use %%license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.11.0-1
- Update to latest upstream release
- Remove dot-files during %%prep
- Tests are now failing, so skip test result during %%check. Issue filed
  upstream at GitHub.

* Tue Nov 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.10.0-2
- Adjust .rspec to work on F19

* Fri Nov 01 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.10.0-1
- Initial package
