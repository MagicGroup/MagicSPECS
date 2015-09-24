# Generated from rbovirt-0.0.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rbovirt

Summary: A Ruby client for oVirt REST API
Name: rubygem-%{gem_name}
Version: 0.0.35
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/abenari/rbovirt
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rest-client)
BuildArch: noarch

%description
A Ruby client for oVirt REST API


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
rspec2 spec/unit
# Integration tests does not work yet (if ever).
# rspec2 spec/integration
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%exclude %{gem_instdir}/.document
%exclude %{gem_instdir}/.gitignore
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES.rdoc
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.35-1
- Update to rbovirt 0.0.35.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 06 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.24-1
- Update to rbovirt 0.0.24.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Michal Fojtik <mfojtik@redhat.com> - 0.0.18-2
- Fixed rspec name

* Mon Mar 18 2013 Michal Fojtik <mfojtik@redhat.com> - 0.0.18-1
- Update to rbovirt 0.0.18

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.17-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Feb 13 2013 Michal Fojtik - 0.0.17-2
- Fixed rspec dependency

* Wed Feb 13 2013 Michal Fojtik <mfojtik@redhat.com> - 0.0.17-1
- Update to rbovirt 0.0.17

* Fri Nov 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.14-1
- Update to rbovirt 0.0.14

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.12-1
- Update to rbovirt 0.0.12.

* Thu Feb 16 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.6-1
- Update to rbovirt 0.0.6.

* Wed Feb 08 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.5-1
- Initial package
