%global gem_name hipchat

Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 3%{?dist}
Summary: Ruby library to interact with HipChat
Group: Development/Languages
License: MIT
URL: https://github.com/hipchat/hipchat-rb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Remove dependency on coveralls. Submitted upstream:
# https://github.com/hipchat/hipchat-rb/pull/116
Patch0: rubygem-hipchat-1.4.0-coveralls.patch
# Port to rspec 3. Submitted upstream:
# https://github.com/hipchat/hipchat-rb/pull/115
Patch1: rubygem-hipchat-1.4.0-rspec3.patch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(httparty)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(httparty)
BuildRequires: rubygem(json)
BuildRequires: rubygem(rr)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(webmock)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Ruby library to interact with HipChat


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
for f in .coveralls.yml .document .gitignore .ruby-gemset .ruby-version \
.travis.yml Gemfile Rakefile; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Remove dependency on coveralls
# https://github.com/hipchat/hipchat-rb/pull/116
%patch0 -p1
# Update for rspec 3
# https://github.com/hipchat/hipchat-rb/pull/115
%if 0%{?fedora} > 21 || 0%{?rhel} > 7
%patch1 -p1
%endif

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# remove unnecessary gemspec
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
%doc %{gem_instdir}/README.textile
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/spec


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 21 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-1
- Update to hipchat 1.4.0 (RHBZ #1129087)
- Drop json/spec_helper change (was merged upstream)
- Submit "make coveralls optional" patch for inclusion upstream
- Conditionally patch for rspec 3
- Use %%license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.2.0-1
- Update to hipchat 1.2.0 (RHBZ #1103690)
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Mar 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-2
- Add missing .gem source

* Tue Mar 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.0-1
- Update to hipchat 1.1.0 (RHBZ #1074980)

* Sat Dec 28 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-1
- Update to hipchat 1.0.1 (RHBZ #1044454)

* Mon Nov 25 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.14.0-1
- Update to hipchat 0.14.0

* Thu Nov 21 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.13.0-1
- Update to hipchat 0.13.0
- Remove excluded files in %%prep

* Mon Nov 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.12.0-2
- Exclude Gemfile, Rakefile, and tests from binary package
- Move README to main package

* Thu Oct 03 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.12.0-1
- Initial package
