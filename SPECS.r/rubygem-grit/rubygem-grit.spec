# Generated from grit-2.5.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name grit

Summary: Ruby bindings for git
Name: rubygem-%{gem_name}
Version: 2.5.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/mojombo/grit
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
Requires: rubygem(mime-types) => 1.15
Requires: rubygem(mime-types) < 2
Requires: rubygem(diff-lcs) => 1.1
Requires: rubygem(diff-lcs) < 2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rake)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}


%description
Grit is a Ruby library for extracting information from a git repository in an
object oriented manner.


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
pushd ./%{gem_instdir}
sed -i s'|rake/rdoctask|rdoc/task|' Rakefile
rake test
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/API.txt
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/PURE_TODO
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/benchmarks.rb
%doc %{gem_instdir}/benchmarks.txt
%doc %{gem_instdir}/examples
%doc %{gem_instdir}/grit.gemspec


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.5.0-5
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.5.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.5.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 20 2014 Joe VLcek<jvlcek@redhat.com> - 2.5.0-1
- Update to newer version form upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.4.1-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Vít Ondruch <vondruch@redhat.com> - 2.4.1-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Joe VLcek <jvlcek@redhat.com> - 2.4.1-2
- Updates to address Fedora package review feedback

* Wed Oct 26 2011 Joe VLcek <jvlcek@redhat.com> - 2.4.1-1
- Initial package

