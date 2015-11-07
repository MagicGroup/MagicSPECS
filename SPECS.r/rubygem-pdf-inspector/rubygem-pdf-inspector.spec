# Generated from pdf-inspector-1.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name pdf-inspector

Summary: A tool for analyzing PDF output
Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 3%{?dist}
Group: Development/Languages
License: GPLv2 or GPLv3 or Ruby
URL: https://github.com/sandal/pdf-inspector
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch

%description
This library provides a number of PDF::Reader[0] based tools for use in
testing PDF output.  Presently, the primary purpose of this tool is to
support the tests found in Prawn[1], a pure Ruby PDF generation library.
However, it may be useful to others, so we have made it available as
a gem in its own right.
[0] https://github.com/yob/pdf-reader
[1] https://github.com/sandal/prawn

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

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/GPLv2
%doc %{gem_instdir}/GPLv3

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README.md

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 为 Magic 3.0 重建

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 23 2014 Josef Stribny <jstribny@redhat.com> - 1.1.0-1
- Update to 1.1.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 1.0.2-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Josef Stribny <jstribny@redhat.com> - 1.0.2-2
- Removal of the Ruby runtime dependency
- Fixed word wrapping in description

* Thu Nov 29 2012 Josef Stribny <jstribny@redhat.com> - 1.0.2-1
- Initial package
