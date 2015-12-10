%define gem_name pervasives

Summary:        Access to pristine object state
Name:           rubygem-%{gem_name}
Version:        1.1.0
Release:        16%{?dist}
Group:          Development/Languages
License:        Ruby
URL:            http://codeforpeople.com/lib/ruby/pervasives/
Source0:        http://rubyforge.org/frs/download.php/25796/%{gem_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires:       ruby(release)
BuildRequires: rubygems-devel
BuildRequires:  rubygem(rake)
BuildRequires:  zip
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
Access to pristine object state. If you don't metaprogram or write
debuggers you probably don't need it.

%prep
%setup -q -n %{gem_name}-%{version}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{gem_name}-%{version}.gem -d %{buildroot}%{gem_dir}

chmod ugo+x %{buildroot}/%{gem_dir}/gems/%{gem_name}-%{version}/install.rb

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gem_instdir}
%doc %{gem_dir}/gems/%{gem_name}-%{version}/README
%doc %{gem_docdir}
%{gem_cache}
%{gem_spec}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.0-16
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.0-15
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-14
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.0-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.0-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.1.0-3
- Fix license

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.1.0-2
- Added ruby(abi) = 1.8 requirement

* Sat Aug 23 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.1.0-1
- Initial packaging for review
