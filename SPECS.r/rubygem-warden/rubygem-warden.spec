%global gem_name warden


Summary: Rack middle-ware that provides authentication for rack applications
Name: rubygem-%{gem_name}
Version: 1.2.3
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/hassox/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rspec) < 3
BuildArch: noarch

%description
Warden is a Rack-based middle-ware, designed to provide a mechanism for
authentication in Ruby web applications. It is a common mechanism that fits
into the Rack Machinery to offer powerful options for authentication.


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


%check
pushd .%{gem_instdir}
rspec2 spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/Gemfile*
%exclude %{gem_instdir}/warden.gemspec
%license %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/spec
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.textile
%doc %{gem_instdir}/History.rdoc
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.3-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vít Ondruch <vondruch@redhat.com> - 1.2.3-1
- Update to warden 1.2.3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to warden 1.2.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.5-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Update to the warden 1.0.5

* Tue Jul 26 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.4-1
- Update to the warden 1.0.4
- Use RSpec 2.x for tests

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Removed RSpec runtime reference

* Mon Dec 20 2010 Vít Ondruch <vondruch@redhat.com> - 1.0.3-2
- Removed obsolete BuildRoot
- Removed explicit library requires
- Removed obsolete build root cleaning
- Removed explicit path to RSpec call

* Wed Dec 15 2010 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
