# Generated from bundler_ext-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bundler_ext

Summary: Load system gems via Bundler DSL
Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/bundlerext/bundler_ext
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby 
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(rails)
BuildArch: noarch

%description
Simple library leveraging the Bundler Gemfile DSL to load gems already on the
system and managed by the systems package manager (like yum/apt)


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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rspec2 spec
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Vít Ondruch <vondruch@redhat.com> - 0.4.0-1
- Update to bundler_ext 0.4.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 30 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.1-1
- Update to bundler_ext 0.3.1.

* Thu Jul 18 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.0-1
- Update to bundler_ext 0.3.0.

* Wed Nov 28 2012 Vít Ondruch <vondruch@redhat.com> - 0.1.0-4
- Yet again RHEL6 and Fedora 16 compatibility fixes.

* Fri Nov 23 2012 Vít Ondruch <vondruch@redhat.com> - 0.1.0-3
- More RHEL6 and Fedora 16 compatibility.

* Thu Nov 22 2012 Vít Ondruch <vondruch@redhat.com> - 0.1.0-2
- Add RHEL6 and Fedora 16 compatibility. 

* Tue Nov 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.1.0-1
- Initial package
