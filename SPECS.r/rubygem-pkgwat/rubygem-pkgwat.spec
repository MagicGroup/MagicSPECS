%global gem_name pkgwat

Name: rubygem-%{gem_name}
Version: 0.1.4
Release: 7%{?dist}
Summary: Check your gems against Fedora/EPEL
Group: Development/Languages
License: MIT
URL: https://github.com/daviddavis/pkgwat
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(nokogiri) => 1.4
Requires: rubygem(nokogiri) < 2
Requires: rubygem(rake)
Requires: rubygem(json) => 1.4
Requires: rubygem(json) < 2
Requires: rubygem(sanitize)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(vcr)
BuildRequires: rubygem(webmock)
BuildRequires: rubygem(sanitize)
# debugger required for tests. Not yet packaged.
#BuildRequires: rubygem(debugger)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
pkgwat checks your Gemfile.lock to make sure all your gems
are packaged in Fedora/EPEL.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# remove some unecessary files
rm Gemfile
rm Rakefile
sed -i 's|"Gemfile",||' %{gem_name}.gemspec
sed -i 's|"Rakefile",||' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -I"lib:test" test/pkgwat_test.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-6
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Update for Minitest 5
- Fix spelling in comment

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-4
- Remove thor requirement

* Wed Oct 30 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-3
- Clean up Summary and Description

* Tue Oct 29 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-2
- Remove Gemfile and Rakefile in %%prep
- Delete extraneous boilerplate comment about C extensions
- Move README.md to main package
- Exclude test suite and Rakefile from binary packages

* Wed Oct 02 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.4-1
- Update to 0.1.4
- Drop upstreamed debugger gem patch
- Drop BR: ruby, since BR: ruby(release) provides the same thing
- Fix gem_dir macro in comment to satisfy rpmlint

* Thu Sep 12 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.3-2
- rubygem-sanitize is now in Fedora. Enable it in the BR.
- Patch to remove hard dep on debugger gem
- Enable test suite

* Mon Jul 29 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.3-1
- Update to 0.1.3
- Update nokogiri and json version requirements to match gemspec

* Sat Jul 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.1.2-1
- Update to 0.1.2
- Drop nokogiri and json strict version requirements
- Set License field
- Package tests and prepare for enabling

* Thu Jun 27 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 0.1.0-1
- Initial package
