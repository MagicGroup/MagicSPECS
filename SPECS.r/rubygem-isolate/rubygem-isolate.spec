%global	gem_name	isolate
Summary:	Very simple RubyGems sandbox

Name:		rubygem-%{gem_name}
Version:	3.3.1
Release:	3%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://github.com/jbarnette/isolate
Source0:	https://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch:	noarch

%if 0%{?fedora} <= 21
Requires:	ruby(release)
%endif
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(hoe)
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(rake)
#BuildRequires:	iputils

Requires:	rubygems

Provides:	rubygem(%{gem_name}) = %{version}

%description
Isolate is a very simple RubyGems sandbox. It provides a way to
express and automatically install your project's Gem dependencies.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# cleanup
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}

%check
ping -c 3 www.google.co.jp || exit 0

pushd .%{gem_instdir}
ruby -rubygems %{_bindir}/rake test --trace

%files
%defattr(-,root,root,-)
%dir	%{gem_instdir}
%doc	%{gem_instdir}/CHANGELOG.rdoc
%doc	%{gem_instdir}/README.rdoc
%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%{gem_instdir}/Manifest.txt
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/test/
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.3.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb  5 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.1-1
- 3.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.4-1
- 3.2.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-4
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.2.2-1
- 3.2.2

* Tue Apr 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.1-4
- Fix conditionals for F17 to work for RHEL 7 as well.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.2.1-3
- Rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1

* Fri Sep  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.2.0-1
- 3.2.0

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2

* Thu Jul 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.1.1-1
- 3.1.1

* Sun Jul 17 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3.1.0-1
- 3.1.0

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.0.0-2
- F-15 mass rebuild

* Sat Nov 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.0.0-1
- Initial package
