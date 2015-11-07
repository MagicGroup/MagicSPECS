%global gem_name state_machine

%global rubyabi 1.9.1
  
%if 0%{?fedora} >= 17
  %global rubyabi 1.9.1
%endif

%if 0%{?fedora} >= 19
  %global rubyabi 2.0.0
%endif

Summary:       Adds support for creating state machines for attributes on any Ruby class
Name:          rubygem-%{gem_name}
Version:       1.1.2
Release:       14%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://www.pluginaweek.org
Source0:       http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      ruby(release)
Requires:      ruby(rubygems)
Requires:      graphviz-ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem-rake
BuildRequires: graphviz-ruby
BuildRequires: ruby-irb
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Adds support for creating state machines for attributes on any Ruby class

%package doc
Summary: Documentation files, rdoc, ri, examples and tests
Group: Documentation

%description doc
Documentation files for state_machine, includes RDoc, ri, tests,
examples and another extra documentation files.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version}

# Modify the gemspec if necessary with a patch or sed
# Also apply patches to code if necessary
# %%patch0 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
%gem_install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# rm unnecesary files
rm %{buildroot}%{gem_instdir}/.gitignore
rm %{buildroot}%{gem_instdir}/.travis.yml
rm %{buildroot}%{gem_instdir}/.yardopts
rm -r %{buildroot}%{gem_instdir}/gemfiles
rm %{buildroot}%{gem_instdir}/init.rb
rm %{buildroot}%{gem_instdir}/Appraisals

%check
cd %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}
# gem 'appraisal (~> 0.4.0) not available in Fedora
# gem 'rcov' not supported in Ruby 1.9
# test suite needs to be modified to be run in Fedora
echo "Running tests (disabled)"
#rake test
rm %{buildroot}%{gem_instdir}/Gemfile
rm %{buildroot}%{gem_instdir}/state_machine.gemspec

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_libdir}
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%{gem_cache}
%doc %{gem_spec}
   /usr/share/gems/gems/state_machine-1.1.2/Gemfile
   /usr/share/gems/gems/state_machine-1.1.2/state_machine.gemspec

%files doc
%defattr(-, root, root, -)
%doc %{gem_instdir}/examples
%doc %{gem_instdir}/test
%doc %{gem_docdir}
%doc %{gem_instdir}/Rakefile

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.2-14
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-13
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.1.2-9
- Minor spec adjustments for Ruby 2.0.0

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Guillermo Gómez <guillermo.gomez@gmail.com> - 1.1.2-6
- Removed unnecesary dependencies
- Spec adjusted according new guidelines

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Guillermo Gomez <gomix@fedoraproject.org> - 1.1.2-4
- Requires fixed for Ruby 1.9.3.

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 21 2012 Guillermo Gómez <gomix@fedoraproject.org> - 1.1.2-2
- Added BR rubygem-bundler to run test suite in the future, excluding
- epel versions, bundler not available yet

* Sat Jan 21 2012 Guillermo Gómez <gomix@fedoraproject.org> - 1.1.2-1
- Updated version 1.1.2

* Wed Jan 04 2012 Guillermo Gómez <gomix@fedoraproject.org> - 1.1.1-1
- Updated version 1.1.1

* Tue Nov 15 2011 Guillermo Gómez <gomix@fedoraproject.org> - 1.1.0-1
- Updated version 1.1.0

* Mon Nov 14 2011 Guillermo Gómez <gomix@fedoraproject.org> - 1.0.3-1
- Updated version 1.0.3

* Thu Sep 15 2011 Guillermo Gómez <gomix@fedoraproject.org> - 1.0.2-1
- Updated version 1.0.2

* Sun Jun 05 2011 Guillermo Gómez <gomix@fedoraproject.org> - 1.0.1-1
- Updated version 1.0.1

* Tue Apr 12 2011 Guillermo Gomez <gomix@fedoraproject.org> - 0.10.3-2
- graphviz-ruby dependency added

* Mon Apr 11 2011 Guillermo Gomez <gomix@fedoraproject.org> - 0.10.3-1
- Udpate version 0.10.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Guillermo Gomez <gomix@fedoraproject.org> - 0.9.4-5
- %%check section added

* Mon Oct 25 2010 Guillermo Gomez <gomix@fedoraproject.org> - 0.9.4-4
- Group Documentation for -doc subpackage

* Thu Sep 23 2010 Guillermo Gomez <gomix@fedoraproject.org> - 0.9.4-3
- Bug fixed BZ636902

* Sun Aug 15 2010 Guillermo Gómez <gomix@fedoraproject.org> - 0.9.4-2
- Documentation splitted in -doc subpackage.

* Tue Aug 10 2010 Guillermo Gomez <gomix@fedoraproject.org> - 0.9.4-1
- Release 0.9.4 of state_machine.

* Mon Aug 17 2009 Darryl Pierce <dpierce@redhat.com> - 0.8.0-1
- Release 0.8.0 of state_machine.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Darryl Pierce <dpierce@redhat.com> - 0.7.6-1
- First official release for Fedora.

* Mon Jul 13 2009 Darryl Pierce <dpierce@redhat.com> - 0.7.4-4
- Fixed ownership of install directory.

* Fri Jul 10 2009 Darryl Pierce <dpierce@redhat.com> - 0.7.4-3
- Fixed double-listing of files.

* Wed Jul  1 2009 Darryl Pierce <dpierce@redhat.com> - 0.7.4-2
- Fixed license to be MIT.
- Added ruby(abi) requirement.

* Sat May 23 2009 Darryl Pierce <dpierce@redhat.com> - 0.7.4-1
- Initial package
