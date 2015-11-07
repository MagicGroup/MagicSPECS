%define gem_name arrayfields

Name: 		rubygem-%{gem_name}
Summary: 	Arrayfields RubyGem
Version: 	4.7.4
Release: 	12%{?dist}
Group:		Development/Languages
License: 	GPLv2+ or Ruby
URL: 		http://codeforpeople.com/lib/ruby/%{gem_name}/
Source0: 	http://codeforpeople.com/lib/ruby/%{gem_name}/%{gem_name}-%{version}/%{gem_name}-%{version}.gem

BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: 	noarch
Provides: 	rubygem(%{gem_name}) = %{version}

%description
Arrayfields RubyGem

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

# Remove backup files
find %{buildroot}/%{gem_instdir} -type f -name "*~" -delete

# Delete zero-length files
find %{buildroot}/%{gem_instdir} -type f -size 0c -exec rm -rvf {} \;

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gem_docdir}/
%doc %{gem_instdir}/README
%doc %{gem_instdir}/sample
%doc %{gem_instdir}/test
%dir %{gem_dir}/gems/%{gem_name}-%{version}/
%{gem_dir}/gems/%{gem_name}-%{version}/*.rb
%{gem_dir}/gems/%{gem_name}-%{version}/lib
%{gem_dir}/gems/%{gem_name}-%{version}/%{gem_name}.gemspec
%{gem_cache}
%{gem_spec}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.7.4-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.7.4-11
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 4.7.4-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 4.7.4-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 4.7.4-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 4.7.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 4.5.0-3
- Rebuild with README marked as docfor review (#457026)

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 4.5.0-2
- Rebuild for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 4.5.0-1
- Initial package
