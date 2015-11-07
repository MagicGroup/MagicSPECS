%global gem_name rack-accept

Summary: HTTP Accept* for Ruby/Rack
Name: rubygem-%{gem_name}
Version: 0.4.5
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/mjackson/rack-accept
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(rack)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
HTTP Accept, Accept-Charset, Accept-Encoding, and Accept-Language for
Ruby/Rack

%package doc
Summary: Documentation for %{gem_name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{gem_name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Run the tests using minitest 5.
ruby -Ilib -rminitest/autorun - << \EOF
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
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/README.md
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.4.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.5-1
- Update rack-accept 0.4.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.3-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.3-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Michal Fojtik <mfojtik@redhat.com> - 0.4.3-5
- Fixed wrong dependency name in -doc

* Thu Oct 07 2010 Michal Fojtik <mfojtik@redhat.com> - 0.4.3-4
- Removed unused macros
- Documentation and tests moved to -doc subpackage
- Removed version dependencies

* Fri Oct 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.4.3-3
- Added another BuildRequire dependency

* Fri Oct 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.4.3-2
- Fixed BuildRequire dependencies

* Fri Oct 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.4.3-1
- Initial package
