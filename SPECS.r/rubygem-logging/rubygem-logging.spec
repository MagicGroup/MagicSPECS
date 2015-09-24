# Generated from logging-1.4.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name logging

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 2%{?dist}
Summary: A flexible and extendable logging library for Ruby
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/logging
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(little-plugger) >= 1.1.3
BuildRequires: rubygem(multi_json) >= 1.3.6
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
Logging is a flexible logging library for use in Ruby programs based on the
design of Java's log4j library. It features a hierarchical logging system,
custom level names, multiple output destinations per log event, custom
formatting, and more.

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
# https://github.com/TwP/logging/issues/114
LANG=en_US.utf8 ruby -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
# contains licensing information
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_libdir}
%{gem_spec}

%files doc
%{gem_instdir}/examples
%{gem_instdir}/script
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%{gem_instdir}/logging.gemspec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Update to Logging 2.0.0.

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.2-1
- Update to Logging 1.8.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.0-1
- Version 1.8.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.6.2-1
- Rebuilt for Ruby 1.9.3.
- Updated to version 1.6.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 02 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.6.1-1
- New version.
- Removed unnecessary defattr macro in files section.
- Removed unnecessary clean section.
- Replaced define macros with more appropriate global.
- Moved gem install to the prep section.
- Added check section to run tests.
- BuildRequires now contain rubygem(little-plugger) and rubygem(flexmock) due to running tests.
- Introduced doc subpackage.

* Wed Mar 16 2011 Chris Lalancette <clalance@redhat.com> - 1.4.3-1
- Initial package
