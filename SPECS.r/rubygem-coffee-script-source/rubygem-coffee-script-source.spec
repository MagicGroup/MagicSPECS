# Generated from coffee-script-source-1.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name coffee-script-source

%global coffee_script_version 1.6.3
%global coffee_script_require coffee-script-common = %{coffee_script_version}


Summary:        The CoffeeScript Compiler
Name:           rubygem-%{gem_name}
Version:        %{coffee_script_version}
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://jashkenas.github.com/coffee-script/
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:       %{coffee_script_require}
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  %{coffee_script_require}
BuildArch:      noarch

%description
CoffeeScript is a little language that compiles into JavaScript.
Underneath all of those embarrassing braces and semicolons,
JavaScript has always had a gorgeous object model at its heart.
CoffeeScript is an attempt to expose the good parts of JavaScript
in a simple way.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Un-bundle coffee-script.js.
ln -sf %{_datadir}/coffee-script/extras/coffee-script.js \
  %{buildroot}%{gem_libdir}/coffee_script/coffee-script.js


%check
# No test suite included. Some tests are included in rubygem-coffee-script,
# which is the only consumer of this package.


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.6.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 23 2014 Vít Ondruch <vondruch@redhat.com> - 1.6.3-1
- Update to coffee-script-source 1.6.3.
- Un-bundle coffee-script.js.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to the coffee-script-source 1.6.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.3-1
- Updated to the coffee-script-source 1.3.3.

* Wed Feb 29 2012 Fotios Lindiakos <fotios@redhat.com> - 1.2.0-2
- Rebuilt with new gem_* macros

* Mon Feb 27 2012 Fotios Lindiakos <fotios@redhat.com> - 1.2.0-1
- Initial package
