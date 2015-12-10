%global gem_name rsolr

Name: rubygem-%{gem_name}
Version: 1.0.11
Release: 5%{?dist}
Summary: A Ruby client for Apache Solr
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/rsolr/rsolr
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: rubygem(builder) >= 2.1.2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
RSolr aims to provide a simple and extensible library for working with Solr.


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
rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%license %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES.txt
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%{gem_instdir}/rsolr.gemspec
%{gem_instdir}/tasks
%doc %{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.11-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.11-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.11-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.11-1
- Update to RSolr 1.0.11.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.2-1
- Updated to the RSolr 1.0.2.

* Tue Jan 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.0-2
- Version file moved into main package, since it is required by runtime
- Removed unnecessary cleanup in install section

* Mon Jan 17 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
