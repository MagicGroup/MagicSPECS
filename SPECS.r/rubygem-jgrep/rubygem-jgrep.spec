%global commit 6a96698f42475975375b027b4d3bf5d8511b4a8f
%global gem_name jgrep

Name:           rubygem-%{gem_name}
Version:        1.3.3
Release:        8%{?dist}
Summary:        Query JSON structure with a matching language

Group:          Development/Tools
License:        ASL 2.0
URL:            http://jgrep.org/
Source0:        https://github.com/ploubser/JSON-Grep/archive/%{commit}/JSON-Grep-%{commit}.tar.gz
Patch0:         0001-Fix-test-run.patch
BuildArch:      noarch

BuildRequires:  rubygems-devel
%if 0%{?rhel} == 0
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(mocha)
%endif
Requires:       ruby(release) >= 1.8
Requires:       rubygems
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

# Drag in the pure Ruby implementation too, so that jruby has something to
# fall back to: https://bugzilla.redhat.com/show_bug.cgi?id=1219502
Requires:       rubygem(json_pure)

%description
JGrep is  Ruby-based CLI tool and API for parsing and displaying JSON data
using a logical expression syntax. It allows you to search a list of JSON
documents and return specific documents or values based on logical truths.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -qn JSON-Grep-%{commit}
%patch0 -p1


%build
gem build %{gem_name}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}


%if 0%{?rhel} == 0
%check
rspec -Ilib spec
%endif


%files
%{_bindir}/*
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/*.gemspec
%{gem_spec}
%doc COPYING README.markdown


%files doc
%{gem_docdir}


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.3.3-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.3-7
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May  7 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.3.3-5
- Work around JRuby woes (rh #1219502)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.3.3-3
- Disable tests on rhel

* Tue Apr 29 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.3.3-2
- Run tests (Lukas Bezdicka, #1092000)
- Fix issue with tests. (Guess adding the run was a good idea...)

* Mon Apr 28 2014 Lubomir Rintel <lkundrak@v3.sk> - 1.3.3-1
- Initial packaging
