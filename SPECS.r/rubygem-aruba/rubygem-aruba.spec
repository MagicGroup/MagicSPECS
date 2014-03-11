# Generated from aruba-0.4.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name aruba

Summary: CLI Steps for Cucumber, hand-crafted for you in Aruba
Name: rubygem-%{gem_name}
Version: 0.5.2
Release: 1%{?dist}
Group: Development/Languages
# aruba itself is MIT
# icons in templates/images are CC-BY
# jquery.js itself is MIT or GPLv2
# jquery.js includes sizzle.js, which is MIT or BSD or GPLv2
License: MIT and CC-BY and (MIT or GPLv2) and (MIT or BSD or GPLv2)
URL: http://github.com/cucumber/aruba
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(cucumber) >= 1.1.1
Requires: rubygem(childprocess) >= 0.2.0
# Doesn't work with ffi 1.0.10, see https://github.com/cucumber/aruba/issues/114
Conflicts: rubygem(ffi) = 1.0.10
Requires: rubygem(rspec) >= 2.7.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(cucumber) >= 1.1.1
BuildRequires: rubygem(childprocess) >= 0.2.0
BuildConflicts: rubygem(ffi) = 1.0.10
BuildRequires: rubygem(rspec) >= 2.7.0
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
