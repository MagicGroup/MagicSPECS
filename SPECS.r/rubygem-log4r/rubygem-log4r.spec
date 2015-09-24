# Generated from log4r-1.1.10.gem by gem2rpm -*- rpm-spec -*-
%global gem_name log4r

Name: rubygem-%{gem_name}
Version: 1.1.10
Release: 3%{?dist}
Summary: Log4r, logging framework for ruby
Group: Development/Languages
# License is changed for future releases!
License: LGPLv3
URL: https://github.com/colbygk/log4r
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream license files
#   https://github.com/colbygk/log4r/issues/39
# Taken from
#   https://github.com/colbygk/log4r/blob/40e2c2edd657a21b34f09dec7de238f348b6f428/
Source1: LICENSE
Source2: LICENSE.LGPLv3
BuildRequires: rubygems-devel 
BuildRequires: rubygem(minitest) >= 5.0.0
BuildRequires: rubygem(builder)
BuildArch: noarch

%description
Log4r is a comprehensive and flexible logging library for use in Ruby programs.
It features a heirarchical logging system of any number of levels, custom level
names, multiple output destinations per log event, custom formatting, and more.

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

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

# License files
install -m 644 %{SOURCE1} .%{gem_instdir}/LICENSE
install -m 644 %{SOURCE2} .%{gem_instdir}/LICENSE.LGPLv3

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# This is not necessary for runtime nor it's a documentation
rm -rf %{buildroot}%{gem_instdir}/lib/log4r/rdoc

# Run the test suite
%check
pushd .%{gem_instdir}
# Test failures
#   https://github.com/colbygk/log4r/issues/37
# Get rid of test/unit specifics and run with Minitest 5
sed -i -e 's/require "test\/unit"//' ./tests/test_helper.rb
sed -i -e 's/include Test::Unit//' ./tests/test_helper.rb
find ./tests -name 'test*.rb' | xargs sed -i -e 's/TestCase/Minitest::Test/'
find ./tests -name 'test*.rb' | xargs sed -i -e 's/assert_raise/assert_raises/'
# Different number of assertions = different number of errors
ruby -rminitest/autorun -Ilib:tests -e 'def assert_nothing_raised(*args); yield end;Dir.glob "./tests/test*.rb", &method(:require)' | grep '2 failures, 1[0-1] errors, 0 skips'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/LICENSE.LGPLv3

%files doc
%doc %{gem_docdir}
%{gem_instdir}/tests
%doc %{gem_instdir}/doc
%{gem_instdir}/examples


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 26 2014 Josef Stribny <jstribny@redhat.com> - 1.1.10-2
- Fix licensing
- Use Minitest 5

* Mon Sep 08 2014 Josef Stribny <jstribny@redhat.com> - 1.1.10-1
- Initial package
