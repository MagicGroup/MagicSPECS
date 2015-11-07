# Generated from ammeter-0.2.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ammeter

Summary: Write specs for your Rails 3+ generators
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/alexrothenberg/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(rspec-rails) >= 2.2
BuildRequires: rubygem(sqlite3)
BuildArch: noarch

%description
Write specs for your Rails 3+ generators.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

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
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/LICENSE.txt
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/ammeter.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/features
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.1.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.2-1
- Update to Ammeter 1.1.2.

* Tue Jun 10 2014 Vít Ondruch <vondruch@redhat.com> - 0.2.9-3
- Fix FTBFS in Rawhide (hrbz#1107063).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 20 2013 Josef Stribny <jstribny@redhat.com> - 0.2.9-1
- Update to 0.2.9
- Rebuilt with Rails 4.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.8-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.8-1
- Updated to Ammeter 0.2.8.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-2
- Moved features to doc subpackage (not needed for runtime).
- Moved gemspec and Gemfile to doc.
- Patched the dependencies to require rspec-core.

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-1
- Initial package
