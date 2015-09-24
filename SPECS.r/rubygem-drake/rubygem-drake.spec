# Tests disabled for now -- deps not in EPEL yet and Fedora packages
# don't seem to be recent enough
%bcond_with tests

%global gem_name drake

Name:           rubygem-%{gem_name}
Version:        0.9.2.0.3.1
Release:        4%{?dist}
Summary:        A branch of Rake supporting automatic parallelizing of tasks

Group:          Development/Tools
License:        MIT
URL:            http://quix.github.io/rake/
Source0:        http://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch

BuildRequires:  rubygems-devel
%if %with tests
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(flexmock)
BuildRequires:  rubygem(session)
BuildRequires:  rubygem(comp_tree)
%endif
Requires:       ruby(release) >= 1.8
Requires:       rubygem(comp_tree)
Requires:       rubygems
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Drake is an auto-parallelizing branch of Rake, a Make-like program
implemented in Ruby. Tasks and dependencies are specified in standard
Ruby syntax.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby >%{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec
%gem_install


%if %with tests
%check
./bin/drake test
%endif


%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
chmod 644 %{buildroot}%{gem_instdir}/lib/rake/ruby182_test_unit_fix.rb


%files
%{_bindir}/*
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/*.gemspec
%exclude %{gem_instdir}/*.rb
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/doc
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/Rakefile*
%exclude %{gem_instdir}/CHANGES*
%exclude %{gem_instdir}/MIT-LICENSE
%exclude %{gem_instdir}/TODO
%exclude %{gem_instdir}/README.rdoc
%{gem_spec}
%doc CHANGES* MIT-LICENSE TODO README.rdoc


%files doc
%{gem_docdir}


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.9.2.0.3.1-2
- Fix up bad permissions

* Mon Apr 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.9.2.0.3.1-1
- Initial packaging
