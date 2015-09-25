%global gem_name aws

Summary: Ruby gem for all Amazon Web Services
Name: rubygem-%{gem_name}
Version: 2.9.1
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/appoxy/aws
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
Requires: rubygem(xml-simple)
Requires: rubygem(http_connection)
Requires: rubygem(uuidtools)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
The RightScale AWS gems have been designed to provide a robust, fast, and
secure interface to Amazon EC2, EBS, S3, SQS, SDB, and CloudFront. These gems
have been used in production by RightScale since late 2006 and are being
maintained to track enhancements made by Amazon

%prep

%build

%install
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%check

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.markdown
%doc %{gem_docdir}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/aws.gemspec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.9.1-3
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Michal Fojtik <mfojtik@redhat.com> - 2.9.1-1
- Version bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 2.7.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Sun Mar 17 2013 Marek Goldmann <mgoldman@redhat.com> - 2.7.0-2
- New guidelines

* Wed Feb 06 2013 Michal Fojtik <mfojtik@redhat.com> - 2.7.0-1
- Version bump

* Mon Sep 10 2012 Michal Fojtik <mfojtik@redhat.com> - 2.5.7-1
- Version bump

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.5.6-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 04 2011 Michal Fojtik <mfojtik@redhat.com> - 2.5.6-1
- Version bump

* Mon Jun 20 2011 Michal Fojtik <mfojtik@redhat.com> - 2.5.5-1
- Replaced right_http_connection with http_connection
- Version bump

* Tue May 10 2011 Michal Fojtik <mfojtik@redhat.com> - 2.5.2-1
- Launch instance bug fixed in this release
- Version bump

* Mon May 09 2011 Michal Fojtik <mfojtik@redhat.com> - 2.5.1-1
- Version bump
- New release no longer has active_support dependency
- Test directory is no longer part of this gem

* Wed Mar 30 2011 Michal Fojtik <mfojtik@redhat.com> - 2.4.5-2
- Added activesupport back

* Tue Mar 29 2011 Michal Fojtik <mfojtik@redhat.com> - 2.4.5-1
- Version bump
- Removed activesupport

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Fojtik <mfojtik@redhat.com> - 2.4.2-1
- Version bump

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 2.3.34-2
- Replaced http_connection to right_http_connection to fix dependency issue

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 2.3.34-1
- Version bump

* Tue Nov 23 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.26-1
- Replaced right_http_connection with http_connection
- Version bump

* Mon Oct 11 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.21-4
* Replaced patch path with macro

* Tue Oct 05 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.21-3
- Included missing patch from 2.3.21-2

* Tue Oct 05 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.21-2
- Added Ruby 1.8 compatibility patch (thx mtasaka)
- Added activesupport dependency
- Fixed typo in right_http_connection dependency in gemspec (upstream contacted)
- Fixed directory ownership

* Sat Sep 25 2010 Michal Fojtik <mfojtik@redhat.com> - 2.3.21-1
- Initial package
