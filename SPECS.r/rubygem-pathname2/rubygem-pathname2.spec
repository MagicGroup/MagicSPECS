%global gem_name    pathname2

%if 0%{?fedora} >= 19
%global gem_extdir %{gem_extdir_mri}
%endif

Name:           rubygem-%{gem_name}
Version:        1.7.3
Release:        4%{?dist}
Summary:        An alternate implementation for the Pathname library

Group:          Development/Languages
License:        Artistic 2.0
URL:            http://raa.ruby-lang.org/project/pathname2/
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: rubygem(facade)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(minitest)
BuildRequires: rubygems-devel

%if 0%{?fedora} >= 19
Requires: ruby(release)
%else
Requires:      ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif

Requires:      rubygem(facade)
Requires:      ruby(rubygems)

Provides:      rubygem(%{gem_name}) = %{version}

%description
An alternate implementation for the Pathname library. This version treats a
 path name as a String, though with certain methods overloaded.

%prep
%setup -q -c -T

%{__mkdir_p} .%{gem_dir}
gem install --local --install-dir=.%{gem_dir} \
   --force --rdoc %{SOURCE0}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{gem_dir}
%{__cp} -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%check
# This seems to fail temporarily due to
# https://github.com/ruby/ruby/commit/4077b9b89dc1f139775774e59705677e54712cba
# but should be already fixed by
# https://github.com/ruby/ruby/commit/a6e3d4bea0c6625c76669d7246868f7683dd23a6
# http://bugs.ruby-lang.org/issues/8633
sed -i "/    methods\.delete('identical?')$/ a\\    methods.delete(:mode_to_s)" $(pwd)%{gem_instdir}/test/test_pathname.rb

ruby -I$(pwd)%{gem_libdir} $(pwd)%{gem_instdir}/test/test_pathname.rb

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{gem_instdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/MANIFEST
%doc %{gem_instdir}/README
%{gem_cache}
%{gem_instdir}/benchmarks
%{gem_instdir}/examples
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_libdir}
%{gem_instdir}/test
%{gem_spec}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014  Brett Lentz <blentz@redhat.com> - 1.7.3-1
- upstream release 1.7.3

* Thu Apr 10 2014  Brett Lentz <blentz@redhat.com> - 1.7.1-1
- upstream release 1.7.1
- drop unneeded patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Brett Lentz <blentz@redhat.com> - 1.6.5-1
- upstream release 1.6.5

* Wed Mar 13 2013 Brett Lentz <blentz@redhat.com> - 1.6.2-12
- Update to new packaging guidelines.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.2-9
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 08 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-6
- change defines to globals.

* Mon Aug 24 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-5
- change install method to allow use of patch macro.
- remove period at the end of summary.

* Mon Aug 24 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-4
- Add check section for running tests.
- Simplify a few things in the files section. 
- Add patch for running tests on ruby 1.8

* Thu Aug 20 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-3
- Fix a few more spec file issues, as noted in https://bugzilla.redhat.com/show_bug.cgi?id=518083

* Thu Aug 20 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-2
- Fix a few spec file issues, as noted in https://bugzilla.redhat.com/show_bug.cgi?id=518083

* Tue Aug 18 2009 Brett Lentz <wakko666@gmail.com> - 1.6.2-1
- First packaging.
