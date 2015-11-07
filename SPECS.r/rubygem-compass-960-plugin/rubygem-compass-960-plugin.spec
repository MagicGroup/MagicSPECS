# Generated from compass-960-plugin-0.10.4.gem by gem2rpm -*- rpm-spec -*-
%define gem_name compass-960-plugin


Summary: Compass compatible Sass port of 960.gs
Name: rubygem-%{gem_name}
Version: 0.10.4
Release: 11%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/chriseppstein/compass-960-plugin
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(compass) >= 0.10.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
The 960 Grid System is an effort to streamline web development workflow by
providing commonly used dimensions, based on a width of 960 pixels.
http://960.gs/

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/


%files
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}
%{gem_cache}
%{gem_spec}


%files doc
%doc %{gem_instdir}/README.mkdn
%doc %{gem_docdir}


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.10.4-11
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.4-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 0.10.4-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.10.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Chris Lalancette <clalance@redhat.com> - 0.10.4-1
- Initial package
