# Generated from shindo-0.3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name shindo


Summary: Simple depth first Ruby testing
Name: rubygem-%{gem_name}
Version: 0.3.8
Release: 4%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/geemus/shindo
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: ruby 
Requires: rubygem(formatador) >= 0.1.1
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(formatador) >= 0.1.1
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Work with your tests, not against them.


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

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}

RUBYOPT="-I." bin/shindo
popd

%files
%dir %{gem_instdir}
%{_bindir}/shindo
%{_bindir}/shindont
%{gem_instdir}/bin
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.rdoc

%files doc
%doc %{gem_docdir}
%{gem_instdir}/tests
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/shindo.gemspec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.8-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Josef Stribny <jstribny@redhat.com> - 0.3.8-1
- Update to shindo 0.3.8
  - This should address the issue with RubyGems 2.0.4 and its Kernel#require
    limitation when working with threads.

* Tue Aug 20 2013 Josef Stribny <jstribny@redhat.com> - 0.3.6-1
- Update to shindo 0.3.6
- Fix tests

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-2
- Simplified the test running.

* Wed Oct 12 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.4-1
- Initial package
