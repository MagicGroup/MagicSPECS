# Generated from gem-nice-install-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name gem-nice-install

Summary: A RubyGems plugin that improves gem installation user experience
Name: rubygem-%{gem_name}
Version: 0.3.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/voxik/gem-nice-install
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
Requires: ruby(release)
Requires: ruby(rubygems)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A RubyGems plugin that improves gem installation user experience. If binary
extension build fails, it tries to install its development dependencies.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}


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
%{gem_instdir}/data
%doc %{gem_instdir}/MIT
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.0-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Josef Stribny <jstribny@redhat.com> - 0.3.0-1
- Update to 0.3.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Josef Stribny <jstribny@redhat.com> - 0.2.0-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Josef Strzibny <jstribny@redhat.com> - 0.2.0-1
- Updated to version 0.2.0

* Thu Oct 25 2012 Josef Strzibny <jstribny@redhat.com> - 0.1.0-2
- Removed LANG=en_US.utf8 option from the installation step;
  was needed for RubyGems 1.8, >= 1.8.24 don't need it

* Thu Oct 18 2012 Josef Strzibny <jstribny@redhat.com> - 0.1.0-1
- Initial package
