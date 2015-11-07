# Generated from ref-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ref

Summary: Library that implements weak, soft, and strong references in Ruby
Name: rubygem-%{gem_name}
Version: 1.0.5
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/bdurand/ref
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Library that implements weak, soft, and strong references in Ruby that work
across multiple runtimes (MRI, REE, YARV, Jruby, Rubinius, and IronRuby). Also
includes implementation of maps/hashes that use references and a reference
queue.


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
pushd .%{gem_instdir}
# To run the tests using minitest 5
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
%doc %{gem_instdir}/MIT_LICENSE
%dir %{gem_instdir}
%exclude %{gem_instdir}/ext
%{gem_libdir}
%exclude %{gem_libdir}/org
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/VERSION
%{gem_instdir}/test
%exclude %{gem_instdir}/test/*.rbc

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Update to ref 1.0.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
