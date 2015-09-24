# Generated from RedCloth-4.1.9.gem by gem2rpm -*- rpm-spec -*-
%global gem_name RedCloth
%global gemlibname redcloth_scan.so

Summary:       Textile parser for Ruby
Name:          rubygem-%{gem_name}
Version:       4.2.9
Release:       12%{?dist}
Group:         Development/Languages
License:       MIT
URL:           http://redcloth.org
Source0:       http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# Fixes failing tests on ARM which defaults to use unsigned char
# http://jgarber.lighthouseapp.com/projects/13054-redcloth/tickets/236-test-failure-on-armelpowerpc
Patch0:        rubygem-redcloth-4.2.9-unsigned-char-fix.patch
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec-core) < 3
BuildRequires: rubygem(rspec-mocks) < 3
BuildRequires: rubygem(rspec-expectations) < 3
BuildRequires: ruby-devel

%description
Textile parser for Ruby.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%patch0 -p1

%build
gem build %{gem_name}.gemspec

%gem_install

# To create debuginfo file corretly (workaround for
# "#line" directive)
pushd .%{gem_instdir}/ext/redcloth_scan
mkdir ext
ln -sf .. ext/redcloth_scan
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

# Move C extension to the ext dir
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

%check 
pushd .%{gem_instdir}
rspec2 -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%{_bindir}/redcloth
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/.rspec
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_instdir}/Gemfile
%{gem_instdir}/redcloth.gemspec
%{gem_instdir}/tasks
%{gem_libdir}
%{gem_extdir_mri}
%doc %{gem_docdir}
%doc %{gem_instdir}/doc
%doc %{gem_instdir}/spec
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/COPYING
%{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.2.9-12
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 4.2.9-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2
- Use RSpec 2.x for test suite.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Vít Ondruch <vondruch@redhat.com> - 4.2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Josef Stribny <jstribny@redhat.com> - 4.2.9-5
- Patch for ARM which doesn't use signed chars as a default

* Thu Mar 07 2013 Josef Stribny <jstribny@redhat.com> - 4.2.9-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 4.2.9-1
- Rebuilt for Ruby 1.9.3.
- Update to RedCloth 4.2.9.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 03 2010 Michael Stahnke <stahnma@fedoraproject.org> - 4.2.3-1
- Version update 

* Mon Feb 15 2010 Darryl L. Pierce <dpierce@redhat.com> - 4.2.2-1
- Commented out the piece of set the executable status on files.
- Release 4.2.2 of RedCloth.

* Thu Jul 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-7
- Resolves: rhbz#505589 - rubygem-RedCloth-debuginfo created from stripped binaries

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-5
- Resolves: rhbz#505589 - rubygem-RedCloth-debuginfo created from stripped binaries

* Fri May  1 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-4
- First official build for Fedora.

* Thu Apr 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-3
- Changed mv to cp for binaries.
- Removed redundant %%doc entries.

* Thu Apr 30 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-2
- Added BuildRequires: ruby-devel to fix koji issues.

* Thu Apr 23 2009 Darryl L. Pierce <dpierce@redhat.com> - 4.1.9-1
- Initial package
