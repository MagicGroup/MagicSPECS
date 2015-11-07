%global gem_name parseconfig

Summary:        Ruby Configuration File Parser 
Name:           rubygem-%{gem_name}
Version:       	1.0.4 
Release:        4%{?dist}
Group:          Development/Languages
License:        MIT 
URL:            http://github.com/derks/ruby-parseconfig
Source0:        http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: 	ruby(rubygems), ruby(release)
BuildRequires: 	rubygems-devel, rubygem-rspec
BuildRequires: 	ruby-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
ParseConfig provides simple parsing of standard configuration files in the 
form of 'param = value'.  It also supports nested [group] sections.

%prep 

%build
# pass, nothing to do

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{gem_cache}
%{gem_spec}
%dir %{gem_instdir}
%dir %{gem_libdir}/
%{gem_libdir}/parseconfig.rb
%doc %{gem_docdir}/
%doc %{gem_instdir}/Changelog
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.4-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 BJ Dierkes <derks@datafolklabs.com> - 1.0.4-1
- Latest sources from upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.2-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 BJ Dierkes <wdierkes@rackspace.com> - 1.0.2-1
- Latest sources from upstream.

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.2-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 05 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.5.2-3
- Removed comment from Source0, URL no longer changes
- Resolved duplicate file listing

* Mon Apr 05 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.5.2-2
- Added geminstdir to file list
- Requires: ruby(abi) >= 1.8
- Removed check
- Updated for current rubygems download url
- Removed unused macros ruby_sitelib, installroot

* Sat Feb 27 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.5.2-1
- Initial spec, borrowed from rubygem-cobbler
