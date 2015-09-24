# Generated from actionpack-1.13.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name actionpack

%global bootstrap 0

Summary: Web-flow and rendering framework putting the VC in MVC
Name: rubygem-%{gem_name}
Epoch: 1
Version: 4.2.4
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: http://rubygems.org/downloads/actionpack-%{version}.gem

# Also the actionpack gem doesn't ship with the test suite.
# You may check it out like so
# git clone http://github.com/rails/rails.git
# cd rails/actionpack/
# git checkout v4.1.0
# tar czvf actionpack-4.2.4-tests.tgz test/
Source2: actionpack-%{version}-tests.tgz

# Let's keep Requires and BuildRequires sorted alphabeticaly
BuildRequires: rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires: rubygem(activemodel) = %{version}
BuildRequires: rubygem(activerecord) = %{version}
BuildRequires: rubygem(activesupport) = %{version}
BuildRequires: rubygem(actionview) = %{version}
BuildRequires: rubygem(railties) = %{version}
BuildRequires: rubygem(journey) >= 1.0.4
BuildRequires: rubygem(journey) < 1.1
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha) >= 0.9.8
BuildRequires: rubygem(rack) >= 1.6
BuildRequires: rubygem(rack) < 1.7
BuildRequires: rubygem(rack-cache) >= 1.2
BuildRequires: rubygem(rack-cache) < 2
BuildRequires: rubygem(rack-test) >= 0.6.2
BuildRequires: rubygem(rack-test) < 0.7
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(therubyracer)
BuildRequires: rubygem(tzinfo)
BuildRequires: rubygem(uglifier)
%endif
BuildArch: noarch

%description
Eases web-request routing, handling, and response as a half-way front,
half-way page controller. Implemented with specific emphasis on enabling easy
unit/integration testing that doesn't require a browser.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{epoch}:%{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

# move the tests into place
tar xzvf %{SOURCE2} -C .%{gem_instdir}

# Remove backup files
# No! these are needed for rake test
# find ./%{gem_instdir} -type f -name "*~" -delete

# Delete zero-length files
# No! these are also needed for rake test
# find ./%{gem_instdir} -type f -size 0c -exec rm -rvf {} \;

