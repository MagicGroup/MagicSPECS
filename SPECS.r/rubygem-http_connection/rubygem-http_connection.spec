%global gem_name http_connection

Summary: RightScale's robust HTTP/S connection module
Name: rubygem-%{gem_name}
Version: 1.4.1
Release: 13%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/appoxy/http_connection
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version} rubygem(right_http_connection) 
Obsoletes: rubygem(right_http_connection)

%description
Rightscale::HttpConnection is a robust HTTP(S) library. It implements a retry
algorithm for low-level network errors.

%prep

%build
%gem_install -n %{SOURCE0}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README.txt
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.4.1-13
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.4.1-12
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.1-11
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Josef Stribny <jstribny@redhat.com> - 1.4.1-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Michal Fojtik <mfojtik@redhat.com> - 1.4.1-2
- Added rubygem-right_http_connection to Provide and Obsolete

* Thu Jun 16 2011 Michal Fojtik <mfojtik@redhat.com> - 1.4.1-1
- Renaming package rubygem-right_http_connection

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.4-2
- Fixed duplicated files
- Fixed ruby dependency

* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.2.4-1
- Initial package
