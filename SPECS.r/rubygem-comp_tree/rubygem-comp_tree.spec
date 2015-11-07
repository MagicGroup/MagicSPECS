%global gem_name comp_tree

Name:           rubygem-%{gem_name}
Version:        1.1.3
Release:        6%{?dist}
Summary:        A simple framework for automatic parallelism

Group:          Development/Libraries
License:        MIT
URL:            http://quix.github.io/comp_tree/
Source0:        http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# https://github.com/quix/comp_tree/pull/1
Patch1:         0001-Make-it-work-with-Minitest-5.patch
Patch2:         0002-Make-tests-work-with-Rake-10.patch
Patch3:         0003-Fix-throw_test-test.patch
Patch4:         0004-Fix-run-with-Minitest-5.patch
BuildArch:      noarch

BuildRequires:  rubygems-devel
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rake)
Requires:       ruby(release) >= 1.8
Requires:       rubygems
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
CompTree is a parallel computation tree structure based upon concepts from
pure functional programming.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
gem spec %{SOURCE0} -l --ruby >%{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
rake test


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/devel
%exclude %{gem_cache}
%exclude %{gem_instdir}/*.rdoc
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/Rakefile
%{gem_spec}
%doc *.rdoc


%files doc
%{gem_docdir}


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.3-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.3-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.1.3-2
- Fix test run

* Mon Apr 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.1.3-1
- Initial packaging
