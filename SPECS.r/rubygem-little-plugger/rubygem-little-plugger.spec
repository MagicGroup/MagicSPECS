# Generated from little-plugger-1.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name little-plugger


Summary: LittlePlugger is a module that provides Gem based plugin management
Name: rubygem-%{gem_name}
Version: 1.1.3
Release: 13%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/little-plugger
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-little-plugger-1.1.3-fix-specs-on-ruby-2.patch
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
LittlePlugger is a module that provides Gem based plugin management.
By extending your own class or module with LittlePlugger you can easily
manage the loading and initializing of plugins provided by other gems.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rspec spec/
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%{gem_libdir}
%{gem_cache}
%{gem_spec}
# contains licensing information
%doc %{gem_instdir}/README.rdoc

%files doc
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.1.3-13
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.3-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.3-11
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.3-6
- BuildRequire rspec instead of rspec-core.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.3-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.3-1
- Update to 1.1.3 version (migrates tests to rspec 2, thanks Vit Ondruch for patch for upstream).

* Wed Nov 02 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-3
- Introduced doc subpackage.
- Introduced check section.
- Removed rspec from Requires and moved it to BuildRequires, as it is only needed for running specs.

* Sat Apr 02 2011 Chris Lalancette <clalance@redhat.com> - 1.1.2-2
- Use the gem from rubygems.org instead of from git

* Wed Mar 16 2011 Chris Lalancette <clalance@redhat.com> - 1.1.2-1
- Initial package
