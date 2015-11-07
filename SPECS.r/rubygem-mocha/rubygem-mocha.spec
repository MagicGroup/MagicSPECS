%global gem_name mocha


Summary:        Mocking and stubbing library
Name:           rubygem-%{gem_name}
Version:        1.1.0
Release:        4%{?dist}
Group:          Development/Languages
License:        MIT or Ruby or BSD
URL:            http://gofreerange.com/mocha/docs
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix Ruby 2.2 test suite compatibility.
# https://github.com/freerange/mocha/commit/a65ea1ed3dce43cbc2cc16b3660afd2cce3db33e
Patch0:         rubygem-mocha-1.1.0-As-of-Ruby-v2.2-nil-is-frozen-so-these-tests-are-irrelevant.patch
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(metaclass)
BuildRequires:  rubygem(introspection)
BuildRequires:  rubygem(minitest)
BuildArch:      noarch

%description
Mocking and stubbing library with JMock/SchMock syntax, which allows mocking
and stubbing of methods on real (non-mock) classes.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check 
pushd .%{gem_instdir}
# Each part of test suite must be run separately, otherwise the test suite fails.
# https://github.com/freerange/mocha/issues/121
ruby -e "Dir.glob('./test/{unit,acceptance}/**/*_test.rb').each {|t| require t}"
ruby -e "Dir.glob('./test/integration/**/*_test.rb').each {|t| require t}"
popd

%files
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/init.rb
%doc %{gem_instdir}/COPYING.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/MIT-LICENSE.md
%doc %{gem_instdir}/RELEASE.md
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Gemfile*
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Rakefile
%{gem_instdir}/mocha.gemspec
%{gem_instdir}/gemfiles/
%{gem_instdir}/test/
%{gem_instdir}/yard-templates/


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to Mocha 1.1.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.14.0-1
- Update to 0.14.0
- Run unit and acceptance tests in a single process
- Patch test suite to work outside rake/bundler

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.13.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Vít Ondruch <vondruch@redhat.com> - 0.13.1-1
- Updated to the Mocha 0.13.1.

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.12.1-1
- Update to Mocha 0.12.1, as this version is needed by ActionPack 3.2.6 tests.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.11.0-1
- Updated to the Mocha 0.11.0.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.10.0-3
- Rebuild for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.10.0-1
- Updated to the Mocha 0.10.0.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 29 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.9.8-1
- Fixed odd naming in BR
- Updating to 0.9.8
- Breaking into -doc package as well
- Adding tests

* Thu Jul 23 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.7-1
- New upstream version

* Mon Apr 27 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.5-1
- New upstream version

* Sun Feb 01 2009 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-4
- Mark files as %%doc

* Thu Oct 30 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-3
- Use gem instead of tgz

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-2
- Fix license

* Sat Oct 25 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.1-1
- New upstream version
- Fix license not being marked as %%doc

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-2
- Add ruby(abi) = 1.8 requirement

* Sat Aug 23 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 0.9.0-1
- New upstream version
- Initial package for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 0.5.6-1
- Initial package
