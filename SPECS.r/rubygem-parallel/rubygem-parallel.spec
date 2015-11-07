%global gem_name parallel
%global with_tests 1

Summary:       Run any kind of code in parallel processes
Name:          rubygem-%{gem_name}
Version:       1.3.3
Release:       4%{?dist}
Group:         Development/Languages
License:       MIT
URL:           https://github.com/grosser/parallel
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream has removed spec test from gem.
# This is how we are getting the tests (Source2)
#  git clone https://github.com/grosser/parallel.git
#  cd parallel
#  git checkout v1.3.3
#  tar cfz parallel-1.3.3-spec.tgz spec/ Rakefile
Source1:       %{gem_name}-%{version}-spec.tgz
Patch1:        rubygem-parallel-1.3.3-fix-tests.patch
Requires:      ruby(release)
Requires:      ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{?with_tests}
BuildRequires: lsof
BuildRequires: procps-ng
BuildRequires: rubygem-rspec
BuildRequires: rubygem-bundler
%endif
BuildArch:     noarch
Provides:      rubygem(%{gem_name}) = %{version}

%description
Run any code in parallel Processes(use all CPUs) 
or Threads(speedup blocking operations).
Best suited for map-reduce or e.g. parallel downloads/uploads.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

tar -xzf %{SOURCE1}

%patch1 -p1

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
%if 0%{?with_tests}
rspec -Ilib spec
%endif

%files
%doc %{gem_instdir}/MIT-LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.3-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.3-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 27 2014 Troy Dawson <tdawson@redhat.com> - 1.3.3-1
- Updated to latest release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Troy Dawson <tdawson@redhat.com> - 1.0.0-1
- Update to version 1.0.0

* Mon Feb 17 2014 Troy Dawson <tdawson@redhat.com> - 0.9.2-3
- More test fixups

* Fri Feb 14 2014 Troy Dawson <tdawson@redhat.com> - 0.9.2-2
- Fix test Buildrequires

* Wed Feb 12 2014 Troy Dawson <tdawson@redhat.com> - 0.9.2-1
- Update to 0.9.2
- Fix tests

* Mon Jan 13 2014 Troy Dawson <tdawson@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Thu Oct 17 2013 Troy Dawson <tdawson@redhat.com> - 0.8.4-2
- Included spec directory for testing

* Tue Oct 08 2013 Troy Dawson <tdawson@redhat.com> - 0.8.4-1
- Initial package
