# Generated from colored-1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name colored

Summary: Extends ruby string class in order to colorize terminal output
Name: rubygem-%{gem_name}
Version: 1.2
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/defunkt/colored
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Rubygem extending the ruby string class to include methods that generates
colored terminal output.

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
pushd ./%{gem_instdir}
# Run the tests using minitest 5.
ruby -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  Test = Minitest

  Dir.glob "./test/**/*_test.rb", &method(:require)
EOF
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%exclude %{gem_cache}
%{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/README
%{gem_instdir}/Rakefile
%{gem_instdir}/test/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Vít Ondruch <vondruch@redhat.com> - 1.2-9
- Fix FTBFS in Rawhide (rhbz#1107090).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012  <mzatko@redhat.com> - 1.2-4
- Owning test directory

* Mon Oct 08 2012  <mzatko@redhat.com> - 1.2-3
- Renamed specfile, corrected summary/description
- Moved tests to doc, not excluding gem_cache
- Runs tests

* Mon Sep 03 2012  <mzatko@redhat.com> - 1.2-2
- Removed unnecessary files, corrected license

* Wed Jul 11 2012  <mzatko@redhat.com> - 1.2-1
- Initial package
