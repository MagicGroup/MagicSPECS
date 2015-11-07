%global gem_name selenium-webdriver


Summary: The next generation developer focused tool for automated testing of webapps
Name: rubygem-%{gem_name}
Version: 2.45.0
Release: 5%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://selenium.googlecode.com
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
Requires: rubygem(childprocess) >= 0.5
Requires: rubygem(multi_json)   >= 1.0
Requires: rubygem(rubyzip)      >= 1.0
Requires: rubygem(websocket)    >= 1.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
WebDriver is a tool for writing automated tests of websites. It aims to mimic
the behavior of a real user, and as such interacts with the HTML of the
application.


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
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
rm -f %{buildroot}%{gem_libdir}/selenium/webdriver/firefox/native/linux/x86/x_ignore_nofocus.so
rm -f %{buildroot}%{gem_libdir}/selenium/webdriver/firefox/native/linux/amd64/x_ignore_nofocus.so
rm -f %{buildroot}%{gem_libdir}/selenium/webdriver/ie/native/x64/IEDriver.dll
rm -f %{buildroot}%{gem_libdir}/selenium/webdriver/ie/native/win32/IEDriver.dll
rm -f %{buildroot}%{gem_instdir}/Gemfile*
rm -f %{buildroot}%{gem_instdir}/%{gem_name}.gemspec


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.45.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.45.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Mo Morsi <mmorsi@redhat.com> - 2.45.0-2
- Fix dependencies

* Thu Apr 09 2015 Mo Morsi <mmorsi@redhat.com> - 2.45.0-1
- Update to 2.45.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.3.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 2.3.2-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 03 2011 Chris Lalancette <clalance@redhat.com> - 2.3.2-1
- Initial package
