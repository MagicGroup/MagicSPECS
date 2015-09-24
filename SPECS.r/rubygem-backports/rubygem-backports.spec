# Generated from backports-2.5.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name backports

Name: rubygem-%{gem_name}
Version: 3.6.4
Release: 1%{?dist}
Summary: Backports of Ruby features for older Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/marcandre/backports
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Essential backports that enable many of the nice features of Ruby 1.8.7 up to
2.1.0 for earlier versions.


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
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# TODO: More test could be enabled, if MSpec and RubySpec are available
# in Fedora.

# To run the tests using minitest 5
ruby -rminitest/autorun -Ilib - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  Test = Minitest

  module Minitest::Assertions; alias :assert_raise :assert_raises; end;

  # Some test cases needs to run in order, while recent Minitest runs it in random order.
  class AAA_TestBackportGuards < MiniTest::Unit::TestCase; def self.test_order; :alpha; end; end;

  Dir.glob "./test/*_test.rb", &method(:require)
EOF

popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/backports.gemspec
%{gem_instdir}/default.mspec
%{gem_instdir}/set_version
%{gem_instdir}/spec
%{gem_instdir}/test

%changelog
* Mon Jun 22 2015 Vít Ondruch <vondruch@redhat.com> - 3.6.4-1
- Update to backports 3.6.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 Vít Ondruch <vondruch@redhat.com> - 3.6.0-1
- Update to backports 3.6.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 17 2013 Vít Ondruch <vondruch@redhat.com> - 3.3.4-1
- Update to backports 3.3.4.

* Mon Sep 02 2013 Vít Ondruch <vondruch@redhat.com> - 3.3.3-1
- Update to backports 3.3.3.

* Mon Apr 30 2012 Vít Ondruch <vondruch@redhat.com> - 2.5.1-2
- Fixed license.

* Fri Apr 27 2012 Vít Ondruch <vondruch@redhat.com> - 2.5.1-1
- Initial package
