%global gem_name resque

Name: rubygem-%{gem_name}
Version: 1.25.2
Release: 7%{?dist}
Summary: A Redis-backed queueing system
Group: Development/Languages
License: MIT
URL: https://github.com/resque/resque
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/resque/resque/pull/1202
Patch0: rubygem-resque-1.25.2-assert-raises.patch
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(redis-namespace) => 1.3
Requires: rubygem(redis-namespace) < 2
Requires: rubygem(vegas) => 0.1.2
Requires: rubygem(vegas) < 0.2
Requires: rubygem(sinatra) >= 0.9.2
Requires: rubygem(multi_json) => 1.0
Requires: rubygem(multi_json) < 2
Requires: rubygem(mono_logger) => 1.0
Requires: rubygem(mono_logger) < 2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(redis-namespace) => 1.3
BuildRequires: rubygem(redis-namespace) < 2
BuildRequires: rubygem(sinatra) >= 0.9.2
BuildRequires: rubygem(multi_json) => 1.0
BuildRequires: rubygem(multi_json) < 2
BuildRequires: rubygem(mono_logger) => 1.0
BuildRequires: rubygem(mono_logger) < 2
BuildRequires: rubygem(rack-test)
BuildRequires: redis
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

# The ruby(release) package already provides a usable Ruby interpreter.
# Filter the extra /usr/bin/ruby requirement here.
%global __requires_exclude ^/usr/bin/ruby$

%description
Resque is a Redis-backed Ruby library for creating background jobs, placing
those jobs on multiple queues, and processing them later.  Background jobs
can be any Ruby class or module that responds to perform. Your existing
classes can easily be converted to background jobs or you can create new
classes specifically to do work. Or, you can do both.
Resque is heavily inspired by DelayedJob and is comprised of three parts:
* A Ruby library for creating, querying, and processing jobs
* A Rake task for starting a worker which processes jobs
* A Sinatra app for monitoring queues, jobs, and workers.


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

# Remove dependency on bundler
sed -e "/require 'bundler\/setup'/d" -i test/test_helper.rb

# Remove /usr/bin/env from shebang so RPM doesn't consider this a dependency
for f in bin/resque bin/resque-web; do
  sed -i 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' $f
done

# Remove developer-only file.
rm Rakefile
sed -i 's|"Rakefile",||g' %{gem_name}.gemspec

# Patch to work with Minitest 5:
# https://github.com/resque/resque/pull/1202
%patch0 -p1

# More fixes that apply for Minitest 5:
# Get the major version number of the Minitest gem
minitest=$(ruby -r 'minitest/unit' \
  -e "puts Minitest::Unit::VERSION.split('.')[0]")
if [ $minitest > 4 ]; then
  # Conditionally correct Minitest usage for Minitest versions 5 and above.
  # Fedora 20 has Minitest 4.x, and Fedora 21 has Minitest 5.x.
  # Just remove the call to test/unit altogether.
  sed -i "/require 'test\/unit'/d" test/test_helper.rb
  # This after_tests syntax is deprecated. Switch to the newer syntax.
  sed -i "s/MiniTest::Unit.after_tests/Minitest.after_run/g" test/test_helper.rb
  # Switch the class name throughout the codebase.
  for f in $(find . -type f); do
    sed -i "s/Test::Unit::TestCase/Minitest::Test/g" $f
  done
  # Switch to the newer Minitest functions.
  for f in $(find test -type f); do
    sed -i "s/assert_not_nil/refute_nil/g" $f
    sed -i "s/assert_not_equal/refute_equal/g" $f
  done
fi

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

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
  mkdir log
  ruby -I'lib:test' -e 'Dir.glob "./test/*_test.rb", &method(:require)'
  rm -r log
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.markdown
%{_bindir}/resque
%{_bindir}/resque-web
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HISTORY.md
%exclude %{gem_instdir}/test

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.25.2-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.25.2-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.25.2-5
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.25.2-3
- Add missing patch to git (oops)

* Tue Apr 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.25.2-2
- Add missing gem source (oops)

* Tue Apr 08 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.25.2-1
- Update to 1.25.2 (RHBZ #1072279)
- Add Minitest 5 compatibility
- Update %%check invocation so tests actually run and pass

* Fri Nov 01 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.25.1-1
- Initial package
