%define gem_name attributes

Name:		rubygem-%{gem_name}
Summary: 	Attributes RubyGem
Version: 	5.0.1
Release: 	15%{?dist}
Group: 		Development/Languages
License:	GPLv2+ or Ruby
URL: 		http://codeforpeople.com/lib/ruby/%{gem_name}/
Source0:	http://codeforpeople.com/lib/ruby/%{gem_name}/%{gem_name}-%{version}.gem
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Attributes RubyGem

%prep

%build

%install
rm -rf %{buildroot}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

chmod +x %{buildroot}/%{gem_instdir}/install.rb

# Remove zero-length file
rm -rf %{buildroot}/%{gem_instdir}/%{gem_name}-%{version}.gem

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gem_dir}/gems/%{gem_name}-%{version}/README
%doc %{gem_docdir}/
%{gem_dir}/gems/%{gem_name}-%{version}/
%{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 5.0.1-15
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 5.0.1-12
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 5.0.1-9
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 12 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 5.0.1-6
- Rebuild for FTBFS (#539108)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 5.0.1-3
- Rebuild for review (#457030)

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 5.0.1-1
- Initial package
