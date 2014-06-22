%global gem_name json_pure

Summary: JSON Implementation for Ruby
Name: rubygem-%{gem_name}
Version: 1.6.3
Release: 8%{?dist}
Group: Development/Languages
License: GPLv2 or Ruby
URL: http://flori.github.com/json
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(release)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%description
This is a JSON implementation in pure Ruby.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done
find %{buildroot}/%{gem_instdir} -type f -perm /g+wx -exec chmod -v g-w {} \;
rm -rf %{buildroot}/%{gem_instdir}/ext
rm -rf %{buildroot}/%{gem_instdir}/java
rm -f %{buildroot}/%{gem_instdir}/json_pure.gemspec
rm -f %{buildroot}/%{gem_instdir}/json.gemspec
rm -f %{buildroot}/%{gem_instdir}/json-java.gemspec
rm -f %{buildroot}/%{gem_instdir}/Gemfile
rm -f %{buildroot}/%{gem_instdir}/diagrams/.keep
rm -f %{buildroot}/%{gem_instdir}/.travis.yml
rm -f %{buildroot}/%{gem_instdir}/.gitignore
# Fix for Fedora 14:
rm -rf %{buildroot}/%{gem_instdir}/tests/test_json_rails.rb


%check
pushd %{buildroot}%{gem_instdir}
JSON=pure testrb tests
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README-json-jruby.markdown
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/GPL
%doc %{gem_instdir}/COPYING-json-jruby
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/VERSION
%doc %{gem_instdir}/TODO


%files doc
%defattr(-, root, root, -)
%{gem_instdir}/tests
%{gem_instdir}/data
%{gem_instdir}/tools
%{gem_instdir}/benchmarks
%{gem_instdir}/Rakefile
%{gem_docdir}
%{gem_instdir}/install.rb

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.6.3-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 12 2011 Michal Fojtik <mfojtik@redhat.com> - 1.6.3-2
- Rebuild after Koji outage

* Thu Dec 8 2011 Michal Fojtik <mfojtik@redhat.com> - 1.6.3-1
- Version bump

* Fri Jun 3 2011 Michal Fojtik <mfojtik@redhat.com> - 1.5.1-1
- Version bump
- Removed gtk dependency to keep this lightweight

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 04 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.6-3
- Removed tests which was failing under F14

* Sat Oct 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.6-2
- Fixed failing test
- Removed unusefull rm call

* Mon Aug 02 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.6-1
- Version bump
- Removed BuildRoot
- Moved 'rm' from check to install
- Moved files from -doc to main package and install.rb to -doc

* Tue Jul 20 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.3-1
- Initial package
