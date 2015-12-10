# Generated from rails_warden-0.5.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails_warden


Summary: A gem that provides authentication via the Warden framework
Name: rubygem-%{gem_name}
Version: 0.5.8
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/hassox/rails_warden
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/hassox/rails_warden.git && cd rails_warden && git checkout v0.5.8
# tar czvf rails_warden-0.5.8-tests.tgz spec/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rails)
BuildRequires: rubygem(warden) >= 1.0.0
BuildArch: noarch

%description
A gem that provides authentication via the Warden framework


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
tar xzvf %{SOURCE1}
rspec spec
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.textile
%doc %{gem_instdir}/TODO


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.5.8-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.5.8-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.8-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Vít Ondruch <vondruch@redhat.com> - 0.5.8-1
- Update to rails_warden 0.5.8.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.7-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.7-1
- Update to rails_warden 0.5.7.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.6-1
- Updated to rails_warden 0.5.6.

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.5-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Vít Ondruch <vondruch@redhat.com> - 0.5.5-1
- Initial package
