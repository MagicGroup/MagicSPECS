%global gem_name facets

Name:           rubygem-%{gem_name}
Summary:        The single most extensive additions and extensions library available for Ruby
Version:        2.8.0
Release:        12%{?dist}
Group:          Development/Languages
License:        Ruby
URL:            http://rubyforge.org/projects/facets/
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Requires:       ruby(release)
Requires:       ruby(rubygems)
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(rake)
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
The single most extensive additions and extensions library available for Ruby

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
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{gem_instdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{gem_instdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

# Remove hidden files
rm -rf %{buildroot}/%{gem_instdir}/.require_paths

%check
pushd %{buildroot}/%{gem_instdir}
rake test || :
popd

%files
%dir %{gem_instdir}/
%doc %{gem_docdir}
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/AUTHORS
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/HISTORY.rdoc
%doc %{gem_instdir}/MANIFEST
%doc %{gem_instdir}/NOTES
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/demo/
%doc %{gem_instdir}/meta/
%{gem_libdir}
%{gem_instdir}/test/
%{gem_instdir}/script/
%exclude %{gem_cache}
%{gem_spec}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.8.0-12
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.8.0-11
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.8.0-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Vít Ondruch <vondruch@redhat.com> - 2.8.0-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.8.0-2
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.5.1-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.5.0-1
- New upstream version

* Sun Oct 25 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.4.5-2
- Fix %%doc files

* Sat Oct 25 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.4.5-1
- Initial package
