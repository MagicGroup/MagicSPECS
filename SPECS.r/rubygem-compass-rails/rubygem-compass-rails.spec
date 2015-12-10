%global gem_name compass-rails
%global rubyabi 1.9.1

Summary:       Integrate Compass into Rails 2.3 and up
Name:          rubygem-%{gem_name}
Version:       2.0.4
Release:       4%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://github.com/Compass/compass-rails
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:      rubygems
Requires:      rubygem(compass) >= 0.12.2
Requires:      rubygem(actionpack)
Requires:      rubygem(rails)
Requires:      rubygem(sass-rails)
%if 0%{?fedora} >= 19 || 0%{?rhel} > 6
Requires:      ruby(release)
BuildRequires: ruby(release)
%else
Requires:      ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif
BuildRequires: rubygems
BuildRequires: rubygems-devel
# For tests
#BuildRequires: rubygem(test-unit)
#BuildRequires: rubygem(compass) >= 0.12.2
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Integrate Compass into Rails 2.3 and up.

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

## fix dependencies
sed -i "s|2.13|3.99|" compass-rails.gemspec
sed -i "s|5.0.1|5.0.99|" compass-rails.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Cleanup stuff
rm -f %{buildroot}%{gem_instdir}/.gitignore
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -f %{buildroot}%{gem_instdir}/*.gemspec
rm -rf %{buildroot}%{gem_instdir}/.yardoc
find %{buildroot} -iname .gitkeep -exec rm -f {} \;
chmod 0755 %{buildroot}%{gem_instdir}/Rakefile

%check
# Dont run tests until they get cleaned up, upstream
#pushd ./%{gem_instdir}
#ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
#popd

%files
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/sache.json

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/Appraisals
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/gemfiles

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.4-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.0.4-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.4-2
- 为 Magic 3.0 重建

* Mon Jul 27 2015 Troy Dawson <tdawson@redhat.com> - 2.0.4-1
- Update to 2.0.4

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 08 2014 Troy Dawson <tdawson@redhat.com> - 1.1.7-4
- Really fix sprockets dependency

* Mon Jul 07 2014 Troy Dawson <tdawson@redhat.com> - 1.1.7-3
- Fix sprockets dependency

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Troy Dawson <tdawson@redhat.com> - 1.1.7-1
- Updated to version 1.1.7

* Wed Mar 12 2014 Troy Dawson <tdawson@redhat.com> - 1.1.6-1
- Updated to version 1.1.6

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.1.3-1
- Updated to version 1.1.3
- Update to latest ruby spec guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 1.0.3-7
- Fix to make it build/install on F19+

* Thu Feb 14 2013 Troy Dawson <tdawson@redhat.com> - 1.0.3-6
- Fix requires for 3.1+ rails versions (#901540)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Troy Dawson <tdawson@redhat.com> - 1.0.3-3
- removed Requires: ruby
- added gemfiles to doc
- comment out tests until upstream cleans them up

* Wed Dec 05 2012 Troy Dawson <tdawson@redhat.com> - 1.0.3-2
- Fixup spec file
- Added rubgem-compass for BuildRequires

* Tue Sep 11 2012 Troy Dawson <tdawson@redhat.com> - 1.0.3-1
- Initial package
