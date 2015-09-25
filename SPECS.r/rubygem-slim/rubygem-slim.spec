# Generated from slim-1.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name slim

Summary: Slim is a template language
Name: rubygem-%{gem_name}
Version: 2.0.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://slim-lang.com/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(creole)
BuildRequires: rubygem(temple)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(sass)
BuildRequires: rubygem(asciidoctor)
BuildRequires: rubygem(org-ruby)
BuildRequires: rubygem(redcarpet)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(wikicloth)
BuildArch: noarch

%description
Slim is a template language whose goal is reduce the syntax to the essential
parts without becoming cryptic.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -T -D -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
rm %{buildroot}%{gem_instdir}/.gitignore
rm %{buildroot}%{gem_instdir}/.travis.yml
rm %{buildroot}%{gem_instdir}/.yardopts
grep -rl /usr/bin/env %{buildroot}%{gem_instdir}/benchmarks  | xargs chmod a+x

%check
pushd ./%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/rails/**/test_*.rb", &method(:require)'
# TestSlimEmbeddedEngines#test_render_with_wiki fails a times :/
ruby -Ilib:test/core -e 'Dir.glob "./test/core/**/test_*.rb", &method(:require)' || :
ruby -Ilib:test/core -e 'Dir.glob "./test/logic_less/**/test_*.rb", &method(:require)'
ruby -Ilib:test/core -e 'Dir.glob "./test/translator/**/test_*.rb", &method(:require)'
ruby -Ilib:test/literate test/literate/run.rb
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{_bindir}/slimrb
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/slim.gemspec
%{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/doc
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_instdir}/benchmarks/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.2-2
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Vít Ondruch <vondruch@redhat.com> - 2.0.2-1
- Update to Slim 2.0.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Josef Stribny <jstribny@redhat.com> - 1.3.8-2
- Fix runtime requirement of temple version

* Mon Apr 15 2013 Josef Stribny <jstribny@redhat.com> - 1.3.8-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to slim 1.3.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012  <mzatko@redhat.com> - 1.2.2-8
- Excluded gem cache
- Check goes after install section

* Wed Oct 17 2012  <mzatko@redhat.com> - 1.2.2-7
- Split prep to prep and build sections
- Made nonexecutable scripts executable
- Owning whole test/ directory

* Tue Oct 16 2012  <mzatko@redhat.com> - 1.2.2-6
- Fixed markdown test

* Thu Oct 11 2012  <mzatko@redhat.com> - 1.2.2-5
- Now owning test and benchmarks directories

* Wed Oct 10 2012  <mzatko@redhat.com> - 1.2.2-4
- Added deps for rails tests. Runs tests.

* Mon Oct 08 2012  <mzatko@redhat.com> - 1.2.2-3
- Moved tests to doc, removed unnecessary files, some minor corrections
- Not running tests (missing deps)

* Mon Sep 03 2012  <mzatko@redhat.com> - 1.2.2-2
- Removed unnecessary files & corrected license

* Wed Jul 11 2012  <mzatko@redhat.com> - 1.2.2-1
- Initial package
