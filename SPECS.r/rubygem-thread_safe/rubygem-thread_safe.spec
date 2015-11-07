# Generated from thread_safe-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name thread_safe

Name: rubygem-%{gem_name}
Version: 0.3.5
Release: 4%{?dist}
Summary: Thread-safe collections and utilities for Ruby
Group: Development/Languages
# jsr166e.LondAdder, jsr166e.Striped64, jsr166e.ConcurrentHashMapV8
# and their Ruby ports are Public Domain
License: ASL 2.0 and Public Domain
URL: https://github.com/ruby-concurrency/thread_safe
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch0 sent upstream at
# https://github.com/ruby-concurrency/thread_safe/pull/13
Patch0: rubygem-thread_safe-0.3.5-optional-deps.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(atomic)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A collection of data structures and utilities to make thread-safe
programming in Ruby easier.


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

# Remove dependency on simplecov and coveralls:
%patch0 -p1

# Remove dependency on minitest-reporters:
sed -i -e "/minitest\/reporters/d" test/test_helper.rb
sed -i -e "/Minitest::Reporters/d" test/test_helper.rb

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd ./%{gem_instdir}
# Skip test_cache_loops.rb for MRI
# Apparantly still an issue on Ruby 2.0.0p247 (2013-06-27 revision 41674)
# http://bugs.ruby-lang.org/issues/8305
#
# Skip test_hash.rb for MRI
# MRI issue/behaviour since thread_safe doesn't really modify MRI's Hash
# https://github.com/headius/thread_safe/issues/10
ruby -Ilib -e \
  'Dir.glob "./test/test_{array,cache,helper,synchronized_delegator}.rb", &method(:require)'

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%license %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/ext
%exclude %{gem_instdir}/.travis.yml

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/examples
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/tasks
%{gem_instdir}/test
%{gem_instdir}/yard-template
%exclude %{gem_instdir}/.yardopts


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.3.5-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.5-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.5-1
- Update to 0.3.5
- New upstream URL.
- Remove extraneous BR: ruby. This is covered by BR: ruby(release).
- Patch to make simplecov and coveralls optional dependencies.
- Remove optional minitest/reporters dependency.
- Drop Rakefile shebang removal. This is fixed upstream.
- Use %%license macro.

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Josef Stribny <jstribny@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Feb 04 2014 Josef Stribny <jstribny@redhat.com> - 0.1.3-3
- Add Public Domain to licenses

* Mon Jan 27 2014 Josef Stribny <jstribny@redhat.com> - 0.1.3-2
- Fix license

* Wed Oct 30 2013 Josef Stribny <jstribny@redhat.com> - 0.1.3-1
- Update to thread_safe 0.1.3

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-3
- Remove shebang from Rakefile
- Add BR: rubygem(atomic)

* Mon Jul 29 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-2
- Remove JRuby for now

* Fri Jul 26 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Add JRuby support

* Thu May 09 2013 Josef Stribny <jstribny@redhat.com> - 0.1.0-1
- Initial package
