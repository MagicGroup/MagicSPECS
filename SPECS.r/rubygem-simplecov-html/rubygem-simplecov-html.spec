%global gem_name simplecov-html
%global rubyabi 1.9.1

Summary:       Default HTML formatter for SimpleCov
Name:          rubygem-%{gem_name}
Version:       0.10.0
Release:       2%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://github.com/colszowka/simplecov-html
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} >= 19 || 0%{?rhel} > 6
Requires:      ruby(release)
%else
Requires:      ruby(abi) >= %{rubyabi}
%endif
Requires:      ruby 
Requires:      rubygems
BuildRequires: ruby 
BuildRequires: rubygems-devel
# For tests
# Cant run tests because they require a circular
#  dependancy that cant be done yet
#BuildRequires: rubygem(test-unit)
#BuildRequires: rubygem(simplecov)
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Default HTML formatter for SimpleCov code coverage tool for ruby 1.9+


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
rm -f %{buildroot}%{gem_instdir}/.document
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.rubocop.yml
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -f %{buildroot}%{gem_instdir}/.yardopts
rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm -f %{buildroot}%{gem_instdir}/Gemfile
rm -f %{buildroot}%{gem_instdir}/simplecov-html.gemspec

%check
# Cant run tests because they require a circular
#  dependancy that cant be done yet
#testrb2 -Ilib test

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_instdir}/assets
%{gem_instdir}/public
%{gem_instdir}/views
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.0-2
- 为 Magic 3.0 重建

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 0.10.0-1
- Updated to version 0.10.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Troy Dawson <tdawson@redhat.com> - 0.8.0-2
- fix for correct EPEL7 build

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 0.8.0-1
- Updated to version 0.8.0
- Update to latest ruby spec guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 0.7.1-3
- Fix to make it build/install on F19+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Troy Dawson <tdawson@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 27 2012 Troy Dawson <tdawson@redhat.com> - 0.5.3-1
- Initial package
