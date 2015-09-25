%global gem_name sshkey

Name:     rubygem-%{gem_name}
Version:  1.7.0
Release:  2%{?dist}
Summary:  Generate private/public SSH key-pairs using pure Ruby
Group:    Development/Languages
License:  MIT
URL:      https://github.com/bensie/sshkey
Source0:  http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch: noarch
BuildRequires: ruby(release)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygems
BuildRequires: rubygems-devel
Requires: ruby(release)
Requires: rubygems

Provides: rubygem(%{gem_name}) = %{version}


%description
Generate private and public SSH keys (RSA and DSA supported) using pure Ruby.


%package doc
Summary: Documentation for %{gem_name}
Group: Documentation
Requires: %{name} = %{version}-%{release}


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
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

#cleanup some files
rm -f %{buildroot}%{gem_instdir}/.travis.yml
rm -f %{buildroot}%{gem_instdir}/.gitignore

%check
pushd %{buildroot}%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%doc LICENSE 
%dir %{gem_instdir}
%exclude %{gem_cache}
%{gem_libdir}
%{gem_spec}


%files doc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/Gemfile
%doc %{gem_docdir}
%{gem_instdir}/test


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7.0-2
- 为 Magic 3.0 重建

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 1.7.0-1
- Updated to version 1.7.0
- Changed check from testrb2 to ruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 04 2014 Troy Dawson <tdawson@redhat.com> - 1.6.1-1
- Updated to version 1.6.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 1.3.1-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Troy Dawson <tdawson@redhat.com> - 1.3.1-2
- Put license in doc subpackage

* Tue Jul 17 2012 Troy Dawson <tdawson@redhat.com> - 1.3.1-1
- Updated to version 1.3.1

* Tue Jul 17 2012 Troy Dawson <tdawson@redhat.com> - 1.3.0-5
- Added doc to the docdir

* Tue Jul 17 2012 Troy Dawson <tdawson@redhat.com> - 1.3.0-4
- Fixed up macrose, exlude gem cache

* Fri Jul 13 2012 Troy Dawson <tdawson@redhat.com> - 1.3.0-3
- Fixed to really be according to F17+ guidelines

* Wed Jun 13 2012 Troy Dawson <tdawson@redhat.com> - 1.3.0-2
- Updated to new rubygem packaging guidelines for F17+

* Sun Apr 29 2012 Wesley Hearn <whearn@redhat.com> - 1.3.0-1
- Initial package

