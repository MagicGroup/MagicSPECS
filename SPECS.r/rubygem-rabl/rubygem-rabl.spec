# Generated from rabl-0.7.9.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rabl

Summary: General Ruby templating with JSON, BSON, XML and MessagePack support
Name: rubygem-%{gem_name}
Version: 0.11.0
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/nesquena/rabl
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(riot)
BuildRequires: rubygem(tilt)
BuildRequires: rubygem(bson)
BuildRequires: rubygem(activesupport)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
General Ruby templating with JSON, BSON, XML and MessagePack support.

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

%check
pushd .%{gem_instdir}

ruby test/*_test.rb

popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/test.watchr
%{gem_instdir}/Gemfile.ci
%{gem_instdir}/Gemfile
%{gem_instdir}/.travis.yml
%{gem_instdir}/fixtures
%{gem_instdir}/examples
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.11.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Josef Stribny <jstribny@redhat.com> - 0.10.0-1
- Update to rabl 0.10.0

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 0.9.3-1
- Update to rabl 0.9.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Josef Stribny <jstribny@redhat.com> - 0.8.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Rabl 0.8.0

* Wed Dec 12 2012 Josef Stribny <jstribny@redhat.com> - 0.7.9-3
- Tests are now ran by `ruby` command
- Removed the minitest build dependency

* Mon Dec 10 2012 Josef Stribny <jstribny@redhat.com> - 0.7.9-2
- Fixed license
- Moved .gemspec to doc subpackage

* Tue Dec 04 2012 Josef Stribny <jstribny@redhat.com> - 0.7.9-1
- Initial package
