%global gem_name rack-cors

Name:           rubygem-%{gem_name}
Version:        0.4.0
Release:        2%{?dist}
Summary:        Middleware for enabling Cross-Origin Resource Sharing in Rack apps

Group:          Development/Languages
License:        MIT
URL:            https://github.com/cyu/rack-cors
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(minitest) >= 5.3.0
BuildRequires:  rubygem(mocha) >= 0.14.0
BuildRequires:  rubygem(rack-test)
%if 0%{?fedora} && 0%{?fedora} <= 20
Requires:       ruby(release)
Requires:       ruby(rubygems)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Middleware that will make Rack-based apps CORS compatible.

Read more here:
http://blog.sourcebender.com/2010/06/09/introducin-rack-cors.html.

Fork the project here: https://github.com/cyu/rack-cors.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
ruby -rminitest/autorun -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%license %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}/
%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/%{gem_name}.gemspec

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/test/


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 František Dvořák <valtri@civ.zcu.cz> - 0.4.0-1
- Update to 0.4.0 (#1212051)

* Sun Jan 04 2015 František Dvořák <valtri@civ.zcu.cz> - 0.3.1-1
- Update to 0.3.1

* Tue Dec 23 2014 František Dvořák <valtri@civ.zcu.cz> - 0.3.0-1
- Update to 0.3.0
- Update file list
- Cleanups

* Fri Oct 10 2014 František Dvořák <valtri@civ.zcu.cz> - 0.2.9-1
- Initial package
