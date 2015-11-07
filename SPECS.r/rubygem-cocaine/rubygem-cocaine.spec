%global gem_name cocaine

Name: rubygem-%{gem_name}
Version: 0.5.7
Release: 4%{?dist}
Summary: A small library for doing (command) lines
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/cocaine
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/thoughtbot/cocaine/pull/86
Patch1: rubygem-cocaine-0.5.7-pathname.patch
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(climate_control) >= 0.0.3
Requires: rubygem(climate_control) < 1.0
Requires: rubygem(posix-spawn)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(bourne)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(activesupport) >= 3.0.0
BuildRequires: rubygem(activesupport) < 5.0
BuildRequires: rubygem(climate_control) >= 0.0.3
BuildRequires: rubygem(climate_control) < 1.0
BuildRequires: rubygem(posix-spawn)
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
A small library for doing (command) lines.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# https://github.com/thoughtbot/cocaine/pull/86
%patch1 -p1

# Remove developer-only files.
for f in .gitignore .travis.yml Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Remove dependency on pry gem.
sed -e "/require 'pry'/d" -i spec/spec_helper.rb

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove extra gemspec file
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  rspec -Ilib spec
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/GOALS
%doc %{gem_instdir}/NEWS.md
%exclude %{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.5.7-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.5.7-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.7-1
- Update to cocaine 0.5.7 (rhbz#1197913)

* Wed Dec 17 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.5-1
- Update to cocaine 0.5.5 (RHBZ #1172652)

* Sat Nov 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.4-3
- Update to latest Fedora Ruby guidelines (drop explicit Requires and Provides)
- Use %%license tag
- Patch for Rails 4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.4-1
- Update to cocaine 0.5.4 (RHBZ #1082319)

* Sat Nov 09 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.3-1
- Update to cocaine 0.5.3
- Move README to main package
- Remove extraneous comment
- Remove extraneous BR: ruby
- Remove Gemfile and Rakefile during %%prep
- Exclude rspec tests from binary packages
- Use HTTPS url

* Sat Jul 27 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.5.1-1
- Update to cocaine 0.5.1

* Fri Aug 03 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.0-1
- Update to cocaine 0.3.0
- RHEL 6 compatibility

* Fri Aug 03 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.2.1-1
- Initial package, created by gem2rpm 0.8.1
