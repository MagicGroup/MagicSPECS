# Generated from fakefs-0.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name fakefs

Name: rubygem-%{gem_name}
Version: 0.6.7
Release: 1%{?dist}
Summary: A fake filesystem. Use it in your tests
Group: Development/Languages
License: MIT
URL: http://github.com/defunkt/fakefs
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
A fake filesystem. Use it in your tests.


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

# https://github.com/defunkt/fakefs/pull/309
chmod a-x %{buildroot}%{gem_instdir}/{test/fakefs_test.rb,lib/fakefs/file.rb}

%check
pushd .%{gem_instdir}
rspec spec

# minitest-rg is not available in Fedora yet not it is needed.
sed -i '/minitest\/rg/ s/^/#/' test/test_helper.rb

ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTORS
%{gem_instdir}/etc
%{gem_instdir}/fakefs.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/spec
%{gem_instdir}/test

%changelog
* Wed Jun 24 2015 Vít Ondruch <vondruch@redhat.com> - 0.6.7-1
- Update to FakeFS 0.6.7.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 23 2014 Vít Ondruch <vondruch@redhat.com> - 0.5.2-1
- Update to FakeFS 0.5.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.2-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to FakeFS 0.4.2.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.0-1
- Initial package
