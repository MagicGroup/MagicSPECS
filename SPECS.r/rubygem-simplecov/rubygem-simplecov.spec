%global gem_name simplecov
%global rubyabi 1.9.1

Summary:       Code coverage analysis tool for Ruby 1.9
Name:          rubygem-%{gem_name}
Version:       0.10.0
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://github.com/colszowka/simplecov
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} >= 19 || 0%{?rhel} > 6
Requires:      ruby(release)
%else
Requires:      ruby(abi) >= %{rubyabi}
%endif
Requires:      ruby 
Requires:      rubygems
Requires:      rubygem(docile) => 1.1.0
Requires:      rubygem(multi_json) => 1.0
Requires:      rubygem(simplecov-html) => 0.8.0
BuildRequires: ruby 
BuildRequires: rubygems-devel 
# For tests
BuildRequires: rubygem(aruba)
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(capybara)
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(docile)
BuildRequires: rubygem(rake)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(shoulda)
BuildRequires: rubygem(simplecov-html)
BuildRequires: rubygem(test-unit)
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Code coverage for Ruby 1.9 with a powerful configuration library and automatic
merging of coverage across test suites


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

#cleanup
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.rspec
rm -f %{buildroot}%{gem_instdir}/.rubocop.yml
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -rf %{buildroot}%{gem_instdir}/.yardopts
rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm -f %{buildroot}%{gem_instdir}/Gemfile
rm -f %{buildroot}%{gem_instdir}/simplecov.gemspec
chmod 0755 %{buildroot}%{gem_instdir}/Rakefile
mv %{buildroot}%{gem_instdir}/doc %{buildroot}/%{gem_docdir}/

%check
pushd %{buildroot}%{gem_instdir}
rm -rf test/faked_project/test/
sed -i 's|Unit Tests", "some_arbitrary_command|MiniTest", "some_arbitrary_command|' test/test_command_guesser.rb
ruby -Ilib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
rm -rf %{buildroot}%{gem_instdir}/tmp
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/cucumber.yml
%{gem_instdir}/features
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%{gem_instdir}/CHANGELOG.md
%{gem_instdir}/README.md
%{gem_instdir}/CONTRIBUTING.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.0-2
- 为 Magic 3.0 重建

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 0.10.0-1
- Updated to version 0.10.0
- Changed check from testrb2 to ruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Jan Klepek <jan.klepek at, gmail.com>  - 0.8.2-4
- fix for correct EPEL7 build

* Wed Feb 05 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-3
- Updated all dependencies
- Re-enabled tests

* Wed Feb 05 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-2
- Updated simplecov-html dependency


* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 0.8.2-1
- Updated to version 0.8.2
- Update to latest ruby spec guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 0.7.1-7
- Fix to make it build/install on F19+
- Removed testing until ruby2 gems have stabilized

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-5
- Correctly declared License

* Fri Nov 30 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-4
- Removed unneeded rubygem-appraisal dependancy

* Fri Nov 30 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-3
- Use pushd and pop in the test/check section

* Thu Nov 29 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-2
- Now with tests

* Mon Nov 19 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 27 2012 Troy Dawson <tdawson@redhat.com> - 0.6.4-1
- Initial package
