%global gem_name factory_girl

Summary: Framework and DSL for defining and using model instance factories
Name: rubygem-%{gem_name}
Version: 2.3.2
Release: 9%{?dist}
Group: Development/Languages
License: MIT
URL: http://thoughtbot.com/projects/factory_girl
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Framework and DSL for defining and using factories - less error-prone,
more explicit, and all-around easier to work with than fixtures.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}
pushd .%{gem_instdir}
popd


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
rm ./%{gem_instdir}/.autotest
rm ./%{gem_instdir}/.gitignore
rm ./%{gem_instdir}/.rspec
rm ./%{gem_instdir}/.travis.yml
rm ./%{gem_instdir}/Appraisals
rm ./%{gem_instdir}/Gemfile
rm ./%{gem_instdir}/Gemfile.lock
rm ./%{gem_instdir}/.yardopts
rm -rf ./%{gem_instdir}/gemfiles
cp -va ./%{gem_dir}/* %{buildroot}%{gem_dir}


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/Changelog
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_docdir}
%{gem_instdir}/features
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%{gem_instdir}/cucumber.yml
%{gem_instdir}/CONTRIBUTION_GUIDELINES.md
%{gem_instdir}/GETTING_STARTED.md


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 2.3.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.3.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Michal Fojtik <mfojtik@redhat.com> - 2.3.2-1
- Version bump

* Tue Jul 05 2011 Chris Lalancette <clalance@redhat.com> - 1.3.2-5
- Fixes to build in rawhide

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-3
- Replaced path with path macro

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-2
- Rakefile fixing moved to a separate patch
- Fixed unneeded Requires
- Fixed directory ownership on doc subpackage
- README and LICENSE moved back to main package

* Sat Oct 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.2-1
- Initial package
