%define gem_name markaby

Summary:        Markup as Ruby, write HTML in your native Ruby tongue
Name:           rubygem-%{gem_name}
Version:        0.5
Release:        14%{?dist}
Group:          Development/Languages
License:        GPLv2+ or Ruby
URL:            http://markaby.github.com/markaby/
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires:	ruby(release)
Requires:       rubygem(builder) >= 2.0.0
BuildRequires: rubygems-devel
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
Markup as Ruby, write HTML in your native Ruby tongue

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_dir}/gems/%{gem_name}-%{version}/
%doc %{gem_docdir}
%doc %{gem_instdir}/README
%{gem_cache}
%{gem_spec}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.5-14
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5-13
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5-10
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.5-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.5-2
- Add required ruby(abi) = 1.8 requirement

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 0.5-1
- Initial package
