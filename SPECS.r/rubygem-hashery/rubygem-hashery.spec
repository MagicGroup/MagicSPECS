%global gem_name hashery

Summary: Facets bread collection of Hash-like classes
Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 7%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubyworks.github.com/hashery
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: ruby(release)
BuildRequires: rubygems-devel

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
The Hashery is a collection of Hash-like classes, spun-off from the original
Ruby Facets library. Included are the widely used OrderedHash, the related but
more featured Dictionary class, a number of open classes, similiar to the
standard OpenStruct and a few variations on the standard Hash.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep

%build

%install
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/alt
%{gem_spec}
%doc %{gem_instdir}/HISTORY.rdoc
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/NOTICE.txt
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_cache}

%files doc
%{gem_instdir}/test
%{gem_instdir}/.yardopts
%{gem_instdir}/.meta
%{gem_docdir}
%doc %{gem_instdir}/DEMO.rdoc
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/NOTICE.txt

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.1.0-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.0-6
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Marek Goldmann <mgoldman@redhat.com> - 2.1.0-4
- Add the gem_spec back to the package, RHBZ#992944

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 2.1.0-2
- Use %%gem_install macro.

* Sat Mar 16 2013 Marek Goldmann <mgoldman@redhat.com> - 2.1.0-1
- Upstream release 2.1.0
- New guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Marek Goldmann <mgoldman@redhat.com> - 2.0.0-1
- Upstream release 2.0.0
- License clarification, RHBZ#787167
- Spec cleanup

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.4.0-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Marek Goldmann <mgoldman@redhat.com> - 1.4.0-2
- Fixed files section

* Thu Jan 20 2011 Marek Goldmann <mgoldman@redhat.com> - 1.4.0-1
- Updated to new upstream release: 1.4.0

* Fri Nov 26 2010 Marek Goldmann <mgoldman@redhat.com> - 1.3.0-3
- Added R: rubygem(facets)

* Mon Nov 15 2010 Marek Goldmann <mgoldman@redhat.com> - 1.3.0-2
- Updated license

* Mon Nov 15 2010 Marek Goldmann <mgoldman@redhat.com> - 1.3.0-1
- Initial package
