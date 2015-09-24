# Generated from krb5-auth-0.6.gem by gem2rpm -*- rpm-spec -*-
%define gem_name krb5-auth

Summary: Kerberos binding for Ruby
Name: rubygem-%{gem_name}
Version: 0.7
Release: 15%{?dist}
Group: Development/Languages
License: LGPLv2+
URL: http://rubyforge.org/projects/krb5-auth
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
BuildRequires: krb5-devel

%description
Kerberos binding for Ruby

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

rm -rf %{buildroot}%{gem_instdir}/ext

%files
%dir %{gem_instdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README
%doc %{gem_instdir}/TODO
%{gem_instdir}/bin
%{gem_instdir}/Rakefile
%{gem_extdir_mri}/
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Vít Ondruch <vondruch@redhat.com> - 0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 0.7-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.7-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 20 2008 Chris Lalancette <clalance@redhat.com> 0.7-1
- Convert from hand-coded makes to a proper Rakefile
- Update to 0.7

* Wed May 21 2008 Alan Pevec <apevec@redhat.com> 0.6-1
- add debuginfo support, taken from rubygem-zoom.spec
- include COPYING file in the gem (for licensing)
- bump the version number to 0.6

* Fri May 16 2008 Alan Pevec <apevec@redhat.com> 0.5-2
- package shared library per Packaging/Ruby guidelines

* Tue Apr 22 2008 Chris Lalancette <clalance@redhat.com> - 0.5-1
- Move project to krb5-auth on RubyForge

* Fri Jan 11 2008 Chris Lalancette <clalance@redhat.com> - 0.4-3
- Update the destroy method to use alternate caches

* Fri Jan 11 2008 Chris Lalancette <clalance@redhat.com> - 0.4-2
- Update the cache method to use alternate caches

* Wed Jan 02 2008 Chris Lalancette <clalance@redhat.com> - 0.4-1
- Initial package

