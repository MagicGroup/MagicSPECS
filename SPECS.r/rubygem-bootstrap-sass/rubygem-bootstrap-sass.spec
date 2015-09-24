# Generated from bootstrap-sass-2.3.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bootstrap-sass

Name: rubygem-%{gem_name}
Version: 2.3.2.2
Release: 4%{?dist}
Summary: Twitter's Bootstrap, converted to Sass and ready to drop into Rails or Compass
Group: Development/Languages
# All source code has the same license as Twitter's Bootstrap
# which is ASLv2.0.
# The license of Glyphicons (CC BF 3.0) is not included.
#
# CC BY 3.0: http://creativecommons.org/licenses/by/3.0/ 
License: ASL 2.0
URL: http://github.com/thomas-mcdonald/bootstrap-sass
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(sass) => 3.2
Requires: rubygem(sass) < 4
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(sass)
BuildRequires: rubygem(test-unit)
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Twitter's Bootstrap, converted to Sass and ready to drop into Rails or Compass

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

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -rtest-unit -e 'Test::Unit::AutoRunner.run(true)' -Ilib test
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%{gem_instdir}/vendor/
%{gem_instdir}/templates/
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/test/
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/asseturl.patch
%{gem_instdir}/update-bootstrap.sh
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Mon Jun 22 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.3.2.2-4
- Fix test-unit usage for F22+

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 02 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 2.3.2.2-1
- Update to 2.3.2.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 16 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 2.3.2.1-1
- Initial package
