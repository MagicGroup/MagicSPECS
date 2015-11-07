%global gem_name typhoeus

Name: rubygem-%{gem_name}
Version: 0.7.2
Release: 3%{?dist}
Summary: Parallel HTTP library on top of libcurl multi
Group: Development/Languages
License: MIT
URL: https://github.com/typhoeus/typhoeus
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(ethon) >= 0.7.0
BuildRequires: rubygem(faraday)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(sinatra)
BuildArch: noarch

%description
Like a modern code version of the mythical beast with 100 serpent heads,
Typhoeus runs HTTP requests in parallel while cleanly encapsulating handling
logic.

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

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# remove all shebang, set permission to 0644 (mtasaka)
for f in $(find %{buildroot}%{gem_instdir} -name \*.rb)
do
       sed -i -e '/^#!/d' $f
       chmod 0644 $f
done


%check
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i -e '/require "bundler"/ s/^/#/' \
  -e '/Bundler\.setup/ s/^/#/' spec/spec_helper.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/UPGRADE.md
%{gem_instdir}/perf
%{gem_instdir}/spec
%{gem_instdir}/typhoeus.gemspec
%doc %{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.7.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.2-2
- 为 Magic 3.0 重建

* Thu Jul 09 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2-1
- Update to Typhoeus 0.7.2.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.8-1
- Update to Typhoeus 0.6.8.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.2-1
- Updated to 0.6.2 to satisfy new Webmock.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.3-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.3-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.3-1
- Updated to typhoeus 0.3.3.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 0.2.0-1
- Version bump

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-3
- Preserved failing test files (thx. to mtasaka)
- Fixed macros usage
- Replaced path with macro
- Removed libcurl from requires

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-2
- Fixed License to MIT
- Fixed libcurl BuildRequire
- Gem now recompiles with correct GCC flags
- Directory issues should be fixed
- Removed -devel subpackage
- Added tests


* Wed Oct 06 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-1
- Initial package
