%global gem_name axiom-types

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 5%{?dist}
Summary: Abstract types for logic programming
Group: Development/Languages
License: MIT
URL: https://github.com/dkubb/axiom-types
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(descendants_tracker) => 0.0.4
Requires: rubygem(ice_nine) => 0.11.0
Requires: rubygem(thread_safe) >= 0.3.1
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rspec-its)
BuildRequires: rubygem(ice_nine) => 0.11.0
BuildRequires: rubygem(descendants_tracker) => 0.0.4
BuildRequires: rubygem(thread_safe) => 0.3.1
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Define types with optional constraints for use within axiom and other
libraries.


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

# Remove requirement on "devtools" (not yet packaged).
# Note that this is not the "devtools" on rubygems.org, but the gem at
# https://github.com/rom-rb/devtools. Upstream will rename this to "develry".
# https://github.com/rom-rb/devtools/pull/39
sed -e "\|require 'devtools/spec_helper'|d" -i spec/spec_helper.rb

# Remove tests that require devtools
find spec -type f | xargs sed -e "/it_should_behave_like/d" -i

# Remove developer-only files.
for f in .gitignore .travis.yml .rspec .ruby-gemset .rubocop.yml .yardopts \
Gemfile Gemfile.devtools Guardfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# test suite uses "its", so we must load rspec-its:
# https://github.com/dkubb/axiom-types/issues/17
sed -i '1s/^/require "rspec\/its"\n/' spec/spec_helper.rb

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
# exclude developer-only files
%exclude %{gem_instdir}/config

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/TODO
%exclude %{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.1-5
- 为 Magic 3.0 重建

* Mon Jul 06 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.1-4
- require rspec-its during tests (rhbz#1239892)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.1-1
- Update to axiom-types 0.1.1 (RHBZ #1081535)
- Add minimum version requirements. The immediate problem was that we missed
  updating ice_nine to 0.11.0 in Rawhide, so axiom-type would install with yum,
  but rubygems could not load it. Adding minimum versions from gem2rpm should
  ward off similar problems in the future.
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Feb 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.0-1
- Update to axiom-types 0.1.0 (RHBZ #1055954)

* Wed Nov 20 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.5-2
- Remove developer dot-files during %%prep

* Fri Oct 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.5-1
- Initial package
