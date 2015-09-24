# Generated from i18n_data-0.2.7.gem by gem2rpm -*- rpm-spec -*-
%global gem_name i18n_data


Summary: Country/language names and 2-letter-code pairs, in 85 languages
Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/grosser/i18n_data
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# For offline build, the RUN_CODE_RUN env variable support is still valuable.
# Revert of https://github.com/grosser/i18n_data/commit/1be35a3a782975052133efc5c574f79dc01cf8dd#spec
Patch0: rubygem-i18n_data-0.4.0-Revert-run-code-run-is-dead.patch
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Country/language names and 2-letter-code pairs, in 85 languages


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

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}

# Encoding is required, otherwise test suite fails.
# https://github.com/grosser/i18n_data/issues/4

# Set RUN_CODE_RUN to exclude live_data_provider_spec.rb since
# it requires internet connetcion.
LANG=en_US.utf8 RUN_CODE_RUN=1 rspec spec/*_spec.rb

popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/gem-public_cert.pem
%exclude %{gem_instdir}/i18n_data.gemspec
%{gem_instdir}/cache
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile*
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/Readme.md
%doc %{gem_instdir}/example_output
%{gem_instdir}/spec


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.0-1
- Update to i18n_data 0.4.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.7-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.7-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.7-2
- Include README.markdown in main package since it contains license.
- Move VERSION into main package since it is required for runtime.
- Remove Requires: rubygem(activesupport) since it is just optional dependency.

* Tue Aug 02 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.7-1
- Initial package
