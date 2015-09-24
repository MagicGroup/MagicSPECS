# Generated from rdoc-3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rdoc


Summary: RDoc produces HTML and command-line documentation for Ruby projects
Name: rubygem-%{gem_name}
Version: 4.1.1
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2 and Ruby and MIT
URL: http://docs.seattlerb.org/rdoc/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(irb)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest) > 5
BuildRequires: rubygem(json) => 1.4
BuildRequires: rubygem(json) < 2
# Execute Rake integration test cases.
BuildRequires: rubygem(rake)
BuildRequires: ruby(irb)
BuildArch: noarch

%description
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the +rdoc+ and +ri+ tools for generating and displaying online
documentation.
See RDoc for a description of RDoc's markup and basic use.

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


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# There is neccessary to disable system gems to avoid conflicts with system
# RDoc and specify several paths for test dependencies manually. Let's evaluate
# them by this nice Ruby snippet.
RUBYOPT=-I`ruby <<EOF
  #specs = %w{rake minitest json psych}.map {|g| Gem::Specification.find_by_name(g)}
  specs = %w{rake minitest json}.map {|g| Gem::Specification.find_by_name(g)}
  paths = specs.map {|s| s.full_require_paths}
  puts paths.join(':')
EOF`:lib GEM_PATH= ruby - << \EOF
  # Avoid RubyGems dependency to explicitely load minitest gem.
  # https://github.com/rdoc/rdoc/issues/313
  alias orig_gem gem

  def gem(gem_name, *requirements)
    orig_gem(gem_name, requirements) unless gem_name == 'minitest'
  end

  Dir.glob "./test/**/test_*.rb", &method(:require)
EOF


popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.rdoc
%doc %{gem_instdir}/LEGAL.rdoc
%exclude %{gem_instdir}/.*
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_libdir}
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.rdoc
%doc %{gem_instdir}/Example*
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CVE-2013-0256.rdoc
%doc %{gem_instdir}/RI.rdoc
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/TODO.rdoc
%{gem_instdir}/test


%changelog
* Tue Jul 08 2014 Vít Ondruch <vondruch@redhat.com> - 4.1.1-2
- Add missing IRB dependency.

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 4.1.1-1
- Update to RDoc 4.1.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 29 2013 Vít Ondruch <vondruch@redhat.com> - 4.0.1-1
- Update to RDoc 4.0.1.

* Tue Mar 26 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-100
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to RDoc 4.0.0

* Wed Feb 06 2013 Josef Stribny <jstribny@redhat.com> - 3.12.1-2
- Encoding issue is still unresolved in upstream.

* Wed Feb 06 2013 Josef Stribny <jstribny@redhat.com> - 3.12.1-1
- Update to version 3.12.1

* Thu Sep 06 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-5
- Fix the location of Ruby documentation (rhbz#854418).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-3
- Add missing obsolete (rhbz#809007).

* Mon Feb 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-2
- Add missing IRB dependency.

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 3.12-1
- Rebuilt for Ruby 1.9.3.
- Updated to RDoc 3.12.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Mo Morsi <mmorsi@redhat.com> - 3.8-2
- Fixes for fedora compliance

* Mon Jan 10 2011 mo morsi <mmorsi@redhat.com> - 3.8-1
- Initial package
