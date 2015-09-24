%global gem_name climate_control

Name: rubygem-%{gem_name}
Version: 0.0.3
Release: 5%{?dist}
Summary: Modify your ENV easily
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/climate_control
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Make simplecov optional
# https://github.com/thoughtbot/climate_control/pull/7
Patch0: rubygem-climate_control-0.0.3-simplecov.patch
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(activesupport) >= 3.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
# SimpleCov is broken in Rawhide. https://bugzilla.redhat.com/1083715
#BuildRequires: rubygem(simplecov)
BuildRequires: rubygem(activesupport) >= 3.0
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
ClimateControl can be used to temporarily assign environment variables within a
code block.


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

# Remove developer-only files.
for f in .gitignore .travisci.yml Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Make simplecov optional
# https://github.com/thoughtbot/climate_control/pull/7
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unecessary gemspec
pushd .%{gem_instdir}
  rm %{gem_name}.gemspec
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/NEWS
%exclude %{gem_instdir}/spec

%changelog
* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.3-5
- Do not BR: simplecov (RHBZ #1083715)
- Patch tests to make SimpleCov optional

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.3-3
- Move README to main package
- Remove Gemfile, Rakefile and dot files during %%prep
- Exclude rspec tests from binary packages

* Wed Dec 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.0.3-2
- Wrap %%description at 80 characters (RHBZ #1017994)

* Sat Jul 27 2013 ktdreyer@ktdreyer.com - 0.0.3-1
- Initial package, with gem2rpm 0.9.2
