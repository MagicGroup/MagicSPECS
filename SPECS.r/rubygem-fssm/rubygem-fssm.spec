%global gem_name fssm

Summary: File system state monitor
Name: rubygem-%{gem_name}
Version: 0.2.10
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/ttilley/fssm
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec) < 3
BuildArch: noarch

%description
The File System State Monitor keeps track of the state of any number of paths
and will fire events when said state changes (create/update/delete). FSSM
supports using FSEvents on MacOS, Inotify on GNU/Linux, and polling anywhere
else.


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


%check
pushd .%{gem_instdir}

# Remove Bundler dependency
sed -i '/bundler\/setup/d' spec/spec_helper.rb

rspec2 spec/
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/ext
%{gem_libdir}/
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.markdown
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/example.rb
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/profile/
%{gem_instdir}/spec/
%doc %{gem_docdir}

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.2.10-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.2.10-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Vít Ondruch <vondruch@redhat.com> - 0.2.10-1
- Update to FSSM 0.2.10.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.7-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.7-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.7-1
- Update to fssm 0.2.7.

* Tue Apr 05 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.6.1-1
- Updated to fssm 0.2.6.1
- Removed obsolete BuildRoot.
- Removed unnecessary cleanup.
- Testsuite executed using RSpec 2.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Vít Ondruch <vondruch@redhat.com> - 0.2.2-3
- Removed explicit RubyGems version

* Fri Dec 17 2010 Vít Ondruch <vondruch@redhat.com> - 0.2.2-2
- Documentation moved into subpackage

* Fri Dec 17 2010 Vít Ondruch <vondruch@redhat.com> - 0.2.2-1
- Initial package
