# Generated from right_aws-1.10.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name right_aws

Summary: Interface classes for the Amazon EC2/EBS, SQS, S3, SDB, and ACF Web Services
Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubyforge.org/projects/rightscale
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
Requires: rubygem(right_http_connection) >= 1.2.4
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
The RightScale AWS gems have been designed to provide a robust, 
fast, and secure interface to Amazon EC2, EBS, S3, SQS, SDB, and
a CloudFront.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_cache}
%{gem_spec}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.0-10
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.0-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Michal Fojtik <mfojtik@redhat.com> - 2.0.0-1
- Version bump
* Thu Mar 18 2010 Michal Fojtik <mfojtik@redhat.com> - 1.10.0-4
- Fixed right_http_connection dependenct
* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.10.0-3
- Fixed dependency name
- Fixed file list
* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.10.0-2
- Fixed duplicate files
* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.10.0-1
- Initial package
