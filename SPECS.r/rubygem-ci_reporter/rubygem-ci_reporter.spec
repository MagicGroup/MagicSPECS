%global gem_name ci_reporter

Summary:       Generate XML for continuous integration systems
Name:          rubygem-%{gem_name}
Version:       2.0.0
Release:       2%{dist}
License:       MIT
URL:           http://caldersphere.rubyforge.org/ci_reporter
Source0:       http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires:      ruby 
Requires:      rubygems >= 1.3.7
Requires:      rubygem(builder)
%if 0%{?fedora} >= 17
BuildRequires: rubygems-devel
%endif
BuildRequires: ruby 
BuildRequires: rubygems >= 1.3.7
# For tests
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(cucumber)
BuildRequires: rubygem(hoe)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rdoc)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rubyforge)
BuildRequires: rubygem(test-unit)
BuildArch:     noarch
Provides:      rubygem(ci_reporter) = %{version}

%description
CI::Reporter is an add-on to Test::Unit, RSpec and Cucumber that allows you to
generate XML reports of your test, spec and/or feature runs. The resulting
files can be read by a continuous integration system that understands Ant's
JUnit report XML format, thus allowing your CI system to track test/spec
successes and failures.

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

# Fix our tests, Fedoras current version
#   of test-unit (2.4.5) doesn't work with them.
sed -i -e "s|^require File.dirname|require 'test/unit/diff'\nrequire File.dirname|" spec/ci/reporter/*_spec.rb

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Cleanup
rm -f %{buildroot}%{gem_instdir}/gemfiles/.gitignore
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -rf %{buildroot}%{gem_instdir}/.travis*
rm -rf %{buildroot}%{gem_instdir}/.yardo*
rm -rf %{buildroot}%{gem_instdir}/.rspec
rm -f %{buildroot}%{gem_instdir}/Gemfile
rm -f %{buildroot}%{gem_instdir}/Gemfile.lock
rm -f %{buildroot}%{gem_instdir}/ci_reporter.gemspec

%check
pushd %{buildroot}%{gem_instdir}
/usr/bin/ruby -S rspec \
    ./spec/ci/reporter/*_spec.rb
popd

%files
%doc %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec
%{gem_instdir}/Rakefile

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 27 2014 Troy Dawson <tdawson@redhat.com> - 2.0.0-1
- Updated to latest release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Troy Dawson <tdawson@redhat.com> - 1.9.2-2
- Re-enabled tests

* Tue Apr 15 2014 Troy Dawson <tdawson@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.9.1-1
- Updated to version 1.9.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Troy Dawson <tdawson@redhat.com> 1.8.2-2
- Tests only run on F18-, due to a bug in cucumber

* Thu Dec 06 2012 Troy Dawson <tdawson@redhat.com> 1.8.2-1
- Updated to 1.8.2
- Fixed tests so they work with our version of test-unit

* Fri Nov 30 2012 Troy Dawson <tdawson@redhat.com> 1.8.0-1
- Updated to 1.8.0
- Added test, and dependancies for test

* Wed Nov 28 2012 Troy Dawson <tdawson@redhat.com> 1.7.3-2
- Created a doc subpackage
- Fix dependancies
- Spec file cleanup

* Mon Nov 19 2012 Troy Dawson <tdawson@redhat.com> 1.7.3-1
- Initial spec file

