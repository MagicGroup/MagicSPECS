# Generated from apipie-bindings-0.0.10.gem by gem2rpm -*- rpm-spec -*-
%global gem_name apipie-bindings

# Tests are disable for now due to missing rubygem(minitest-spec-context)
%{!?enable_test: %global enable_test 0}

Name: rubygem-%{gem_name}
Version: 0.0.14
Release: 1%{?dist}
Summary: The Ruby bindings for Apipie documented APIs
Group: Development/Languages
License: MIT
URL: http://github.com/Apipie/apipie-bindings
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(json) >= 1.2.1
Requires: rubygem(rest-client) >= 1.6.5
Requires: rubygem(oauth)
Requires: rubygem(awesome_print)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if 0%{enable_test}
BuildRequires: rubygem(awesome_print)
BuildRequires: rubygem(minitest) < 5
#BuildRequires: rubygem(minitest-spec-context)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(oauth)
BuildRequires: rubygem(rest-client)
%endif
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Bindings for API calls that are documented with Apipie. Bindings are generated
on the fly.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%if 0%{enable_test}
%check
pushd .%{gem_instdir}
# We don't care about code coverage.
sed -i '/require.*simplecov/ s/^/#/' test/unit/test_helper.rb
sed -i '/SimpleCov/,/SimpleCov\.root/ s/^/#/' test/unit/test_helper.rb

ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd
%endif


%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/doc
%{gem_instdir}/test
%exclude %{gem_instdir}/test/dummy/.gitignore

%changelog
* Wed Aug 26 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.14-1
- Update to apipie-bindings 0.0.14.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 2 2015 Steve Traylen <steve.traylen@cern.ch> - 0.0.13-1
- Update 0.0.13.

* Mon Mar 23 2015 Steve Traylen <steve.traylen@cern.ch> - 0.0.12-1
- Update 0.0.12.

* Fri Sep 26 2014 Steve Traylen <steve.traylen@cern.ch> - 0.0.10-2
- Specify gem requirement version limits.

* Fri Sep 19 2014 Steve Traylen <steve.traylen@cern.ch> - 0.0.10-1
- Initial package
