%global gem_name capillary

Name: rubygem-%{gem_name}
Version: 1.0.4
Release: 5%{?dist}
Summary: Generate a JSON payload from Git log output
Group: Development/Languages
License: AGPLv3+
URL: https://gitorious.org/capillary
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(json)
Requires: rubygem(htmlentities)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(htmlentities)
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

# The ruby(release) package already provides a usable Ruby interpreter.
# Filter the extra /usr/bin/ruby requirement here.
%global __requires_exclude ^/usr/bin/ruby$

%description
Capillary works in conjunction with capillary.js, which outputs a beautiful
graphical representation of your repository history.

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

# Fix shebang
sed -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' bin/%{gem_name}

# Remove dependency on bundler
sed -e '\|require "bundler/setup"|d' -i test/test_helper.rb

# Remove dependency on simplecov
sed -e '/simplecov/Id' -i test/test_helper.rb

# Remove developer-only gitignore file
rm .gitignore
sed -i 's|".gitignore",||' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary files
pushd .%{gem_instdir}/
  rm %{gem_name}.gemspec
  rm Gemfile
  rm Gemfile.lock
  rm Rakefile
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
  ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README
%{_bindir}/capillary
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 11 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.4-4
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Adjustments for Minitest 5 (RHBZ #1107075)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 22 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.4-2
- Add missing dependency on htmlentities
- Remove dependency on simplecov
- Use HTTPS URL

* Fri Oct 11 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.4-1
- Update to capillary 1.0.4
- Drop upstreamed mini_shoulda patch

* Wed Oct 09 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-3
- Adjust mini_shoulda gemspec removal regex to remove during %%prep

* Tue Oct 08 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-2
- Remove mini_shoulda from installed gemspec
- Add "test" directory to load-path during %%check
- Move README to main package
- Do not ship Gemfile, Gemfile.lock, Rakefile, or tests
- Remove /usr/bin/env and /usr/bin/ruby from auto-requirements

* Mon Oct 07 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.3-1
- Update to capillary 1.0.3
- Drop License file, since upstream ships their own
- Drop EL6 support

* Sat Feb 16 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.2-1
- Update to capillary 1.0.2
- Remove upsteamed patch for reading test fixtures as utf-8
- Update license to AGPLv3+
- RHEL 6 compatibility

* Thu Aug 09 2012 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.0.1-1
- Initial package, created by gem2rpm 0.8.1
