%global gem_name cucumber-rails

Name: rubygem-%{gem_name}
Version: 1.4.2
Release: 1%{?dist}
Summary: Cucumber Generators and Runtime for Rails
Group: Development/Languages
License: MIT
URL: http://cukes.info
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(ammeter)
# BuildRequires: %%{_bindir}/cucumber
# BuildRequires: rubygem(aruba)
# BuildRequires: rubygem(rails)
BuildArch: noarch

%description
Cucumber Generator and Runtime for Rails.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

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
# The fixture_support can be dropped as soon as new Ammeter is released:
# https://github.com/alexrothenberg/ammeter/issues/48
rspec -rrspec/rails/fixture_support spec

# Cucumber test suite runs just out of git repo:
# https://github.com/cucumber/cucumber-rails/issues/219
# sed -i "/require 'bundler\/setup'/d" features/support/env.rb
# cucumber
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/config/.gitignore
%license %{gem_instdir}/LICENSE
%{gem_instdir}/config
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/dev_tasks
%{gem_instdir}/features
%{gem_instdir}/gemfiles
%{gem_instdir}/Appraisals
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Wed Sep 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.4.2-1
- Update to cucumber-rails 1.4.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Josef Stribny <jstribny@redhat.com> - 1.3.0-5
- Fix: require rubygem-nokogiri and rubygem-capybara for runtime

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.0-1
- Update to cucumber-rails 1.3.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.2-9
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.2-1
- Update to latest upstream release

* Fri Jul 08 2011 Chris Lalancette <clalance@redhat.com> - 0.3.2-7
- Remove the check section as it doesn't work currently
- Re-arrange the spec to install the gem during prep

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.2-5
- Fixed wrong email in changelog
- Fixed version in cucumber dependency
- Fixed attributes on doc subpackage

* Mon Oct 11 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.2-4
- Moved tests and documentation to doc subpackage
- Fixed licence tag
- Removed unused macros
- Fixed version dependencies

* Sat Oct 02 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.2-3
- Added nokogiri gem to dependencies

* Sat Oct 02 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.2-2
- Added missing cucumber dependency for build

* Fri Oct 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.3.2-1
- Initial package
