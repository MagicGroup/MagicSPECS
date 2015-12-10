%define gem_name reststop

Summary:	Convenient RESTfulness for all your Camping controller needs
Name:		rubygem-%{gem_name}
Version:	0.4.0
Release:	13%{?dist}
Group:		Development/Languages
License:	LGPLv3
URL:		http://rubyforge.org/projects/reststop/
Source0:	http://gems.rubyforge.org/gems/%{gem_name}/%{gem_name}-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	ruby(release)
Requires: ruby(rubygems)
BuildRequires: rubygems-devel
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Convenient RESTfulness for all your Camping controller needs

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

rm -rf %{buildroot}/%{gem_instdir}/.project
rm -rf %{buildroot}/%{gem_instdir}/.loadpath

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{gem_docdir}
%doc %{gem_instdir}/examples/*
%doc %{gem_instdir}/test
%doc %{gem_instdir}/CHANGELOG.txt
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%doc %{gem_instdir}/setup.rb
%doc %{gem_instdir}/History.txt
%{gem_libdir}
%{gem_cache}
%{gem_spec}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.4.0-13
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.4.0-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.0-11
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.0-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.4.0-1
- New upstream version

* Fri Oct 18 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.3.0-1
- Package for review
