# Generated from factory_girl_rails-1.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name factory_girl_rails


Summary: Provides integration between factory_girl and rails 3
Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/thoughtbot/factory_girl_rails
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
Requires: rubygem(railties) >= 3.0.0
Requires: rubygem(factory_girl) => 2.3.0
Requires: rubygem(factory_girl) < 2.4.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
# see check section below
#BuildRequires: rubygem(cucumber)
#BuildRequires: rubygem(rake)
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Provides integration between factory_girl and rails 3
(currently just automatic factory definition loading)


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

pushd .%{gem_instdir}
rm Gemfile.lock

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# remove some unecessary files
pushd %{buildroot}%{gem_instdir}
rm -rf CONTRIBUTING.md %{gem_name}.gemspec .gitignore .bundle

# this will complain about missing 'aruba' gem
#%check
#pushd %{buildroot}%{gem_instdir}
#rake features

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/features
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.0-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Mo Morsi <mmorsi@redhat.com> - 1.4.0-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Mo Morsi <mmorsi@redhat.com> - 1.4.0-1
- new upstream release

* Fri Jul 15 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.1-2
- fix license, whitespace issues, package summary

* Wed Jul 13 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- Initial package
