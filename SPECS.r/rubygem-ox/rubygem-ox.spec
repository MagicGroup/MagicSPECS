%global gem_name ox

# tests require minitest >= 5
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
%global with_tests 0
%else
%global with_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        2.1.8
Release:        4%{?dist}
Summary:        Fast XML parser and object serializer

Group:          Development/Languages
# lib/ox.rb licensed also under MIT:
# https://github.com/ohler55/ox/pull/108
License:        MIT
URL:            http://www.ohler.com/ox
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/ohler55/ox && cd ox
# git checkout v2.1.8
# tar -czf rubygem-ox-2.1.8-test.tgz test/
Source1:        %{name}-%{version}-test.tgz

BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel
%if 0%{?with_tests}
BuildRequires:  rubygem(minitest) >= 5
%endif
%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(release)
Requires:       ruby(rubygems)
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
A fast XML parser and object serializer that uses only standard C lib.
Optimized XML (Ox), as the name implies was written to provide speed optimized
XML handling. It was designed to be an alternative to Nokogiri and other Ruby
XML parsers for generic XML parsing and as an alternative to Marshal for
Object serialization.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version} -a1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if 0%{?fedora} && 0%{?fedora} <= 20 || 0%{?rhel} && 0%{?rhel} <= 7
mkdir -p %{buildroot}%{gem_extdir_mri}/lib/ox
mv %{buildroot}%{gem_instdir}/lib/ox.so %{buildroot}%{gem_extdir_mri}/lib/ox/
%else
mkdir -p %{buildroot}%{gem_extdir_mri}/ox
cp -a .%{gem_extdir_mri}/gem.build_complete %{buildroot}%{gem_extdir_mri}/
cp -a .%{gem_extdir_mri}/*.so %{buildroot}%{gem_extdir_mri}/ox/
%endif
rm -rf %{buildroot}%{gem_instdir}/ext/


%if 0%{?with_tests}
%check
cp -pr test/ ./%{gem_instdir}
pushd ./%{gem_instdir}
# always use minitest (tests.rb requires it anyway)
sed -i -e 's/\(use_minitest\) = .*/\1 = 1/' test/sax/sax_test.rb
ruby -Ilib:test test/tests.rb
ruby -Ilib:test test/sax/sax_test.rb
rm -rf test
popd
%endif


%files
%dir %{gem_instdir}/
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}/
%{gem_extdir_mri}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.8-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.8-2
- Use the %%license tag
- Move README.md to the main package

* Tue Feb 17 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.8-1
- Update to 2.1.8

* Tue Feb 10 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.7-1
- Update to 2.1.7

* Wed Dec 31 2014 František Dvořák <valtri@civ.zcu.cz> - 2.1.6-1
- Update to 2.1.6
- Changed license from BSD to MIT (https://github.com/ohler55/ox/issues/104)
- Tests added

* Fri Oct 03 2014 František Dvořák <valtri@civ.zcu.cz> - 2.1.3-1
- Initial package
