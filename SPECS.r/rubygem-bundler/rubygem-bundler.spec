%global gem_name bundler

%{!?enable_test: %global enable_test 0}

# Macro for symlinking system RubyGems as a replacement for removed vendored libs
%global symlink_vendored_libs \
for dependency in \\\
  net-http-persistent \\\
  thor \
do \
  for fileordir in \\\
    %{gem_dir}/gems/$dependency-*/lib/* \
  do \
    ln -s -f $fileordir -t %{gem_libdir}/bundler/vendor/ \
  done \
done

Summary: Library and utilities to manage a Ruby application's gem dependencies
Name: rubygem-%{gem_name}
Version: 1.7.8
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://gembundler.com
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
# These dependencies are originally vendored, not specified in gemspec
# and therefore not auto-generated
Requires: rubygem(thor)
Requires: rubygem(net-http-persistent)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if 0%{enable_test} > 0
BuildRequires: ruby-devel
BuildRequires: rubygem(rspec) >= 3.0
BuildRequires: rubygem(thor)
BuildRequires: rubygem(net-http-persistent)
#BuildRequires: rubygem(psych)
#BuildRequires: git snv sudo
BuildRequires: git sudo
%endif
BuildArch: noarch

%description
Bundler manages an application's dependencies through its entire life, across
many machines, systematically and repeatably

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
# Remove bundled libraries
rm -rf .%{gem_libdir}/bundler/vendor
mkdir .%{gem_libdir}/bundler/vendor

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod 755
find %{buildroot}%{gem_instdir}/lib/bundler/templates/newgem/bin -type f | xargs chmod 755
chmod 755 %{buildroot}%{gem_instdir}/lib/bundler/templates/Executable*

# Man pages are used by Bundler internally, do not remove them!
mkdir -p %{buildroot}%{_mandir}/man5
cp -a %{buildroot}%{gem_libdir}/bundler/man/gemfile.5 %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man1
for i in bundle bundle-config bundle-exec bundle-install bundle-package bundle-platform bundle-update
do
        cp -a %{buildroot}%{gem_libdir}/bundler/man/$i %{buildroot}%{_mandir}/man1/`echo $i.1`
done

# Test suite has to be disabled for official build, since it downloads various
# gems, which are not in Fedora or they have different version etc.
# Nevertheless, the test suite should run for local builds.
# TODO: investigate failures
%if 0%{enable_test} > 0
%check
pushd .%{gem_instdir}

# This test does not work, since ruby is configured with --with-ruby-version=''
# https://github.com/bundler/bundler/issues/2365
sed -i '/"fetches gems again after changing the version of Ruby"/,/end$/{s/^/#/}' spec/install/gems/platform_spec.rb

# Test suite needs to run in initialized git repository.
# https://github.com/carlhuda/bundler/issues/2022
git init

# Test with system net-http-persistent and thor.
for dependency in \
  net-http-persistent \
  thor
do
  for fileordir in \
    %{gem_dir}/gems/$dependency-*/lib/*
  do
    ln -s -f $fileordir lib/bundler/vendor/$(basename "$fileordir")
  done
done

rspec spec

%endif

%post
# Create symlinks to system RubyGems as a replacement for vendored libs
# See rhbz#1163039
%symlink_vendored_libs

%triggerpostun -- rubygem-thor, rubygem-net-http-persistent
# We need to recreate the symlinks after the old package of vendored lib
# has been removed, not before
%symlink_vendored_libs

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/man
%{gem_libdir}
%ghost %attr(644, root, root) %{gem_libdir}/bundler/vendor/net
%ghost %attr(644, root, root) %{gem_libdir}/bundler/vendor/thor
%ghost %attr(644, root, root) %{gem_libdir}/bundler/vendor/thor.rb
%exclude %{gem_libdir}/bundler/ssl_certs/.document
%exclude %{gem_libdir}/bundler/ssl_certs/*.pem
%doc %{gem_instdir}/LICENSE.md
%{gem_instdir}/.travis.yml
%{_bindir}/bundle
%{_bindir}/bundler
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*

%files doc
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/ISSUES.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/UPGRADING.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/DEVELOPMENT.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 05 2015 Vít Ondruch <vondruch@redhat.com> - 1.7.8-2
- Properly uninstall the vendor directory.

* Tue Dec 09 2014 Vít Ondruch <vondruch@redhat.com> - 1.7.8-1
- Update to Bundler 1.7.8.

* Thu Nov 20 2014 Josef Stribny <jstribny@redhat.com> - 1.7.6-2
- Keep ssl_certs/certificate_manager.rb file (used in tests)
- Correctly add load paths for gems during tests

* Wed Nov 12 2014 Josef Stribny <jstribny@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Nov 11 2014 Josef Stribny <jstribny@redhat.com> - 1.7.4-2
- Use symlinks for vendored libraries (rhbz#1163039)

* Mon Oct 27 2014 Vít Ondruch <vondruch@redhat.com> - 1.7.4-1
- Update to Bundler 1.7.4.
- Add thor and net-http-persistent dependencies into .gemspec.

* Mon Sep 22 2014 Josef Stribny <jstribny@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Sam Kottler <skottler@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (BZ #1047222)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.5-1
- Update to Bundler 1.3.5.

* Mon Mar 04 2013 Josef Stribny <jstribny@redhat.com> - 1.3.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Bundler 1.3.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.1-1
- Update to Bundler 1.2.1.
- Fix permissions on some executable files.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.4-1
- Update to Bundler 1.1.4.

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.21-1
- Rebuilt for Ruby 1.9.3.
- Update to Bundler 1.0.21.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.15-1
- Updated to Bundler 1.0.15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.10-1
- Upstream update

* Thu Jan 27 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.9-2
- More concise summary
- Do not remove manpages, they are used internally
- Added buildroot cleanup in clean section

* Mon Jan 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.9-1
- Bumped to Bundler 1.0.9
- Installed manual pages
- Removed obsolete buildroot cleanup

* Mon Nov 1 2010 Jozef Zigmund <jzigmund@redhat.com> - 1.0.3-2
- Add ruby(abi) dependency
- Add using macro %%{geminstdir} in files section
- Add subpackage doc for doc files
- Removed .gitignore file
- Removed rubygem-thor from vendor folder
- Add dependency rubygem(thor)

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 1.0.3-1
- Initial package
