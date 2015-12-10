%global gem_name commander


Summary: The complete solution for Ruby command-line executable
Name: rubygem-%{gem_name}
Version: 4.3.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/tj/commander
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(highline)
BuildArch: noarch

%description
The complete solution for Ruby command-line executable

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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

%check
pushd .%{gem_instdir}
# We don't care about coverage.
sed -i '/simplecov/,/^end$/ s/^/#/' spec/spec_helper.rb

rspec spec
popd


%files
%license %{gem_instdir}/LICENSE
%{_bindir}/commander
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile

%{gem_spec}

%files doc
%doc %{gem_instdir}/DEVELOPMENT
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 4.3.0-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 4.3.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.3.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Vít Ondruch <vondruch@redhat.com> - 4.3.0-1
- Update to Commander 4.3.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 4.1.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 John (J5) Palmieri <johnp@redhat.com> - 4.1.2-1
- patch out simplecov 

* Wed Jun 20 2012 John (J5) Palmieri <johnp@redhat.com> - 4.1.2-1
- update to 4.1.2 since the highline dep has been updated

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 4.0.6-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Vít Ondruch <vondruch@redhat.com> - 4.0.6-1
- Updated to Commander 4.0.6.
- Migrated to RSpec 2.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 21 2010 Michal Fojtik <mfojtik@redhat.com> - 4.0.3-3
- Fixed version dependencies

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 4.0.3-2
- Fixed highline build dependency

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 4.0.3-1
- Initial package
