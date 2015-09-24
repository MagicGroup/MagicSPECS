%global gem_name echoe

Summary: A Rubygems packaging tool that provides Rake tasks for documentation, extension compiling, testing, and deployment
Name: rubygem-%{gem_name}
Version: 4.3.1
Release: 11%{?dist}
Group: Development/Languages
License: MIT
URL: http://blog.evanweaver.com/files/doc/fauna/echoe/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0: %{name}-remove-vendor-rake.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(gemcutter)
Requires: rubygem(rake)
Requires: rubygem(rubyforge)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A Rubygems packaging tool that provides Rake tasks for documentation,
extension compiling, testing, and deployment.

%prep
%setup -q -c -T 
%gem_install -n %{SOURCE0}
pushd .%{gem_instdir}
%patch0
popd

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}


# Vendorized rake is not needed here
rm -rf %{buildroot}%{gem_instdir}/vendor

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/Manifest
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}
%{gem_cache}
%{gem_spec}


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 4.3.1-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 4.3.1-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Michal Fojtik <mfojtik@redhat.com> 4.3.1-2
- Removed vendorized rake from echoe.rb
- Removed unused site_lib macro

* Wed Oct 27 2010 Michal Fojtik <mfojtik@redhat.com> 4.3.1-1
- Version bump
- Fixed file list (marked doc files)
- Removed vendored rake

* Fri Apr 30 2010 jesus m. rodriguez <jesusr@redhat.com> 4.3-2
- rebuild with tito

* Wed Mar 31 2010 Adam Young <ayoung@ayoung.boston.devel.redhat.com> - 4.3-1
- Initial package
