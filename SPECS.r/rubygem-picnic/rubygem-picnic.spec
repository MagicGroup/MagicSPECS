%define gem_name picnic

Summary:	Easier distribution of Camping-based applications
Name:		rubygem-%{gem_name}
Version:	0.8.1
Release:	13%{?dist}
Group:		Development/Languages
License:	LGPLv3
URL:		http://rubyforge.org/projects/picnic/
Source0:	http://gems.rubyforce.org/gems/%{gem_name}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	ruby(release)
Requires: ruby(rubygems)
Requires:	rubygem(markaby)
BuildRequires: rubygems-devel
#BuildRequires:	rubygem-rake
#BuildRequires:	zip
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Picnic makes it easy(ier) to distribute and run
Camping-based applications as well-behaved stand-alone
Linux/Windows services

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}
#            --force --rdoc %{gem_name}-%{version}.gem

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
%{gem_dir}/gems/%{gem_name}-%{version}/
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.txt
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%{gem_cache}
%{gem_spec}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.8.1-13
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.8.1-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.1-11
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.1-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.1-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.8.1-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.7.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.6.5-2
- Fix license (#467347)

* Fri Oct 18 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.6.5-1
- New upstream version, package for review

* Thu Sep 18 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.6.4-1
- New upstream version, package for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 0.6.3-1
- Initial package
