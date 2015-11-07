%global gem_name aws-sdk-v1

%if 0%{?fedora} >= 19
%global gem_extdir %{gem_extdir_mri}
%endif

Summary:        AWS SDK for Ruby
Name:           rubygem-aws-sdk
Version:        1.60.2
Release:        4%{?dist}
Group:          Development/Languages
License:        ASL 2.0
URL:            http://aws.amazon.com/sdkforruby/
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:      ruby(release)
%else
Requires:      ruby(abi) >= %{rubyabi}
BuildRequires: ruby(abi) >= %{rubyabi}
%endif

Requires:       ruby(rubygems)
Requires:       rubygem(json)
Requires:       rubygem(nokogiri)
Requires:       rubygem(uuidtools)

BuildRequires: rubygems-devel

BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
Build Ruby applications with the aws-sdk gem that takes the complexity
out of coding directly against the web service interfaces. The gem handles
common tasks, such as authentication, request retries, XML processing,
error handling, and more.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -a 0 -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install -n %{gem_name}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# If there were programs installed:
mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_instdir}/rails
%{gem_instdir}/ca-bundle.crt
%{gem_instdir}/endpoints.json
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%{_bindir}/aws-rb

%files doc
%defattr(-, root, root, -)
%{gem_docdir}
%doc %{gem_instdir}/.yardopts
%doc %{gem_instdir}/LICENSE.txt

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.60.2-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.60.2-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 06 2015 Brett Lentz <blentz@redhat.com> - 1.60.2-1
- Upstream release 1.60.2

* Wed Oct 01 2014 Brett Lentz <blentz@redhat.com> - 1.54.0-2
- Use aws-sdk-v1 gem

* Mon Sep 29 2014 Brett Lentz <blentz@redhat.com> - 1.54.0-1
- Upstream release 1.54.0

* Mon Aug 04 2014 Brett Lentz <blentz@redhat.com> - 1.50.0-1
- Upstream release 1.50.0

* Thu Jun 26 2014 Brett Lentz <blentz@redhat.com> - 1.44.0-1
- Upstream release 1.44.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Brett Lentz <blentz@redhat.com> - 1.40.3-1
- Upstream release 1.40.3

* Tue May 06 2014 Brett Lentz <blentz@redhat.com> - 1.39.0-1
- Upstream release 1.39.0

* Wed Feb 12 2014 Brett Lentz <blentz@redhat.com> - 1.38.0-1
- Upstream release 1.38.0

* Wed Feb 12 2014 Brett Lentz <blentz@redhat.com> - 1.34.0-1
- Upstream release 1.34.0

* Wed Feb 5 2014 Brett Lentz <blentz@redhat.com> - 1.33.0-1
- Upstream release 1.33.0

* Wed Jan 22 2014 Brett Lentz <blentz@redhat.com> - 1.32.0-1
- Upstream release 1.32.0

* Wed Nov 06 2013 Brett Lentz <blentz@redhat.com> - 1.24.0-1
- Upstream release 1.24.0
- BZ#1027289

* Tue Aug 13 2013 Brett Lentz <blentz@redhat.com> - 1.15.0-1
- Upstream release 1.15.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Brett Lentz <blentz@redhat.com> - 1.12.0-1
- Upstream release 1.12.0

* Mon Jun 24 2013 Brett Lentz <blentz@redhat.com> - 1.11.3-1
- Upstream release 1.11.3

* Mon May 06 2013 Brett Lentz <blentz@redhat.com> - 1.9.5-1
- Upstream release 1.9.5

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 1.8.4-2
- Use %%gem_install macro.

* Wed Mar 13 2013 Brett Lentz <blentz@redhat.com> - 1.8.4-1
- Update to new packaging guidelines.
- Upstream release 1.8.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013 Brett Lentz <blentz@redhat.com> - 1.8.0-1
- Upstream release 1.8.0

* Mon Nov 26 2012 Brett Lentz <blentz@redhat.com> - 1.7.1-1
- Upstream release 1.7.1

* Fri Sep 7 2012 Brett Lentz <blentz@redhat.com> - 1.6.5-1
- Upstream release 1.6.5

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Brett Lentz <blentz@redhat.com> - 1.5.2-1
- Upstream release 1.5.2

* Wed Apr 25 2012 Marek Goldmann <mgoldman@redhat.com> - 1.4.1-1
- Upstream release 1.4.1

* Tue Mar 13 2012 Brett Lentz <blentz@redhat.com> - 1.3.7-1
- Upstream release 1.3.7

* Tue Mar 06 2012 Brett Lentz <blentz@redhat.com> - 1.3.5-1
- Upstream release 1.3.5

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Marek Goldmann <mgoldman@redhat.com> - 1.1.1-1
- Upstream release 1.1.1

* Fri Aug 05 2011 Marek Goldmann <mgoldman@redhat.com> - 1.0.4-1
- Upstream release 1.0.4

* Tue Jul 26 2011 Marek Goldmann <mgoldman@redhat.com> - 1.0.2-1
- Upstream release 1.0.2

* Tue Jul 19 2011 Marek Goldmann <mgoldman@redhat.com> - 1.0.1-1
- Initial package

