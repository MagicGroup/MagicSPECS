# -*- rpm-spec -*-
%global gem_name systemu

# EPEL6 lacks rubygems-devel package that provides these macros
%if %{?el6}0
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%endif

Name:           rubygem-%{gem_name}
Version:        2.6.4
Release:        2%{?dist}
Summary:        Universal capture of stdout and stderr and handling of child process pid
Group:		Development/Libraries

License:        BSD or Ruby
URL:            https://github.com/ahoward/systemu
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

%if 0%{?fedora} >= 19
Requires: ruby(release)
BuildRequires: ruby(release)
%else
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
Requires:	ruby(rubygems) 
BuildRequires:	ruby(rubygems)
%{!?el6:BuildRequires: rubygems-devel}

Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Universal capture of stdout and stderr and handling of child process pid.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root,-)
%doc %{gem_docdir}/
%{gem_dir}/gems/%{gem_name}-%{version}/
%{gem_cache}
%{gem_spec}

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Julian C. Dunn <jdunn@aquezada.com> - 2.6.4-1
- Upgrade to 2.6.4 (bz#1072276)

* Sun Mar 02 2014 Julian C. Dunn <jdunn@aquezada.com> - 2.6.3-1
- Upgrade to 2.6.3 (bz#1066935)

* Thu Jan 23 2014 Julian C. Dunn <jdunn@aquezada.com> - 2.6.0-1
- Upgrade to 2.6.0 (bz#1039515)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.5.2-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Sat Mar 16 2013 Julian C. Dunn <jdunn@aquezada.com> - 2.5.2-3
- Unbreak build on Fedora >= 19

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Julian C. Dunn <jdunn@aquezada.com> - 2.5.2-1
- Upgrade to 2.5.2.
- Unify spec so it can be built from the same one across Fedora and EPEL.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 2.4.1-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Jeffrey Ollie <jeff@ocjtech.us> - 2.4.1-2
- Fix typo _buildroot => buildroot
- Add group

* Mon Dec  5 2011 Jeffrey Ollie <jeff@ocjtech.us> - 2.4.1-1
- First version
