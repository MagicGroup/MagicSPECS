# Generated from aruba-0.4.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name aruba

Summary: CLI Steps for Cucumber, hand-crafted for you in Aruba
Name: rubygem-%{gem_name}
Version: 0.6.2
Release: 4%{?dist}
Group: Development/Languages
# aruba itself is MIT
# icons in templates/images are CC-BY
# jquery.js itself is MIT or GPLv2
# jquery.js includes sizzle.js, which is MIT or BSD or GPLv2
License: MIT and CC-BY and (MIT or GPLv2) and (MIT or BSD or GPLv2)
URL: http://github.com/cucumber/aruba
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(cucumber) >= 1.1.1
BuildRequires: rubygem(childprocess) >= 0.2.0
%if 0%{?fedora} >= 22
BuildRequires: rubygem(rspec) >= 3
%else
BuildRequires: rubygem(rspec)
%endif
# used in one of the features
BuildRequires: bc
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Aruba is Cucumber extension for Command line applications written
in any programming language.


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

%if 0%{?fedora} < 23
pushd .%{gem_instdir}/
sed -i -e 's|:example|:each|' \
	spec/aruba/api_spec.rb
popd
%endif

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
cucumber
rspec spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/config
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/cucumber.yml
%{gem_instdir}/features
%{gem_instdir}/spec
%{gem_instdir}/templates

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.6.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.2-1
- 0.6.2

* Mon Sep  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.1-1
- 0.6.1

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.0-1
- 0.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.5.4-1
- 0.5.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Josef Stribny <jstribny@redhat.com> - 0.5.2-1
- Update to aruba 0.5.2

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.11-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-5
- Disable tests that do not actually test anything (patch from upstream).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-2
- Remove the ffi dependency and add conflicts with the problematic version.

* Fri Feb 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.11-1
- Initial package
