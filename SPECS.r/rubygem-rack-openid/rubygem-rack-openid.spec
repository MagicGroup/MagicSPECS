%global gem_name rack-openid

Name: rubygem-%{gem_name}
Version: 1.4.2
Release: 5%{?dist}
Summary: Provides a more HTTPish API around the ruby-openid library
Group: Development/Languages
License: MIT
URL: https://github.com/grosser/rack-openid
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream does not ship the test suite in the gem.
Source1: rubygem-rack-openid-generate-test-tarball.sh
Source2: rack-openid-%{version}-tests.tar.xz
# Upstream does not yet include the full text of the MIT license in any
# released version of the gem. In the next release, we can drop this external
# file. See https://github.com/grosser/rack-openid/issues/3
# This Source3 file is available at
# https://raw.github.com/grosser/rack-openid/master/LICENSE
Source3: rubygem-rack-openid-LICENSE
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(rack)
Requires: rubygem(ruby-openid)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(ruby-openid)
BuildRequires: rubygem(rots)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Provides a more HTTPish API around the ruby-openid library.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a 2

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Until upstream ships the full text of the MIT license in a released gem, we
# will ship the version from Git master.
install -p -m 0644 %{SOURCE3} %{buildroot}%{gem_instdir}/LICENSE

%check
cp -pr test .%{gem_instdir}
pushd .%{gem_instdir}
  # Remove dependency on bundler
  sed -e "/require 'bundler\/setup'/d" -i test/helper.rb
  # Remove dependency on minitest-rg
  sed -e "/require 'minitest\/rg'/d" -i test/helper.rb
  # Run tests
  ruby -Ilib test/test_integration.rb test/test_rack_openid.rb
  # Cleanup
  rm -rf test
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.4.2-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.2-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 05 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.2-1
- Update to rack-openid 1.4.2 (RHBZ #1055958)
- Adjust tests tarball generation script to be more tidy

* Thu Nov 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.1-2
- Address issues from package review (RHBZ #1032186)
- Correct comment about LICENSE
- Unpack the tests tarball during %%setup
- Use "set -e" in tests tarball generation script
- Clean up zip file in tests tarball generation script

* Wed Nov 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.1-1
- Update to rack-openid 1.4.1
- Ship license file from upstream Git

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-1
- Initial package