# Fix anything executable that does not have a shebang
for file in `find ./%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find ./%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}


%clean
rm -rf %{buildroot}

%if 0%{bootstrap} < 1
%check
pushd .%{gem_instdir}

# load_path is not available, remove its require.
sed -i '1,2d' test/abstract_unit.rb

# fix rack/test requirement
sed -i "1i\require 'rack/test'" lib/action_controller/metal/strong_parameters.rb

ruby -w -I.:lib:test -rtimeout -e 'Dir.glob("test/{abstract,controller,dispatch,template}/**/*_test.rb").each {|t| require t}'
popd
%endif

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/test/

%changelog
* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.4-2
- Enable tests

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.4-1
- Update to actionpack 4.2.4

* Wed Jul 01 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.3-2
- Enable tests

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.3-1
- Update to actionpack 4.2.3

* Tue Jun 23 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.2-2
- Run tests

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.2-1
- Update to actionpack 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.1-2
- Run tests

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.1-1
- Update to actionpack 4.2.1

* Fri Feb 13 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.0-2
- Run all tests

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 1:4.2.0-1
- Update to actionpack 4.2.0

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to actionpack 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 4.1.4-1
- Update to actionpack 4.1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.1-1
- Update to ActionPack 4.1.1

* Fri Apr 18 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Apr 14 2014 Josef Stribny <jstribny@redhat.com> - 1:4.1.0-1
- Update to ActionPack 4.1.0

* Wed Feb 26 2014 Josef Stribny <jstribny@redhat.com> - 1:4.0.3-1
- Update to ActionPack 4.0.3

* Thu Dec 05 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.2-1
- Update to ActionPack 4.0.2
  - Fixes CVE-2013-6417, CVE-2013-6414, CVE-2013-6415, CVE-2013-6416 and CVE-2013-4491

* Thu Nov 14 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.1-1
- Update to ActionPack 4.0.1

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 1:4.0.0-1
- Update to ActionPack 4.0.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.13-2
- Test suite passes once again.

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.13-1
- Update to the ActionPack 3.2.13.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.12-1
- Update to the ActionPack 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.11-1
- Update to the ActionPack 3.2.11.

* Thu Jan 03 2013 Vít Ondruch <vondruch@redhat.com> - 1:3.2.10-1
- Update to the ActionPack 3.2.10.

* Sat Oct 13 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.8-2
- Relaxed Builder dependency.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.8-1
- Update to the ActionPack 3.2.8.

* Wed Aug 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.2.7-2
- Remove the unneded symlink used for tests in previous versions (RHBZ #840119).

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.7-1
- Update to the ActionPack 3.2.7.

* Tue Jul 24 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.2.6-2
- Fixed missing epoch in -doc subpackage.

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.2.6-1
- Updated to the ActionPack 3.2.6.
- Remove Rake dependency.
- Introduce -doc subpackage.
- Relax sprockets dependency.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.15-1
- Updated to the ActionPack 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 1:3.0.13-1
- Updated to the ActionPack 3.0.13.

* Fri Mar 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-3
- The CVE patches names now contain the CVE id.

* Tue Mar 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-2
- Fix for CVE-2012-1098.
- Fix for CVE-2012-1099.

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.11-1
- Rebuilt for Ruby 1.9.3.
- Updated to ActionPack 3.0.11.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.10-1
- Update to ActionPack 3.0.10

* Mon Jul 04 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.9-1
- Update to ActionPack 3.0.9

* Thu Jun 16 2011 Mo Morsi <mmorsi@redhat.com> - 1:3.0.5-3
- Include fix for CVE-2011-2197

* Fri Jun 03 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-2
- Removed regin and multimap dependencies. They were added into rack-mount
  where they actually belongs.

* Fri Mar 25 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.5-1
- Updated to ActionPack 3.0.5

* Wed Feb 16 2011 Vít Ondruch <vondruch@redhat.com> - 1:3.0.3-4
- Relaxed erubis dependency
- Fixed build compatibility with RubyGems 1.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-2
- changelog fixes

* Mon Jan 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1:3.0.3-1
- Update to rails 3

* Thu Aug 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-2
- Bumped actionpack rack dependency to version 1.1.0

* Mon Aug 09 2010 Mohammed Morsi <mmorsi@redhat.com> - 1:2.3.8-1
- Update to 2.3.8

* Mon May 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-2
- Set TMPDIR environment at %%check to make it sure all files created
  during rpmbuild are cleaned up

* Thu Jan 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.5-1
- Update to 2.3.5

* Fri Jan  8 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.3.4-4
- Workaround patch to fix for rack 1.1.0 dependency (bug 552972)

* Thu Dec 10 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-3
- Patch for CVE-2009-4214 (bz 542786)

* Wed Oct  7 2009 David Lutterkort <lutter@redhat.com> - 1:2.3.4-2
- Bump Epoch to ensure upgrade path from F-11

* Sun Sep 20 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.4-1
- Update to 2.3.4 (bug 520843, CVE-2009-3009)
- Fix tests

* Sun Aug  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.3.3-1
- 2.3.3
- Enable test (some tests fail, please someone investigate!!)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 2.3.2-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 David Lutterkort <lutter@redhat.com> - 2.2.2-1
- New version

* Tue Sep 16 2008 David Lutterkort <dlutter@redhat.com> - 2.1.1-1
- New version (fixes CVE-2008-4094)

* Thu Jul 31 2008 Michael Stahnke <stahnma@fedoraproject.org> - 2.1.0-1
- New Upstream

* Tue Apr  8 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-2
- Fix dependency

* Mon Apr 07 2008 David Lutterkort <dlutter@redhat.com> - 2.0.2-1
- New version

* Mon Dec 10 2007 David Lutterkort <dlutter@redhat.com> - 2.0.1-1
- New version

* Thu Nov 29 2007 David Lutterkort <dlutter@redhat.com> - 1.13.6-1
- New version

* Tue Nov 13 2007 David Lutterkort <dlutter@redhat.com> - 1.13.5-2
- Fix buildroot; mark docs in geminstdir cleanly

* Tue Oct 30 2007 David Lutterkort <dlutter@redhat.com> - 1.13.5-1
- Initial package
