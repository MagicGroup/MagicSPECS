# Generated from memcache-client-1.8.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name memcache-client


Summary: A Ruby library for accessing memcached
Name: rubygem-%{gem_name}
Version: 1.8.5
Release: 10%{?dist}
Group: Development/Languages
License: BSD
URL: http://github.com/mperham/memcache-client
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(flexmock)

BuildArch: noarch

%description
A Ruby library for accessing memcached.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# test_benchmark require running memcache server
# and test_event_machine requires ruby 1.9 so
# not running those now
ruby -I "lib/" test/test_mem_cache.rb
popd

%files
%{_bindir}/memcached_top
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/FAQ.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/performance.txt
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/test
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Mon Aug 04 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.5-10
- Fix FTBFS in Rawhide (rhbz#1107162).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 1.8.5-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Change BuildRequires: rubygem-flexmock to rubygem(flexmock) (bz#674413 solved)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Mo Morsi <mmorsi@redhat.com> - 1.8.5-4
- updated to ruby 1.9

* Wed Feb 02 2011 Mo Morsi <mmorsi@redhat.com> - 1.8.5-3
- Removed %clean section

* Tue Feb 01 2011 Mo Morsi <mmorsi@redhat.com> - 1.8.5-2
- Updates to conform to fedora guidelines

* Mon Jan 10 2011 Mo Morsi <mmorsi@redhat.com> - 1.8.5-1
- Initial package
