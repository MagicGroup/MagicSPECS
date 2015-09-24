%global gem_name ferret

Summary: Full-featured text search engine library
Name: rubygem-%{gem_name}
Version: 0.11.8.4
Release: 11%{?dist}
Group: Development/Languages
# License from
# - MIT-LICENSE: MIT
# - ext/posh.c: 3-clause BSD
# - ext/q_parser.c: GPLv2+
License: MIT and BSD
URL: http://github.com/jkraemer/ferret
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix compatibility with minitest. Already accepted by upstream.
# https://github.com/jkraemer/ferret/pull/3
Patch0: rubygem-ferret-0.11.8.4-Fix-compatibily-with-minitest.patch
# Rake should not be runtime requirement.
# https://github.com/jkraemer/ferret/pull/5
Patch1: rubygem-ferret-0.11.8.4-make-rake-just-development-dependency.patch
Patch2: rubygem-ferret-0.11.8.4-Block-variables-has-local-scopes.patch
# See https://bugs.ruby-lang.org/issues/9889
Patch3: rubygem-ferret-0.11.8.4-ruby22-hashsize.patch
# fix build on aarch64
Patch4: rubygen-ferret-posh.h-aarch64.patch
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(minitest) < 5
BuildRequires: rubygem(test-unit)

%description
Ferret is a high-performance, full-featured text search
engine library written entirely in pure Ruby (with an
optional C extension). It is inspired by the Java Lucene
Project.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

%patch0 -p2
%patch2 -p2
%patch3 -p1
%patch4 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}-%{version}.gemspec
%patch1 -p1

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

# Remove executable flags (fix rpmlint warnings).
find %{buildroot}%{gem_instdir}/test -type f | xargs chmod a-x
chmod a-x %{buildroot}%{gem_instdir}/Rakefile


%check
pushd .%{gem_instdir}
# Disable buffer overflow failing test
# https://github.com/jkraemer/ferret/issues/2
sed -i '67d' test/unit/index/tc_index_writer.rb

ruby test/test_all.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{_bindir}/ferret-browser
%{gem_instdir}/bin
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README
%doc %{gem_instdir}/RELEASE_CHANGES
%doc %{gem_instdir}/RELEASE_NOTES
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/TUTORIAL
%{gem_instdir}/Rakefile
%{gem_instdir}/setup.rb
%{gem_instdir}/test/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.11.8.4-10
- add aarch64 definitions to posh.h to fix FTBFS

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.11.8.4-9
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Fix RHASH_SIZE related fix failure

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Vít Ondruch <vondruch@redhat.com> - 0.11.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.11.8.4-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Vít Ondruch <vondruch@redhat.com> - 0.11.8.4-1
- Update to ferret 0.11.8.4.
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 05 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.11.6-9
- Update from comments in #468597
- Update to reflect new package guidelines

* Wed Oct 29 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.11.6-7
- Adjust license tag for package (#468597)
- Adjust Source0 URL (#468597)
- Make sure that the gem installation dir itself is owned by this package (#468597)

* Sun Oct 25 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.11.6-6
- Majorly revise packaging strategy (#468597)
- Found all licenses in each of the files
- Include license file

* Sun Oct 25 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.11.6-2
- Better use of macros
- rpmlint now silent

* Sun Oct 25 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.11.6-1
- Initial package
