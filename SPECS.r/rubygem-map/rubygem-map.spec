# Generated from map-5.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name map

Name: rubygem-%{gem_name}
Version: 6.5.5
Release: 3%{?dist}
Summary: String/symbol indifferent ordered hash
Group: Development/Languages
License: Ruby or BSD
URL: https://github.com/ahoward/map
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
The awesome ruby container you've always wanted: a string/symbol
indifferent ordered hash that works in all rubies.

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

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# To run the tests using minitest 5
# https://github.com/ahoward/map/issues/24
sed -i 's/assert_nothing_raised.*/result = block.call/' test/lib/testing.rb

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
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README
%{gem_instdir}/Rakefile
%{gem_instdir}/a.rb
%{gem_instdir}/test


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 6.5.5-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 6.5.5-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 6.5.5-1
- Update to map 6.5.5.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 6.5.3-1
- Update to map 6.5.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 6.3.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to Map 6.3.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 5.2.0-1
- Initial package
