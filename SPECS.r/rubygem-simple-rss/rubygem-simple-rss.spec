%global gem_name simple-rss

Summary: A simple, flexible, extensible, and liberal RSS and Atom reader for Ruby
Name: rubygem-%{gem_name}
Version: 1.2.3
Release: 10%{?dist}
Group: Development/Languages
License: LGPLv2+
URL: http://rubyforge.org/projects/simple-rss
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems), ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A simple, flexible, extensible, and liberal RSS and Atom reader for Ruby. It
is designed to be backwards compatible with the standard RSS parser, but will
never do RSS generation.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}


%clean
rm -rf %{buildroot}

%check
cd %{buildroot}%{gem_instdir}
#rake test

%files
%defattr(-,root,root,-)
%dir %{gem_instdir}/
%doc %{gem_docdir}
%doc %{gem_instdir}/[A-Z]*
%{gem_instdir}/[a-z]*
%{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.3-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.3-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 04 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.3
- New version

* Sat Apr 10 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.2-1
- New version 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.1-4
- More fixes from review

* Sun Jan 25 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.1-3
- One more doc update for review

* Sat Jan 10 2009 Michael Stahnke <stahnma@fedoraproject.org> - 1.1-2
- Spec updates per review

* Thu Nov 13 2008 Michael Stahnke <stahnma@fedoraproject.org> - 1.1-1
- Initial package
