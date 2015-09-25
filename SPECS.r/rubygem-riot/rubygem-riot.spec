# Generated from riot-0.12.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name riot

Summary: An extremely fast, expressive, and context-driven unit-testing framework
Name: rubygem-%{gem_name}
Version: 0.12.7
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/thumblemonks/riot
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(rr) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: rubygem(rr) 
BuildRequires: rubygem(minitest) 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
An extremely fast, expressive, and context-driven unit-testing framework.
A replacement for all other testing frameworks. Protest the slow test.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Get rid of Bundler
sed -i -e '3d' test/teststrap.rb
ruby -Ilib:test -e "Dir.glob './test/core/**/*_test.rb', &method(:require)"
ruby -Ilib:test -e "Dir.glob './test/extensions/*_test.rb', &method(:require)"

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE
%exclude %{gem_instdir}/.yardopts
%exclude %{gem_instdir}/.travis.yml

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown
%doc %{gem_instdir}/CHANGELOG
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.12.7-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 0.12.7-1
- Update to riot 0.12.7

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 0.12.5-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 10 2012 Josef Stribny <jstribny@redhat.com> - 0.12.5-2
- Fixed license
- Moved .gemspec to doc subpackage
- Excluded .yardopts from the package
- Changed to testrb -Ilib:test to avoid issues with bootsrap

* Tue Dec 04 2012 Josef Stribny <jstribny@redhat.com> - 0.12.5-1
- Initial package
