%global gem_name jnunemaker-matchy

Summary: RSpec-esque matchers for use in Test::Unit
Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 12%{?dist}
Group: Development/Languages
License: MIT
URL: http://matchy.rubyforge.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
RSpec-esque matchers for use in Test::Unit

%package doc
Summary:           Documentation for %{name} 
Group:             Documentation
Requires:          %{name} = %{version}-%{release}

%description doc 
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
rm -f %{buildroot}/%{gem_instdir}/matchy.gemspec

%check
pushd %{buildroot}%{gem_instdir}
testrb2 test/all.rb
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/License.txt
%doc %{gem_instdir}/PostInstall.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/setup.rb
%{gem_instdir}/countloc.rb
%{gem_instdir}/Rakefile
%{gem_instdir}/config
%{gem_instdir}/tasks
%{gem_instdir}/test
%{gem_docdir}


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.4.0-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.0-11
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Josef Stribny <jstribny@redhat.com> - 0.4.0-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.0-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 <stahnma@fedoraproject.org> - 0.4.0-3
- Rebuilt to fix 716203

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 16 2010  <stahnma@fedoraproject.org> - 0.4.0-2
- Review Modifications

* Mon Aug 16 2010  <stahnma@fedoraproject.org> - 0.4.0-1
- Initial package
