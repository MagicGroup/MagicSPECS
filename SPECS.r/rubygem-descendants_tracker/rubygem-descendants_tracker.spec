%global gem_name descendants_tracker

Name: rubygem-%{gem_name}
Version: 0.0.4
Release: 6%{?dist}
Summary: Module that adds descendant tracking to a class
Group: Development/Languages
License: MIT
URL: https://github.com/dkubb/descendants_tracker
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(thread_safe)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Module that adds descendant tracking to a class.


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
sed -e "/it_should_behave_like/d" -i spec/unit/descendants_tracker/descendants_spec.rb
sed -e "/it_should_behave_like/d" -i spec/unit/descendants_tracker/add_descendant_spec.rb

# Remove developer-only files.
for f in Gemfile Gemfile.devtools Guardfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unecessary gemspec
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
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
# exclude developer-only files
%exclude %{gem_instdir}/config

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
# Currently the TODO file is empty. Don't ship it.
%exclude %doc %{gem_instdir}/TODO
%exclude %{gem_instdir}/spec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.0.4-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.4-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.0.4-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.4-1
- Update to 0.0.4
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Nov 01 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.3-2
- Updates for Fedora package review request (RHBZ #1018004)
- Remove developer-only files during %%prep
- Exclude test suite from binary RPMs
- Move README to main package

* Thu Oct 10 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.3-1
- Update to 0.0.3

* Sat Oct 05 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.2-1.20131005git9ab291c
- Initial package
