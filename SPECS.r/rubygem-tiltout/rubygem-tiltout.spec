# Generated from tiltout-1.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name tiltout

Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 4%{?dist}
Summary: Tilt templates with layouts and helpers
Group: Development/Languages
License: MIT
URL: http://gitorious.org/gitorious/tiltout
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(tilt) => 1.3
BuildArch: noarch

%description
Tiltout is a small abstraction on top of Tilt that allows you to render
templates with optional layouts, share state between layout and template,
register helper modules and optionally cache templates.


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

# Remove dependency on bundler.
sed -i -e '/require "bundler\/setup"/d' test/%{gem_name}_test.rb

# Remove developer-only files.
for f in Gemfile Gemfile.lock Rakefile .travis.yml; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

# Relax Tilt dependency.
sed -i '/dependency.*tilt/ s/\["~> 1\.3"\]/[">= 1.3", "< 3"]/' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm -rf .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # Fix compatibility with recent Mocha.
  sed -i 's|mocha|mocha/mini_test|' test/*_test.rb

  # Fix compatibility with tilt >= 1.4.0
  sed -i "/def fake_file/a\    File.stubs(:open).with(file, 'rb').returns(content)" test/tiltout_test.rb

  ruby -Ilib test/*_test.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/Readme.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test

%changelog
* Wed Sep 16 2015 Vít Ondruch <vondruch@redhat.com> - 1.4.0-4
- Relax Tilt dependency.
- Fix FTBFS (rhbz#1239973).

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.0-1
- Initial package
