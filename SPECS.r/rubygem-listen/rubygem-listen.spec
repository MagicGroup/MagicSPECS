# Generated from listen-0.4.7.gem by gem2rpm -*- rpm-spec -*-
%global gem_name listen

Name: rubygem-%{gem_name}
Version: 3.0.3
Release: 4%{?dist}
Summary: Listen to file modifications
Group: Development/Languages
License: MIT
URL: https://github.com/guard/listen
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/guard/listen.git && cd listen && git checkout v3.0.3
# tar czvf rubygem-listen-3.0.3-tests.tgz spec
Source1: rubygem-listen-%{version}-tests.tgz
# Remove the hardcoded dependencies. We don't have them in Fedora (except rb-inotify),
# they are platform specifis and not needed.
# https://github.com/guard/listen/pull/54
Patch0: listen-%{version}-Remove-hardcoded-platform-specific-dependencies.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rb-inotify)
BuildRequires: rubygem(thor)
BuildRequires: rubygem(rspec) => 3.0.0rc1
BuildRequires: rubygem(rspec) < 3.1
BuildArch: noarch

%description
The Listen gem listens to file modifications and notifies you about the
changes. Works everywhere!


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
# Patch: Avoid Kernel.require
# https://github.com/guard/listen/issues/340
sed -i -e 's/Kernel.require/require/' ./lib/listen/adapter/linux.rb 
popd

pushd .%{gem_dir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
# Move the tests into place
tar xzvf %{SOURCE1} -C .%{gem_instdir}

pushd .%{gem_instdir}
# We removed dependencies from other platforms so let's remove
# tests as well
rm spec/lib/listen/adapter/darwin_spec.rb
rspec -Ilib:spec -rspec_helper spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/listen
%{gem_instdir}/bin
%doc %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CONTRIBUTING.md

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 3.0.3-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.0.3-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.0.3-2
- 为 Magic 3.0 重建

* Tue Aug 18 2015 Josef Stribny <jstribny@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 07 2014 Josef Stribny <jstribny@redhat.com> - 2.7.11-1
- Update to listen 2.7.11

* Mon Sep 01 2014 Josef Stribny <jstribny@redhat.com> - 2.7.9-1
- Update to listen 2.7.9.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.7-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.7-1
- Initial package
