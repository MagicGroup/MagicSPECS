%global gem_name    facade

Name:           rubygem-%{gem_name}
Version:        1.0.5
Release:        5%{?dist}
Summary:        A module that helps implement the facade pattern

Group:          Development/Languages
License:        Artistic 2.0
URL:            https://github.com/djberg96/facade
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildArch:      noarch

BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)



%description
A simple way to implement the facade pattern in Ruby.

%prep

%build

%install
%{__rm} -rf %{buildroot}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%check
pushd %{buildroot}/%{gem_instdir}
ruby -Ilib test/test_facade.rb
popd

%files
%dir %{gem_instdir}
%dir %{gem_libdir}
%dir %{gem_instdir}/test
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/MANIFEST
%doc %{gem_instdir}/README
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_libdir}/%{gem_name}.rb
%{gem_instdir}/test/test_facade.rb
%exclude %{gem_cache}
%{gem_spec}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.0.5-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.5-4
- 为 Magic 3.0 重建

* Tue Jul 29 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.5-3
- Fix FTBFS in Rawhide (rhbz#1107107).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 5 2014 Brett Lentz <blentz@redhat.com> - 1.0.5-1
- update to 1.0.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Brett Lentz <blentz@redhat.com> - 1.0.4-10
- Use %%gem_install macro

- Rebuilt according to new packaging guidelines for F19/F20
* Wed Mar 13 2013 Brett Lentz <blentz@redhat.com> - 1.0.4-9
- Rebuilt according to new packaging guidelines for F19/F20

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.4-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 20 2009 Brett Lentz <wakko666@gmail.com> - 1.0.4-4
- Simplify a few things in the files section. 

* Thu Aug 20 2009 Brett Lentz <wakko666@gmail.com> - 1.0.4-3
- Fix a few more spec file issues, as noted in https://bugzilla.redhat.com/show_bug.cgi?id=518082

* Thu Aug 20 2009 Brett Lentz <wakko666@gmail.com> - 1.0.4-2
- Fix a few spec file issues, as noted in https://bugzilla.redhat.com/show_bug.cgi?id=518082

* Tue Aug 18 2009 Brett Lentz <wakko666@gmail.com> - 1.0.4-1
- First packaging.
