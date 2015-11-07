# Generated from haml-rails-0.3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name haml-rails


Summary: Haml-rails provides Haml generators for Rails 3
Name: rubygem-%{gem_name}
Version: 0.5.3
Release: 5%{?dist}
Group: Development/Languages
License: MIT or Ruby
URL: http://github.com/indirect/haml-rails
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(railties) => 3.0
BuildRequires: rubygem(activerecord) => 3.0
BuildRequires: rubygem(actionmailer) => 3.0
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Haml-rails provides Haml generators for Rails 3. It also enables Haml as the
templating engine for you, so you don't have to screw around in your own
application.rb when your Gemfile already clearly indicated what templating
engine you have installed. Hurrah.


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
# To run with Minitest 5
ruby -rminitest/autorun -rrubygems -rshellwords -Itest - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end
  Test = Minitest
  Dir.glob "./test/lib/generators/haml/*_test.rb", &method(:require)
EOF
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%doc %{gem_docdir}
%{gem_instdir}/haml-rails.gemspec
%{gem_instdir}/test
%{gem_instdir}/gemfiles
%{gem_instdir}/Gemfile
%{gem_instdir}/Appraisals

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.3-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.3-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Josef Stribny <jstribny@redhat.com> - 0.5.3-1
- Update to haml-rails 0.5.3

* Mon Aug 12 2013 Josef Stribny <jstribny@redhat.com> - 0.4-1
- Update to haml-rails 4.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-10
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-8
- Rebuild with new Haml.
- Fix tests failing with Rails 3.2.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-4
- Removed unused testdir macro
- haml-rails.gemspec is no longer marked as document

* Tue Sep 13 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-3
- Removed Requires: activesupport and actionpack (they install with railties)

* Tue Sep 13 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-2
- Improved the test section
- Fixed BuildRequires not to require rails, but railties, actiomailer and activerecord
- Moved tests and Gemfile to doc subpackage

* Mon Sep 12 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-1
- Initial package
