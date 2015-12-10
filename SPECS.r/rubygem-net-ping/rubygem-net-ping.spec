%global gem_name net-ping
%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

Summary: A ping interface for Ruby
Name: rubygem-%{gem_name}
Version: 1.7.7
Release: 4%{?dist}
Group: Development/Languages
License: Artistic 2.0
URL: http://www.rubyforge.org/projects/shards
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
%if 0%{?rhel} == 6
Requires: ruby(abi) = 1.8
%else
%if 0%{?fedora} >= 19
Requires: ruby(release)
%else
Requires: ruby(abi) = 1.9.1
%endif
%endif
Requires: ruby(rubygems)
Requires: rubygem(net-ldap)
Requires: rubygem(ffi)

BuildRequires: iputils
BuildRequires: rubygems
BuildRequires: ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(fakeweb)
BuildRequires: rubygem(net-ldap)
BuildRequires: rubygem(ffi)

%description
The net-ping library provides a ping interface for Ruby. It includes
separate TCP, HTTP, ICMP, UDP, WMI (for Windows) and external ping
classes.

%package doc
Summary: A ping interface for Ruby - documentation
Group: Development/Languages

%description doc
This package contains the documentation files for the %{gem_name} Ruby
library.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%doc %{gem_instdir}/README.md
%{gem_cache}
%{gem_spec}

%files doc
%dir %{gem_instdir}
%doc %{gem_instdir}/doc/ping.txt
%doc %{gem_instdir}/examples/
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%{gem_instdir}/test
%{gem_instdir}/net-ping.gemspec
%{gem_instdir}/MANIFEST
%{gem_instdir}/CHANGES

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.7.7-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.7.7-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7.7-2
- 为 Magic 3.0 重建

* Wed Jun 24 2015 Lukas Zapletal <lzap+rpm@redhat.com> 1.7.7-1
- Update to 1.7.7
- Dropped unused rubygem-ldap dependency

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 06 2014 Lukas Zapletal <lzap+rpm@redhat.com> 1.7.3-1
- version bump
- fixed bogus date in the changelog

* Thu Aug 15 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.6.2-1
- version bump

* Thu Aug 01 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.6.1-1
- version bump

* Thu Mar 21 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.0-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Mar 20 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.6.0-1
- version bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Miroslav Suchý <msuchy@redhat.com> 1.5.3-6
- require net-ldap and ffi (msuchy@redhat.com)

* Fri Aug 10 2012 Miroslav Suchý <msuchy@redhat.com> 1.5.3-5
- fix filelist section (msuchy@redhat.com)

* Fri Aug 10 2012 Miroslav Suchý <msuchy@redhat.com> 1.5.3-4
- add rubygems to buildrequires (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 1.5.3-3
- new package built with tito

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.5.3-1
- New version

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.5.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.5.1-1
- rebuild

* Fri Mar 18 2011 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.4.1-1
- unit tests now use mock servers
- fixing issues from the review #672845

* Tue Jan 25 2011 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.4.0-1
- Initial package
