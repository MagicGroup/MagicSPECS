# Generated from main-2.8.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name main

Summary:        A class factory and dsl for generating command line programs real quick
Name:           rubygem-%{gem_name}
Version:        6.0.0
Release:        4%{?dist}
Group:          Development/Languages
License:        BSD or Ruby
URL:            https://github.com/ahoward/main
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(arrayfields)
BuildRequires:  rubygem(fattr)
BuildRequires:  rubygem(map)
BuildRequires:  rubygem(chronic)
BuildRequires:  rubygem(test-unit)
BuildArch:      noarch

%description
A class factory and dsl for generating command line programs real quick.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%check
pushd .%{gem_instdir}/test
ruby main_test.rb
popd

%clean
rm -rf %{buildroot}

%files
%dir %{gem_instdir}/
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/a.rb
%doc %{gem_instdir}/README
%{gem_instdir}/main.gemspec
%{gem_instdir}/README.erb
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/TODO
%{gem_instdir}/samples
%{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 6.0.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 6.0.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 09 2014 Vít Ondruch <vondruch@redhat.com> - 6.0.0-1
- Update to main 6.0.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Josef Stribny <jstribny@redhat.com> - 4.7.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 4.7.0-1
- Rebuilt for Ruby 1.9.3.
- Updated to version 4.7.0 (and altered the dependencies properly).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 25 2009 Jeroen van Meeuwen <kanarip@kanarip.com> - 4.0.0-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.8.4-2
- Add requirement for rubygem(fattr) (Brenton Leanhardt)

* Sat Jun 06 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.8.4-1
- New upstream version

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.8.3-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.8.2-3
- Fix license (#459886)

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.8.2-2
- Add ruby(abi) = 1.8 requirement

* Sat Aug 23 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.8.2-1
- New version
- Submit for review

* Tue Jul 15 2008 Matt Hicks <mhicks@localhost.localdomain> - 2.8.0-1
- Initial package
