%global gem_name openstack


Summary: Ruby Openstack Compute and Object-Store bindings
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/ruby-openstack/ruby-openstack
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# Upstream apparently does releases without runnint testsuite :(
# https://github.com/ruby-openstack/ruby-openstack/pull/40
Patch0: rubygem-openstack-1.1.2-fix-testsuite.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description

Ruby Openstack Compute and Object-Store bindings for the v1.0 OSAPI.
Currently supports both v1.0 and v2.0 (keystone) authentication.

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
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Remove shebang
sed -i -e '/^#!\//, 1d' %{buildroot}%{gem_instdir}/lib/openstack.rb

%check
pushd .%{gem_instdir}
# Run the tests using minitest 5.
ruby -rminitest/autorun -rmocha/setup - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  module Minitest::Assertions
    alias :assert_not_nil :refute_nil
  end

  Test = Minitest

  Dir.glob "./test/**/*_test.rb", &method(:require)
EOF
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%{gem_libdir}
%exclude %{gem_instdir}/.yardoc
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/test

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.2-1
- Update to OpenStack 1.1.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.9-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Feb 13 2013 Michal Fojtik <mfojtik@redhat.com> 1.0.9-1
- Version bump

* Wed Feb 06 2013 Michal Fojtik <mfojtik@redhat.com> 1.0.8-1
- Version bump

* Thu Sep 13 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.6-1
- Fixed problem with gemspec

* Thu Sep 13 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.5-2
- Removed %%doc prefix from VERSION
- Removed test-unit dependecy from BuildRequire

* Thu Sep 13 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.5-1
- Version bump
- Included tests

* Thu Sep 13 2012 Michal Fojtik <mfojtik@redhat.com> 1.0.4-1
- Initial release
