%define gem_name pam
%define libname _%{gem_name}.so

# Main package bundles it at a gem
Name:           rubygem-%{gem_name}
Version:        1.5.4
Release:        24%{?dist}
Summary:        Ruby bindings for pam
Group:          Development/Languages

License:        LGPLv2+
URL:            http://rubyforge.org/projects/ruby-pam
Source0:        http://rubyforge.org/frs/download.php/43802/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  pam-devel >= 0.0.6
BuildRequires:  ruby-devel >=  1.9
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  ruby-irb
BuildRequires:  rubygem-rake
Requires:       rubygems
Requires:       ruby(release) >= 1.9
Provides:       rubygem(%{gem_name}) = %{version}

%description
Ruby bindings for pam exposed via a gem

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

# Installs the gem, and then moves the compiled code to the site
# library.
%install
rm -rf %{buildroot}
install -d -m0755  %{buildroot}%{gem_dir}
install -d -m0755  %{buildroot}%{ruby_sitelibdir}
install -d -m0755  %{buildroot}%{ruby_sitearchdir}

# copy the results of hte build over.
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Move the library into the extension specific location
%if 0%{?fedora} >= 21
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/{%{libname},gem.build_complete}  %{buildroot}%{gem_extdir_mri}
%else
mkdir -p %{buildroot}%{gem_extdir_mri}/ext
mv %{buildroot}%{gem_instdir}/ext/%{libname} %{buildroot}%{gem_extdir_mri}/ext/%{libname}
%endif

# Remove the cruft in the old locations.
rm -rf %{buildroot}%{gem_instdir}/ext
rm -rf %{buildroot}%{gem_dir}/extensions

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{gem_instdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/lib
%{gem_dir}/cache/%{gem_name}-%{version}.gem
%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%{gem_extdir_mri}/
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/MANIFEST
%doc %{gem_instdir}/README
%doc %{gem_instdir}/ChangeLog
%doc %{gem_dir}/doc

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.5.4-24
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.5.4-23
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.5.4-21
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Dec 23 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.4-20
- Install gem.build_complete on F-21+ (bug 1176450)
- Fix directory ownership for extension files

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Bryan Kearney <bkearney@redhat.com> - 1.5.4-17
- Rebuilt with new macros. Also, per the standard, removed the non gem version.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 Bryan Kearney <bkearney@redhat.com> - 1.5.4-15
- Change ruby(abi) to ruby(release)

* Wed Mar 27 2013 Bryan Kearney <bkearney@redhat.com> - 1.5.4-14
- Rebuild to get the latest dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 19 2012 Bryan Kearney <bkearney@redhat.com> - 1.5.4-11
- Make the ruby requirements a bit more lax

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 16 2009 Bryan Kearney <bkearney@redhat.com> - 1.5.3-7
- Added rdoc directories to the build based on s390 failures.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.5.3-5
- Fix unowned versioned directory (#474607).

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> - 1.5.3-4
- Removed redefined version and release from subpackage

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> - 1.5.3-3
- Another rebuilt to solve the koji buildsystem failure

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 23 2008 Bryan Kearney <bkearney@redhat.com> - 1.5.3-1
- Added a shim layer to better support multiple architectures

* Tue Aug 19 2008 Bryan Kearney <bkearney@redhat.com> - 1.5.2-3
- More package review.

* Tue Aug 19 2008 Bryan Kearney <bkearney@redhat.com> - 1.5.2-2
- Fixes according to Fedora review

* Wed Aug 6 2008 Bryan Kearney <bkearney@redhat.com> - 1.5.2-1
- Initial specfile
