# Generated from ruby-dbus-0.7.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ruby-dbus
%global with_tests 0

Summary: Ruby module for interaction with D-Bus
Name: rubygem-%{gem_name}
Version: 0.9.0
Release: 5%{?dist}
Group: Development/Languages
License: LGPLv2+
URL: https://trac.luon.net/ruby-dbus
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
# soft dependency => require only for build
BuildRequires: rubygem(nokogiri)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
# Obsolete ruby-dbus
Provides: ruby(dbus) = %{version}
Provides: ruby-dbus = %{version}-%{release}
Obsoletes: ruby(dbus) <= 0.3.0
Obsoletes: ruby-dbus < 0.3.0-5

%description
Ruby D-Bus provides an implementation of the D-Bus protocol such that the
D-Bus system can be used in the Ruby programming language.


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

# fix rpmlint issue with Rakefile (should not have shebang)
sed -i '1d' .%{gem_instdir}/Rakefile

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}/test
%if 0%{?with_tests}
RUBYOPT="-I../lib" ./test_env testrb *_test.rb t[0-9]*.rb
%endif
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/NEWS
%doc %{gem_instdir}/VERSION
%doc %{gem_instdir}/doc
%doc %{gem_instdir}/examples
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-1
- Update to 0.9.0.
- Don't run tests by default (fail on Koji because of no networking).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Update to 0.8.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.0-3
- Bump release to allow getting 0.7.0-3 into F16 (stupid mistake).

* Tue Feb 28 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.0-2
- Simplified the test running.
- Properly obsolete ruby-dbus.
- Applied the patch that unbundles files from activesupport (accepted by upstream).

* Tue Feb 28 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.0-1
- Initial package
