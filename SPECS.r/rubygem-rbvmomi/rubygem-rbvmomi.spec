# Generated from rbvmomi-1.2.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rbvmomi


Summary: Ruby interface to the VMware vSphere API
Name: rubygem-%{gem_name}
Version: 1.8.1
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/vmware/rbvmomi
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix nokogiri 1.6.x compatibility.
# https://github.com/vmware/rbvmomi/pull/32
Patch0: rubygem-rbvmomi-1.8.1-nokogiri-attributes-workaround-support-for-1.6.x.patch
BuildRequires: ruby(release)
BuildRequires: rubygem(nokogiri) >= 1.4.1
BuildRequires: rubygem(builder)
BuildRequires: rubygem(minitest)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.7
BuildArch: noarch

%description
Ruby interface to the VMware vSphere API


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.


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

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Fix rpmlint issues.
sed -i '/#!.*env ruby/d' %{buildroot}%{gem_instdir}/devel/{benchmark,collisions}.rb

%check
pushd .%{gem_instdir}
# Run the tests using minitest 5.
ruby -Ilib:test -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  module Minitest::Assertions
    alias :assert_raise :assert_raises
  end

  Test = Minitest

  Dir.glob "./test/**/test_*.rb", &method(:require)
EOF
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{_bindir}/rbvmomish
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/vmodl.db
%exclude %{gem_instdir}/.yardopts
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/VERSION
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/devel
%{gem_instdir}/test
%doc %{gem_instdir}/examples
%{gem_instdir}/Rakefile

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.8.1-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.8.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.8.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 17 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.1-1
- Update to rbvmomi 1.8.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.3-3
- Added vmodl.db back, since it's required dependency

* Mon Jul 11 2011 Francesco Vollero <fvollero@redhat.com> - 1.2.3-2
- Fix License to MIT
- Removed the >= 0 versions from rubygems Requires
- Add Requires and BuildRequires: ruby(abi) = 1.8
- Executed the test suite.

* Tue Jun 14 2011 Francesco Vollero <fvollero@redhat.com> - 1.2.3-1
- Initial package
