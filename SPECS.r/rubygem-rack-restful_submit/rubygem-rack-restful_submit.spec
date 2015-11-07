%global gem_name rack-restful_submit


Summary: Allows RESTful routing without Javascript and multiple submit buttons
Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/martincik/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix test suite to pass against Rack 1.6+.
# https://github.com/martincik/rack-restful_submit/pull/4
Patch0: rubygem-rack-restful_submit-1.2.2-Fix-test-suite-to-pass-against-Rack-1.6.patch
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
Requires: rubygem(rack) >= 1.3.0
Requires: rubygem(rack) < 2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rack) >= 1.3.0
BuildRequires: rubygem(rack) < 2
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Implements support of RESTful resources with Rails MVC when Javascript is off
and bulk operations are required with multiple submit buttons.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}
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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd %{buildroot}%{gem_instdir}
rspec spec/
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/.gitignore
%doc %{gem_instdir}/README.markdown
%doc %{gem_instdir}/LICENSE
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.2-10
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.2-9
- 为 Magic 3.0 重建

* Fri Jun 26 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.2-8
- Fix test suite compabitility with Rack 1.6+.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Rebuilt for Ruby 1.9.3.

* Fri Jan 06 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Updated to rack-restful_submit 1.2.2.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.1-3
- Fix upgrade path.

* Mon Aug 29 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.1-1
- Updated to rack-restful_submit 1.2.1.

* Tue Jun 28 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.2-4
- Relaxed Rack dependency to ~> 1.1.

* Tue Mar 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.2-3
- Updated RSpec dependencies. RSpec2 used for newer distributions.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Jozef Zigmund <jzigmund@redhat.com> - 1.1.2-1
- Initial package
