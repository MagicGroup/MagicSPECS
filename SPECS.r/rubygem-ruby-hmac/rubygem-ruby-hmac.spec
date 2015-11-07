# Generated from ruby-hmac-0.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ruby-hmac

Summary: This module provides common interface to HMAC functionality
Name: rubygem-%{gem_name}
Version: 0.4.0
Release: 14%{?dist}
Group: Development/Languages
License: MIT and Ruby
URL: http://ruby-hmac.rubyforge.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides:  rubygem(ruby-hmac) = %{version}
Provides:  rubygem(hmac) = %{version}-%{release}
Obsoletes: rubygem(hmac) < 0.4.0-6

%description
This module provides common interface to HMAC functionality. HMAC is a kind of
"Message Authentication Code" (MAC) algorithm whose standard is documented in
RFC2104. Namely, a MAC provides a way to check the integrity of information
transmitted over or stored in an unreliable medium, based on a secret key.
Originally written by Daiki Ueno. Converted to a RubyGem by Geoffrey
Grosenbach


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
pushd %{buildroot}/%{gem_instdir}
ruby test/test_hmac.rb
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/Rakefile
%{gem_libdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%doc %{gem_instdir}/test
%doc %{gem_docdir}
%{gem_cache}
%{gem_spec}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.4.0-14
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.0-13
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 07 2012 Mo Morsi <mmorsi@redhat.com> - 0.4.0-7
- small fixes for fedora compliance:
- renamed spec
- added obsoletes

* Thu Aug 02 2012 Mo Morsi <mmorsi@redhat.com> - 0.4.0-6
- renamed rubygem-hmac to rubygem-ruby-hmac

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Chris Lalancette <clalance@redhat.com> - 0.4.0-2
- Updates from review

* Tue Jul 05 2011 Chris Lalancette <clalance@redhat.com> - 0.4.0-1
- Initial package
