# Generated from uglifier-1.2.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name uglifier

Summary: Ruby wrapper for UglifyJS JavaScript compressor
Name: rubygem-%{gem_name}
Version: 2.4.0
Release: 6%{?dist}
Group: Development/Languages
# Uglifier itself is MIT
# the bundled JavaScript from UglifyJS is BSD
License: MIT and BSD
URL: http://github.com/lautis/uglifier
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(execjs) >= 0.3.0
Requires: rubygem(multi_json) => 1.3
Requires: rubygem(multi_json) < 2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(execjs) >= 0.3.0
BuildRequires: rubygem(multi_json) => 1.3
BuildRequires: rubygem(multi_json) < 2
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(therubyracer)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Ruby wrapper for UglifyJS JavaScript compressor.


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

# source_map is not part of fedora yet, ged rid of source_map in specs
sed -i "s/require 'source_map'//"  spec/spec_helper.rb
rm spec/source_map_spec.rb

rspec spec
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%exclude %{gem_instdir}/gemfiles
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.4.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.4.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.4.0-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Josef Stribny <jstribny@redhat.com> - 2.4.0-1
- Update to uglifier 2.4.0

* Wed Oct 30 2013 Josef Stribny <jstribny@redhat.com> - 2.3.0-1
- Update to uglifier 2.3.0

* Mon Oct 21 2013 Josef Stribny <jstribny@redhat.com> - 2.2.1-1
- Update to uglifier 2.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 5 2012 Josef Stribny <jstribny@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Mon Jul 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.6-1
- Initial package
