# Generated from sanitize-2.0.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sanitize

Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 5%{?dist}
Summary: Whitelist-based HTML sanitizer
Group: Development/Languages
License: MIT
URL: https://github.com/rgrove/sanitize/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: rubygems
Requires: rubygem(nokogiri) >= 1.4.4
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.2.0
BuildRequires: ruby
BuildRequires: rubygem(minitest4)
BuildRequires: rubygem(nokogiri)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Sanitize is a whitelist-based HTML sanitizer. Given a list of acceptable 
elements and attributes, Sanitize will remove all unacceptable HTML from 
a string.

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

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/HISTORY.md
%{gem_instdir}/test/

%changelog
* Mon Jun 22 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.0-5
- Fix minitest usage for F22+

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.0-3
- Fix minitest BR (#1107232)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 25 2014 Achilleas Pipinellis <axilleaspi@ymail.com> - 2.1.0-1
- Update to 2.1.0

* Sat Jul 27 2013 Achilleas Pipinellis <axilleaspi@ymail.com> - 2.0.6-2
- Tests don't need to be removed
- Fix BR nokogiri to match upstream gemspec

* Sat Jul 27 2013 Achilleas Pipinellis <axilleaspi@ymail.com> - 2.0.6-1
- Initial package
