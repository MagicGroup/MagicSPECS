%define gem_name hawler

Summary:        Hawler, the ruby HTTP crawler
Name:           rubygem-%{gem_name}
Version:        0.3
Release:        14%{?dist}
Group:          Development/Languages
License:        BSD
URL:            http://spoofed.org/files
Source0:        http://spoofed.org/files/hawler/gems/%{gem_name}-%{version}.gem
# From http://spoofed.org/files/hawler/src/COPYING
Source1:        rubygem-hawler.COPYING
Patch0:         rubygem-hawler-0.3.4-fix-tests.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(release)
Requires: ruby(rubygems)
Requires:       rubygem(hpricot)
BuildRequires: rubygems-devel
BuildRequires:  rubygem(hpricot)
BuildRequires:  rubygem(minitest)
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
Hawler, the Ruby HTTP crawler. Written to ease satisfying
curiousities about the way the web is woven.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

pushd %{buildroot}/%{gem_instdir}
patch -p0 < %{PATCH0}
popd

install -p -m644 %{SOURCE1} %{buildroot}/%{gem_instdir}/COPYING

# Remove backup files
find %{buildroot}/%{gem_instdir} -type f -name "*~" -delete

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{gem_instdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{gem_instdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

# Remove these hidden files
rm -rf %{buildroot}/%{gem_instdir}/.project
rm -rf %{buildroot}/%{gem_instdir}/.loadpath

%check
pushd %{buildroot}/%{gem_instdir}
ruby test/ts_hawlee.rb || :
ruby test/ts_hawlerhelper.rb || :
ruby test/ts_hawler.rb || :
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gem_docdir}
%{gem_cache}
%{gem_spec}
%dir %{gem_instdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/COPYING
%{gem_libdir}/
%{gem_instdir}/test/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3-14
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Josef Stribny <jstribny@redhat.com> - 0.3-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.3-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov  1 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-5
- Fix tests (mtasaka, #530204)
- Add requirement for rubygem-hpricot

* Sun Oct 25 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-4
- License is BSD
- Included License file
- Updated description
- Enabled tests

* Wed Oct 21 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-2
- The license is actually unknown to me

* Sat Oct 17 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.3-1
- First package
