%if 0%{?fedora} >= 17
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif
%else
%global	rubyabi	1.8
%endif

%global	gem_name	allison

Summary:	A modern, pretty RDoc template
Name:		rubygem-%{gem_name}
Version:	2.0.3
Release:	16%{?dist}
Group:		Development/Languages
License:	AFL
URL:		http://github.com/fauna/allison/tree/master
Source0:	http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif

BuildRequires:	rubygems-devel
Requires:	ruby(rubygems)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
%{summary}.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
popd

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

# And cleanups
rm -rf %{buildroot}%{gem_dir}/bin
rm -f %{buildroot}%{gem_instdir}/%{gem_name}.gemspec

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{gem_name}

%dir %{gem_instdir}
%doc %{gem_instdir}/[A-Z]*
%exclude %{gem_instdir}/Manifest
%{gem_instdir}/bin/
%{gem_instdir}/lib/
%{gem_instdir}/cache/
%{gem_spec}
%{gem_cache}

%files doc
%defattr(-,root,root,-)
%{gem_instdir}/Manifest
%{gem_instdir}/contrib/
%{gem_docdir}/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.3-16
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.0.3-15
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.3-14
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.3-10
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0.3-7
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-4
- F-12: Mass rebuild

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-3
- It turned out that the patch mentioned below was not needed...

* Tue Jun 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-2
- Patch to make allison work when called as %%_bindir/allison

* Tue Jun 16 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-1
- Initial package
