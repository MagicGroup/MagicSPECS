%global gem_name sinatra-rabbit

Summary: Ruby DSL for creating restful applications using Sinatra
Name: rubygem-%{gem_name}
Version: 1.1.6
Release: 5%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/mifo/sinatra-rabbit
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(sinatra)
Requires: rubygem(haml)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack-test)
BuildRequires: rubygem(nokogiri)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description

Sinatra::Rabbit is a Sinatra extensions that makes designing a REST API much
easier and more fun.
Rabbit maps REST resources to 'collections'. Every collection then could define
CRUD and other operations to manipulate with resource. Rabbit will handle
parameter validation and capability checks for you, so you can focus on the
structure and design of your REST API.

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
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
# Tests disabled for now because of bug in Fedora minitest
#
#pushd .%{gem_instdir}
#for test_file in tests/*_test.rb; do
#  testrb $test_file
#done
#popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/.yardoc
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/tests

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.6-5
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Michal Fojtik <mfojtik@redhat.com> - 1.1.6-1
- New release (1.1.6)

* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.4-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> 1.1.4-1
- New release (1.1.4)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Michal Fojtik <mfojtik@redhat.com> 1.1.2-1
- New release (1.1.2)

* Fri Sep 14 2012 Michal Fojtik <mfojtik@redhat.com> 1.1.0-1
- New release (1.1.0)

* Tue Jul 10 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.9-1
- New release (1.0.9)
* Tue Jul 10 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.8-1
- New release (1.0.8)

* Mon Jun 04 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.6-2
- Added exclude tag before gem_cache
- Removed the ruby dependency

* Mon Jun 04 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.6-1
- Initial import

