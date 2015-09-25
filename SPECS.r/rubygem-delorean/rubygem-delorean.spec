%global gem_name delorean

Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 3%{?dist}
Summary: Delorean lets you travel in time with Ruby by mocking Time.now
Group: Development/Languages
License: MIT
URL: https://github.com/bebanjo/delorean
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# to get specs:
# git clone https://github.com/bebanjo/delorean.git && cd delorean
# git checkout v2.1.0
# tar -czf rubygem-delorean-2.1.0-spec.tgz spec/
Source1:  %{name}-%{version}-spec.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# for specs:
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(chronic)
BuildArch: noarch

%description
Delorean lets you travel in time with Ruby by mocking Time.now.

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
tar xzf %{SOURCE1}

rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.0-1
- Update to Delorean 2.1.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 20 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-5
- Rebuilt with ActiveSupport 4.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 2.0.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.0-1
- Update to version 2.0.0.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-5
- Properly set ruby(abi) = 1.9.1.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-2
- Fixed the specfile permissions.
- Added tests.

* Mon Jan 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-1
- Initial package.
