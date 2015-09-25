%global gem_name pr_geohash

Summary: GeoHash encode/decode library for pure Ruby
Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 13%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/masuidrive/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest) > 5
BuildArch: noarch

%description
GeoHash encode/decode library for pure Ruby.
It's implementation of http://en.wikipedia.org/wiki/Geohash


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

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

rm %{buildroot}/%{gem_instdir}/.autotest
rm %{buildroot}/%{gem_instdir}/Manifest.txt

%check
pushd .%{gem_instdir}
# To run the tests using minitest 5
ruby -Ilib -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end

  end

  Test = Minitest

  Dir.glob "./test/**/test_*.rb", &method(:require)
EOF
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/README.rdoc
%{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.0-13
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 18 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.0-11
- Fix FTBFS in Rawhide (rhbz#1107197).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 20 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.0-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.0-2
- Removed unnecessary version information.

* Thu Jan 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
