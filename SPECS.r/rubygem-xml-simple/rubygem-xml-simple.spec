# Generated from xml-simple-1.0.12.gem by gem2rpm -*- rpm-spec -*-
%global gem_name xml-simple

Summary: A simple API for XML processing
Name: rubygem-%{gem_name}
Version: 1.1.2
Release: 7%{?dist}
Group: Development/Languages
License: BSD or Ruby
URL: http://xml-simple.rubyforge.org
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A simple API for XML processing.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

chmod -x %{buildroot}/%{gem_libdir}/xmlsimple.rb

%files
%{gem_instdir}
%doc %{gem_docdir}
%{gem_cache}
%{gem_spec}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.2-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.2-6
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.2-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 21 2013 Michal Fojtik <mfojtik@redhat.com> - 1.1.2-1
- Version bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.12-7
- Updated license after clarification with author.

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.12-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 30 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0.12-3
- Removed buildroot
- Fixed emails and changelog formatting

* Tue Apr 20 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0.12-2
- Fixed permissions
- Fixed timestamps

* Tue Apr 20 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0.12-1
- Initial package
