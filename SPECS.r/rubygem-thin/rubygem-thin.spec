%global gem_name thin

Summary: A thin and fast web server
Name: rubygem-%{gem_name}
Version: 1.6.2
Release: 7%{?dist}
Group: Development/Languages
License: (GPLv2 or Ruby) and MIT
URL: http://code.macournoyer.com/thin/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/macournoyer/thin.git && cd thin && git checkout v1.6.2
# tar czvf thin-1.6.2-tests.tgz spec/
Source1: %{gem_name}-%{version}-tests.tgz
# https://github.com/macournoyer/thin/issues/76
Patch3: rubygem-thin-fix-install-spec.patch
Requires: curl
BuildRequires: ruby(release)
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
%if 0%{?fedora} >= 22
BuildRequires: rubygem(rspec2)
%else
BuildRequires: rubygem(rspec)
%endif
BuildRequires: rubygem(eventmachine) >= 0.12.6
BuildRequires: rubygem(daemons) >= 1.0.9
BuildRequires: rubygem(rack) >= 1.0.0

%description
Thin is a Ruby web server that glues together three of the best Ruby
libraries in web history.
The Mongrel parser, the root of Mongrel speed and security,
Event Machine, a network I/O library with extremely high scalability and
Rack, a minimal interface between webservers and Ruby frameworks.

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir}/example -type f ! -perm /a+x -name "*.ru"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%check
pushd .%{gem_instdir}

tar xzvf %{SOURCE1}

# Depends on rubygem-benchmark_unit, not available in Fedora yet.
rm -rf spec/perf
# The 'should force kill process in pid file' spec is not compatible with RSpec2.
# https://github.com/rspec/rspec-core/issues/520
sed -i "/'should force kill process in pid file'/a \    pending" spec/daemonizing_spec.rb

# These 2 tests are passing independently, but fails when running with the
# whole testsuite.
sed -i '/"tracing routines (with NO custom logger)"/a \    before { pending }' spec/logging_spec.rb

# https://github.com/macournoyer/thin/issues/232
sed -i '/"should close body tempfile when closing"/a \    pending' spec/request/processing_spec.rb

cat %{PATCH3} | patch -p1

%if 0%{?fedora} >= 22
rspec2 \
%else
rspec \
%endif
	-I$(dirs +1)%{gem_extdir_mri} spec

popd

%files
%{gem_instdir}/README.md
%{_bindir}/%{gem_name}
%dir %{gem_instdir}
%{gem_instdir}/bin
%dir %{gem_libdir}
%{gem_libdir}/thin.rb
%{gem_libdir}/rack/
%dir %{gem_libdir}/thin/
%{gem_libdir}/thin/*.rb
%{gem_libdir}/thin/backends/
%{gem_libdir}/thin/controllers/
# BSD
%{gem_libdir}/thin/stats.html.erb
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_docdir}
%{gem_instdir}/example/
%{gem_instdir}/CHANGELOG
%{gem_instdir}/Rakefile

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.6.2-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.6.2-6
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.2-4
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Use rspec2 for now

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.6.2-1
- Update to thin 1.6.2.

* Wed Apr 16 2014 Josef Stribny <jstribny@redhat.com> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.5.0-1
- Update to thin 1.5.0.

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.1-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.1-1
- Update to Thin 1.3.1.

* Tue Sep 06 2011 Chris Lalancette <clalance@redhat.com> - 1.2.11-10
- Bump the release so upgrades from F-16 work

* Mon Jul 25 2011 Chris Lalancette <clalance@redhat.com> - 1.2.11-3
- Move stats.html.erb to the main package (it is a runtime requirement)

* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 1.2.11-2
- Fix the load path for thin_parser

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.11-1
- Version bump

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-3
- Removed Rake dependency completely

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-2
- Fixed RSpec tests

* Tue Mar 01 2011 Michal Fojtik <mfojtik@redhat.com> - 1.2.8-1
- Updated to upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.7-1
- Updated to upstream version

* Thu Feb 04 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-5
- Excluded ppc64 in tests (566401)
- Fixed Licensing

* Wed Feb 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-4
- Added rspec tests
- Fixed unwanted recompilation
- Fixed licensing

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-3
- Fixed description

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-2
- Build fixed
- Licence corrected
- Added missing requires
- Marked relevant files as documentation

* Tue Feb 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.5-1
- Initial package


