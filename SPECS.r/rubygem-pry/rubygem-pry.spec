%global gem_name pry

Summary: An IRB alternative and runtime developer console
Name: rubygem-%{gem_name}
Version: 0.10.1
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://pryrepl.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream does not ship the test suite in the gem.
Source1: %{name}-generate-test-tarball.sh
Source2: %{gem_name}-%{version}-tests.tar.xz
# rm stray openstruct reference. Upstream at
# https://github.com/pry/pry/commit/70942ad3b2d93e028fc3e8bfe1c6bd11ec79ffad
Patch0: rubygem-pry-0.10.1-rm-openstruct.patch
# Fix "wrong number of arguments (0 for 1)" test suite error.
# https://github.com/pry/pry/commit/0807328bcfd1585b0f668c269dd232505fab8a2c
Patch1: rubygem-pry-0.10.1-Rename-helper-singleton_class-to-eigenclass.patch
# Fix "can't modify frozen object" error.
# https://github.com/pry/pry/commit/74784e8f7889c3b8f0bb337f04b050e79a3df34a
Patch2: rubygem-pry-0.10.1-Handle-error-about-frozen-object-in-Ruby-2.2.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(coderay) => 1.1.0
Requires: rubygem(coderay) < 1.2
Requires: rubygem(slop) => 3.4
Requires: rubygem(slop) < 4
Requires: rubygem(method_source) => 0.8.1
Requires: rubygem(method_source) < 0.9
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(coderay) => 1.1.0
BuildRequires: rubygem(coderay) < 1.2
BuildRequires: rubygem(slop) => 3.4
BuildRequires: rubygem(slop) < 4
BuildRequires: rubygem(method_source) => 0.8.1
BuildRequires: rubygem(method_source) < 0.9
# editor specs fail if no editor is available (soft requirement)
BuildRequires: vi
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
An IRB alternative and runtime developer console.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a 2

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Remove dependency on bundler
sed -e "/require 'bundler\/setup'/d" -i spec/helper.rb
sed -e "/Bundler.require/d" -i spec/helper.rb

# rm stray openstruct reference
%patch0 -p1

%patch1 -p1
%patch2 -p1

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
cp -pr spec .%{gem_instdir}
pushd .%{gem_instdir}
  rspec -I"lib:spec" spec/*_spec.rb
  rm -rf spec/
popd

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{_bindir}/pry
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.10.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.10.1-1
- Update to latest upstream release (RHBZ #1108177)
- Remove gem2rpm auto-generated comment
- Update URL to latest upstream location
- Add generate-test-tarball.sh script since upstream no longer ships the tests
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use gem unpack / setup / build per Ruby packaging guidelines
- Use %%license tag

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Vít Ondruch <vondruch@redhat.com> - 0.9.12.6-1
- Update to Pry 0.9.12.6.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.12-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to Pry 0.9.12.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.10-1
- Initial package
